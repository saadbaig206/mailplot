import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import get_settings
from src.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

settings = get_settings()
# Check for command line override via -x db_url=<url>
x_args = context.get_x_argument(as_dictionary=True)
if "db_url" in x_args:
    db_url = x_args["db_url"]
else:
    db_url = getattr(settings, "SYNC_DATABASE_URL", None) or getattr(settings, "DATABASE_URL", "")

# Convert async to sync for alembic migrations
db_url = db_url.replace("+asyncpg", "").replace("+aiosqlite", "")
config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
