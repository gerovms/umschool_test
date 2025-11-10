"""Add subject enum type

Revision ID: 6a99e7a704dc
Revises: 
Create Date: 2025-11-09 18:07:16.968225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.enums import SubjectEnum


revision: str = '6a99e7a704dc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("tg_id", sa.BigInteger, unique=True, nullable=True),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("surname", sa.String(255), nullable=False),
    )

    op.create_table(
        "scores",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "subject",
            sa.Enum(SubjectEnum, name="subjectenum", create_type=False),
            nullable=False
        ),
        sa.Column("score", sa.Integer, nullable=False),
        sa.UniqueConstraint("user_id", "subject", name="uq_user_subject"),
        sa.CheckConstraint("score >= 0 AND score <= 100", name="ck_score_range"),
    )


def downgrade():
    op.drop_table("scores")
    op.drop_table("users")
