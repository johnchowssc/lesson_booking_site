"""name not unique

Revision ID: 363b74490255
Revises: 5c22c6c9ec86
Create Date: 2022-01-17 14:47:21.464454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '363b74490255'
down_revision = '5c22c6c9ec86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_name', table_name='users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_users_name', 'users', ['name'], unique=False)
    # ### end Alembic commands ###
