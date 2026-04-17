"""Add warehouses and bins tables

Revision ID: 2d7d917e6083
Revises: f4d2b651a9d0
Create Date: 2026-04-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d7d917e6083'
down_revision = 'f4d2b651a9d0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    # Create warehouses table
    op.create_table(
        'warehouses',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('estado', sa.String(length=50), nullable=False),
        sa.Column('direccion', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_warehouses_nombre', 'warehouses', ['nombre'], unique=False)

    # Create bins table
    op.create_table(
        'bins',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('x', sa.String(length=15), nullable=False, server_default=sa.text("'0'")),
        sa.Column('y', sa.String(length=15), nullable=False, server_default=sa.text("'0'")),
        sa.Column('z', sa.String(length=15), nullable=False, server_default=sa.text("'0'")),
        sa.Column('warehouse_id', sa.Uuid(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='RESTRICT'),
    )
    op.create_index('idx_bins_warehouse_id', 'bins', ['warehouse_id'], unique=False)


def downgrade():
    op.drop_index('idx_bins_warehouse_id', table_name='bins')
    op.drop_table('bins')
    op.drop_index('idx_warehouses_nombre', table_name='warehouses')
    op.drop_table('warehouses')