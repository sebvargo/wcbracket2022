"""empty message

Revision ID: 8adb37392a67
Revises: 4612f23e3d2f
Create Date: 2022-11-18 15:55:07.084350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8adb37392a67'
down_revision = '4612f23e3d2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('goals1', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('goals2', sa.Integer(), nullable=True))
        batch_op.drop_column('cell1')
        batch_op.drop_column('cell2')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cell2', sa.VARCHAR(length=4), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('cell1', sa.VARCHAR(length=4), autoincrement=False, nullable=True))
        batch_op.drop_column('goals2')
        batch_op.drop_column('goals1')

    # ### end Alembic commands ###