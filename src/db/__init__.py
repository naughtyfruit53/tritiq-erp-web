from dotenv import load_dotenv
import os

# Calculate absolute path to .env in project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from .supabase_ssl import supabase_ssl_context

# Get and validate connection string
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment variables")

# Print for debugging (remove in production)
print(f"DEBUG: Loaded .env from {dotenv_path}")
print(f"DEBUG: DATABASE_URL = {DATABASE_URL}")

# Force asyncpg driver if not specified
if not DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Determine if local DB (no SSL) or remote (e.g., Supabase with SSL)
connect_args = {}
if 'localhost' not in DATABASE_URL and '127.0.0.1' not in DATABASE_URL and not DATABASE_URL.startswith("sqlite"):
    connect_args["ssl"] = supabase_ssl_context

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=True,
    connect_args=connect_args
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db():
    """
    Async database session generator
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()