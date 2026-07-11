"""added is_admin authorization in users tabel

Revision ID: 37b97f2993fc
Revises: 1db29d1b093e
Create Date: 2026-07-10 02:26:33.579515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37b97f2993fc'
down_revision: Union[str, Sequence[str], None] = '1db29d1b093e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "is_admin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false")
        )
    )


def downgrade() -> None:
    op.drop_column("users", "is_admin")