# src/db/crud/backup.py
import logging
from datetime import datetime
import os
import re
from sqlalchemy import text, MetaData
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.base import Base  # Assuming all models are imported in base.py

logger = logging.getLogger(__name__)

async def get_table_names(db: AsyncSession) -> list:
    """Retrieve all table names from the database metadata."""
    try:
        metadata = Base.metadata
        return [table.name for table in metadata.sorted_tables]
    except Exception as e:
        logger.error(f"Failed to get table names: {e}")
        return []

async def export_table_data(db: AsyncSession, table_name: str) -> list:
    """Export data from a table as SQL INSERT statements."""
    try:
        table = Base.metadata.tables[table_name]
        result = await db.execute(table.select())
        rows = result.fetchall()
        if not rows:
            return []
        
        columns = [col.name for col in table.columns]
        
        insert_statements = []
        for row in rows:
            values = ', '.join(["'" + str(v).replace("'", "''") + "'" if v is not None else 'NULL' for v in row])
            insert_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values});")
        return insert_statements
    except Exception as e:
        logger.error(f"Failed to export data from {table_name}: {e}")
        return []

async def get_column_info(db: AsyncSession, table_name: str) -> dict:
    """Retrieve column information for a table."""
    try:
        query = text(f"""
            SELECT column_name, is_nullable
            FROM information_schema.columns
            WHERE table_name = :table_name
        """)
        result = await db.execute(query, {"table_name": table_name})
        return {row[0]: row[1] for row in result.fetchall()}
    except Exception as e:
        logger.error(f"Failed to get column info for {table_name}: {e}")
        return {}

async def create_backup(db: AsyncSession, backup_path: str):
    """Perform the database backup operation to a file."""
    try:
        tables = await get_table_names(db)
        with open(backup_path, 'w', encoding='utf-8') as f:
            for table in tables:
                insert_statements = await export_table_data(db, table)
                if insert_statements:
                    f.write(f"-- Table: {table}\n")
                    for stmt in insert_statements:
                        f.write(stmt + "\n")
                    f.write("\n")
        return backup_path
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        raise e

async def perform_restore(db: AsyncSession, backup_path: str):
    """Perform the database restore operation from a file."""
    try:
        with open(backup_path, 'r', encoding='utf-8') as f:
            sql_statements = f.read().splitlines()
        
        tables = await get_table_names(db)
        for table in tables:
            await db.execute(text(f"DELETE FROM {table}"))
        
        for stmt in sql_statements:
            if stmt.strip() and not stmt.startswith('--'):
                table_name, columns, values_str = parse_insert_columns(stmt)
                if not table_name:
                    continue
                
                column_info = await get_column_info(db, table_name)
                if not column_info:
                    logger.warning(f"Table {table_name} not found in database, skipping")
                    continue
                
                # Validate columns match
                if set(columns) - set(column_info.keys()):
                    logger.warning(f"Column mismatch for {table_name}, skipping statement")
                    continue
                
                await db.execute(text(stmt))
        
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to perform restore: {e}")
        raise e

def parse_insert_columns(insert_stmt: str):
    """Parse an INSERT statement to extract table name, columns, and values."""
    match = re.match(r"INSERT\s+INTO\s+(\w+)\s*\((.*?)\)\s*VALUES\s*\((.*)\);", insert_stmt, re.IGNORECASE | re.DOTALL)
    if not match:
        logger.error(f"Invalid INSERT statement: {insert_stmt}")
        return None, None, None
    
    table_name = match.group(1)
    columns_str = match.group(2).strip()
    values_str = match.group(3).strip()
    
    columns = []
    current = ""
    in_quotes = False
    for char in columns_str + ',':
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            if current.strip():
                columns.append(current.strip().strip('"'))
            current = ""
        else:
            current += char
    if current.strip():
        columns.append(current.strip().strip('"'))
    
    return table_name, columns, values_str