"""empty message

Revision ID: 177c2d78b5d7
Revises: b561a7e4ff46
Create Date: 2022-12-02 08:20:38.182282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '177c2d78b5d7'
down_revision = 'b561a7e4ff46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('round_order', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_column('round_order')

    # ### end Alembic commands ###
