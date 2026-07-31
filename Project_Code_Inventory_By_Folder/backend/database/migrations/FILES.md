# Folder: backend/database/migrations Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/database/migrations`

Contains 2 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/database/migrations/env.py

**Folder path:** `backend/database/migrations`

**File path:** `backend/database/migrations/env.py`

```python
from logging.config import fileConfig

from alembic import context

from database.base import Base
from database.connection import DATABASE_URL
from database import models  # noqa: F401


config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = context.config.attributes.get("connection")
    if connectable is None:
        from sqlalchemy import create_engine

        connectable = create_engine(DATABASE_URL, pool_pre_ping=True)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## backend/database/migrations/script.py.mako

**Folder path:** `backend/database/migrations`

**File path:** `backend/database/migrations/script.py.mako`

```
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa


revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
```
