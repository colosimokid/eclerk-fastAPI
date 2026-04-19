"""Add products table

Revision ID: a1b2c3d4e5f6
Revises: f4d2b651a9d0
Create Date: 2026-04-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'f4d2b651a9d0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table(
        'products',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('category_id', sa.Uuid(), nullable=False),
        sa.Column('section_id', sa.Uuid(), nullable=False),
        sa.Column('sub_section_id', sa.Uuid(), nullable=True),
        sa.Column('codigo', sa.String(length=50), nullable=False),
        sa.Column('referencia', sa.String(length=100), nullable=True),
        sa.Column('descripcion', sa.String(length=255), nullable=False),
        sa.Column('descripcion_adicional', sa.Text(), nullable=True),
        sa.Column('cod_barras_1', sa.String(length=50), nullable=True),
        sa.Column('cod_barras_2', sa.String(length=50), nullable=True),
        sa.Column('cod_barras_3', sa.String(length=50), nullable=True),
        sa.Column('brand_id', sa.Uuid(), nullable=True),
        sa.Column('ultimo_coste', sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column('peso', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('impuesto_compra', sa.Numeric(precision=5, scale=2), server_default=sa.text('0'), nullable=False),
        sa.Column('impuesto_venta', sa.Numeric(precision=5, scale=2), server_default=sa.text('0'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='RESTRICT', onupdate='CASCADE'),
        sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ondelete='RESTRICT', onupdate='CASCADE'),
        sa.ForeignKeyConstraint(['sub_section_id'], ['sub_sections.id'], ondelete='SET NULL', onupdate='CASCADE'),
        sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ondelete='SET NULL', onupdate='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_products_category_id', 'products', ['category_id'], unique=False)
    op.create_index('idx_products_section_id', 'products', ['section_id'], unique=False)
    op.create_index('idx_products_sub_section_id', 'products', ['sub_section_id'], unique=False)
    op.create_index('idx_products_brand_id', 'products', ['brand_id'], unique=False)
    op.create_index('idx_products_codigo', 'products', ['codigo'], unique=False)


def downgrade():
    op.drop_index('idx_products_codigo', table_name='products')
    op.drop_index('idx_products_brand_id', table_name='products')
    op.drop_index('idx_products_sub_section_id', table_name='products')
    op.drop_index('idx_products_section_id', table_name='products')
    op.drop_index('idx_products_category_id', table_name='products')
    op.drop_table('products')