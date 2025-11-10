import asyncio
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

import sys, os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from core.db import Base
from core.config import settings

config = context.config
config.set_main_option('sqlalchemy.url', settings.database_url)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    raise RuntimeError("Offline migrations не поддерживаются с async engine")


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    if "revision" in sys.argv or "autogenerate" in sys.argv:
        sync_engine = create_engine(
            settings.database_url.replace("+asyncpg", "+psycopg2").strip(),
            poolclass=pool.NullPool
        )
        with sync_engine.connect() as connection:
            do_run_migrations(connection)
        sync_engine.dispose()
    else:
        asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
