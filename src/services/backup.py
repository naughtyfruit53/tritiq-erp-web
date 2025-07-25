# src/services/backup.py
from fastapi import UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import List
from io import StringIO
import logging
import os
from datetime import datetime
import shutil
import tempfile
from src.db.models.base import Base

logger = logging.getLogger(__name__)

async def get_table_names(db: AsyncSession) -> List[str]:
    result = await db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"))
    return [row[0] for row in result.fetchall()]

async def export_table_data(db: AsyncSession, table_name: str) -> List[str]:
    result = await db.execute(text(f"SELECT * FROM {table_name}"))
    rows = result.fetchall()
    if not rows:
        return []
    
    result = await db.execute(text(f"PRAGMA table_info({table_name})"))
    columns = [col[1] for col in result.fetchall()]
    
    insert_statements = []
    for row in rows:
        values = ', '.join(["'" + str(v).replace("'", "''") + "'" if v is not None else 'NULL' for v in row])
        insert_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values});")
    return insert_statements

async def create_backup(db: AsyncSession) -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".sql")
    tables = await get_table_names(db)
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        for table in tables:
            insert_statements = await export_table_data(db, table)
            if insert_statements:
                f.write(f"-- Table: {table}\n")
                for stmt in insert_statements:
                    f.write(stmt + "\n")
                f.write("\n")
    logger.info(f"Backup created at {temp_file.name}")
    return temp_file.name

async def perform_restore(db: AsyncSession, file: UploadFile):
    content = await file.read()
    sql_commands = content.decode('utf-8').split(';')
    await db.execute(text("BEGIN TRANSACTION;"))
    try:
        tables = await get_table_names(db)
        for table in tables:
            await db.execute(text(f"DELETE FROM {table};"))
        
        for command in sql_commands:
            command = command.strip()
            if not command or command.startswith('--'):
                continue
            await db.execute(text(command))
        
        await db.commit()
        logger.info("Restore completed successfully")
    except Exception as e:
        await db.rollback()
        logger.error(f"Restore failed: {e}")
        raise e
