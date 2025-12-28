"""Semana 4: add updated_at to time_entries

Revision ID: 3a9c7c0b2531
Revises: 
Create Date: 2025-12-27 16:48:00.675151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a9c7c0b2531'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'time_entries',
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False
        )
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('time_entries', 'updated_at')
