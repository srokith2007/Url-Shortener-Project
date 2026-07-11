"""changed expired_at to 1 year which was not updated in previous alembic.

Revision ID: 1db29d1b093e
Revises: 2d04208de525
Create Date: 2026-07-09 23:31:32.421987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1db29d1b093e'
down_revision: Union[str, Sequence[str], None] = '2d04208de525'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
    "urls",
    "expires_at",
    server_default=sa.text("now() + interval '1 year'")
)


def downgrade():
    op.alter_column(
        "urls",
        "expires_at",
        server_default=sa.text("now() + interval '2 minutes'")
    )
