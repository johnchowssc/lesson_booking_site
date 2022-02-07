"""empty message

Revision ID: ad2009188a02
Revises: b730bc742b80
Create Date: 2022-02-07 09:19:22.943284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad2009188a02'
down_revision = 'b730bc742b80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('slots', sa.Column('paid', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('slots', 'paid')
    # ### end Alembic commands ###