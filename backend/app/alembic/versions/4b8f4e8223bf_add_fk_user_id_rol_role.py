"""Add FK from user.id_rol to role.id

Revision ID: 4b8f4e8223bf
Revises: b3b1322998f5
Create Date: 2026-04-13 15:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b8f4e8223bf'
down_revision = 'b3b1322998f5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        'user_id_rol_fkey',
        'user',
        'role',
        ['id_rol'],
        ['id'],
    )


def downgrade():
    op.drop_constraint('user_id_rol_fkey', 'user', type_='foreignkey')
