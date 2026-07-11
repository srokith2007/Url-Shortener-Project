"""create users and urls table

Revision ID: a8755f3f32f5
Revises: 
Create Date: 2026-07-09 16:32:18.906296

"""
from turtle import title
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8755f3f32f5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
     op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False, unique=True),
        sa.Column("email_id", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
    )
     
     op.create_table(
        "urls",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("url", sa.String(), nullable=False, unique=True),
        sa.Column("short_code", sa.String(), nullable=True, unique=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "expires_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            server_default=sa.text("now() + interval '1 year'"),
        ),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )


def downgrade():
    op.drop_table("urls")
    op.drop_table("users")
