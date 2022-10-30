"""empty message

Revision ID: b04ec7ce6e23
Revises: 6094b41e4468
Create Date: 2022-10-11 17:01:14.893257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b04ec7ce6e23'
down_revision = '6094b41e4468'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('class_slots', schema=None) as batch_op:
        batch_op.add_column(sa.Column('class_capacity', sa.Integer(), nullable=True))
        batch_op.drop_column('capacity')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('class_slots', schema=None) as batch_op:
        batch_op.add_column(sa.Column('capacity', sa.INTEGER(), nullable=False))
        batch_op.drop_column('class_capacity')

    # ### end Alembic commands ###
