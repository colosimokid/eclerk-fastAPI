"""Add storage details table

Revision ID: 3b9c5a7f2ecd
Revises: ('2d7d917e6083', 'a1b2c3d4e5f6')
Create Date: 2026-04-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b9c5a7f2ecd'
down_revision = ('2d7d917e6083', 'a1b2c3d4e5f6')
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table(
        'storage_details',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('product_id', sa.Uuid(), nullable=False),
        sa.Column('bin_id', sa.Uuid(), nullable=False),
        sa.Column('qty_on_hand', sa.Numeric(), nullable=False, server_default=sa.text('0')),
        sa.Column('qty_order_on_hand', sa.Numeric(), nullable=False, server_default=sa.text('0')),
        sa.Column('date_last_inventory', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='storage_detail_key'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='storage_detail_product_fk', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['bin_id'], ['bins.id'], name='storage_detail_bin_fk', ondelete='RESTRICT'),
        sa.UniqueConstraint('product_id', 'bin_id', name='storage_detail_product_bin_uq'),
    )
    op.create_index('idx_storage_details_product_id', 'storage_details', ['product_id'], unique=False)
    op.create_index('idx_storage_details_bin_id', 'storage_details', ['bin_id'], unique=False)


def downgrade():
    op.drop_index('idx_storage_details_bin_id', table_name='storage_details')
    op.drop_index('idx_storage_details_product_id', table_name='storage_details')
    op.drop_table('storage_details')
