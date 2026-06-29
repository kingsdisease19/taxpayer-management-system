"""Add user role enum column

Revision ID: c0e8d2a1b4f5
Revises: 816c0fac5095
Create Date: 2026-06-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c0e8d2a1b4f5'
down_revision: Union[str, Sequence[str], None] = '816c0fac5095'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    role_enum = sa.Enum(
        'registration_officer',
        'supervisor',
        'administrator',
        name='roleenum',
    )
    role_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'users',
        sa.Column('role', role_enum, nullable=False, server_default='registration_officer')
    )


def downgrade() -> None:
    op.drop_column('users', 'role')
    sa.Enum(name='roleenum').drop(op.get_bind(), checkfirst=True)
