"""semana_6_add_labels_and_subtasks

Revision ID: semana_6_labels_subtasks
Revises: 3a9c7c0b2531
Create Date: 2026-01-08 16:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'semana_6_labels_subtasks'
down_revision = '3a9c7c0b2531'
branch_labels = None
depends_on = None


def upgrade():
    # Create labels table
    op.create_table(
        'labels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('card_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_labels_id'), 'labels', ['id'], unique=False)
    
    # Create subtasks table
    op.create_table(
        'subtasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('card_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('position', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subtasks_id'), 'subtasks', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_subtasks_id'), table_name='subtasks')
    op.drop_table('subtasks')
    op.drop_index(op.f('ix_labels_id'), table_name='labels')
    op.drop_table('labels')
