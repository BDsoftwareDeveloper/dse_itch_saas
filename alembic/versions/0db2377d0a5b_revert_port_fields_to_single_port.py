"""Revert port fields to single port

Revision ID: 0db2377d0a5b
Revises: 7c36a709b276
Create Date: 2025-05-05 07:53:50.134885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, Integer

# revision identifiers, used by Alembic.
revision: str = '0db2377d0a5b'
down_revision: Union[str, None] = '7c36a709b276'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add 'port' as nullable
    with op.batch_alter_table("servers") as batch_op:
        batch_op.drop_column("primary_port")
        batch_op.drop_column("failover_port")
        batch_op.add_column(sa.Column("port", sa.Integer(), nullable=True))

    # Step 2: Backfill the column with a default value (change `5432` as needed)
    servers_table = table("servers", column("port", Integer))
    op.execute(servers_table.update().values(port=5432))

    # Step 3: Alter to NOT NULL
    with op.batch_alter_table("servers") as batch_op:
        batch_op.alter_column("port", nullable=False)

def downgrade():
    with op.batch_alter_table("servers") as batch_op:
        batch_op.drop_column("port")
        batch_op.add_column(sa.Column("primary_port", sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column("failover_port", sa.Integer(), nullable=True))

