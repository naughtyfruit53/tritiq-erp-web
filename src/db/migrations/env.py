# src/db/migrations/env.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))  # Add project root to path

from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
from src.db.models.base import Base
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env from project root

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")  # Use sync driver for Alembic
DATABASE_URL = DATABASE_URL.replace('%', '%%')  # Escape '%' for configparser

config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)  # Dynamically set URL

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()