"""Cleanup legacy singular tables

Revision ID: f8e7d6c5b4a3
Revises: d6d74667522f
Create Date: 2026-04-13 16:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f8e7d6c5b4a3'
down_revision = 'd6d74667522f'
branch_labels = None
depends_on = None


def upgrade():
    # Drop legacy singular tables after the plural versions already exist
    op.drop_table('subsection')
    op.drop_table('section')
    op.drop_table('category')


def downgrade():
    # Recreate legacy singular tables in reverse order with original foreign keys
    op.create_table(
        'category',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'section',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('category_id', sa.Uuid(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['category.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'subsection',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(length=150), nullable=False),
        sa.Column('section_id', sa.Uuid(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['section_id'], ['section.id']),
        sa.PrimaryKeyConstraint('id'),
    )
