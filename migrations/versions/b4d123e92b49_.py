"""empty message

Revision ID: b4d123e92b49
Revises: 828faea5a6ab
Create Date: 2022-12-03 21:43:39.578238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4d123e92b49'
down_revision = '828faea5a6ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('points', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_points', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('rd16_points', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('quarters_points', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('semis_points', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('finals_points', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('points', schema=None) as batch_op:
        batch_op.drop_column('finals_points')
        batch_op.drop_column('semis_points')
        batch_op.drop_column('quarters_points')
        batch_op.drop_column('rd16_points')
        batch_op.drop_column('group_points')

    # ### end Alembic commands ###