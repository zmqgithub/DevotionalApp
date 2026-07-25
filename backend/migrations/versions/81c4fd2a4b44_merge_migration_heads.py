"""merge migration heads

Revision ID: 81c4fd2a4b44
Revises: 2382a9f4660c, bb79dc8b4bdc
Create Date: 2026-07-25 14:27:24.281467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision = "new_revision_id"
down_revision = "0e03f0d17a01"

# revision identifiers, used by Alembic.
revision: str = '81c4fd2a4b44'
down_revision: Union[str, Sequence[str], None] = ('2382a9f4660c', 'bb79dc8b4bdc')
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
