"""Split port into primary_port and failover_port

Revision ID: 7c36a709b276
Revises: 038382edda25
Create Date: 2025-05-05 07:12:48.234333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c36a709b276'
down_revision: Union[str, None] = '038382edda25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Rename existing "port" to "primary_port"
    op.alter_column("servers", "port", new_column_name="primary_port")
    # Add new "failover_port" column
    op.add_column("servers", sa.Column("failover_port", sa.Integer(), nullable=True))


def downgrade():
    op.drop_column("servers", "failover_port")
    op.alter_column("servers", "primary_port", new_column_name="port")
