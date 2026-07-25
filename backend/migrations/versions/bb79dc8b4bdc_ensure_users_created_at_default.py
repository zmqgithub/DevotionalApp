"""ensure users created_at default

Revision ID: bb79dc8b4bdc
Revises: ff0073113463
Create Date: 2026-07-25 14:17:29.020220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision = "new_revision_id"
down_revision = "0e03f0d17a01"

# revision identifiers, used by Alembic.
revision: str = 'bb79dc8b4bdc'
down_revision: Union[str, Sequence[str], None] = 'ff0073113463'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        server_default=None,
    )
