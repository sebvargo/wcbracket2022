"""empty message

Revision ID: 7042493e4f8a
Revises: 177c2d78b5d7
Create Date: 2022-12-02 12:11:49.004353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7042493e4f8a'
down_revision = '177c2d78b5d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prediction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('round_order', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prediction', schema=None) as batch_op:
        batch_op.drop_column('round_order')

    # ### end Alembic commands ###