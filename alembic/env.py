from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import your models here
from app.models.user import User
from app.models.tenant import Tenant
from app.models.server_config import Server

# If all your models use a common Base, import it and set metadata from Base
# Example: from app.models.base import Base
# target_metadata = Base.metadata

# If not, just pick one (all share same metadata under Base)
target_metadata = User.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Retrieve the SQLAlchemy DB URI from env or hardcode if needed
# You can also set this in alembic.ini under sqlalchemy.url
DB_URL = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://saiful:saiful123@dse_postgres:5432/saas_dse_db")
config.set_main_option("sqlalchemy.url", DB_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
