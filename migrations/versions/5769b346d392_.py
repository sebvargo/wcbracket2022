"""empty message

Revision ID: 5769b346d392
Revises: 99a6abcbdcfe
Create Date: 2022-11-29 07:31:06.668894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5769b346d392'
down_revision = '99a6abcbdcfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('official_stage', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team1', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('team2', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('team3', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('team4', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('official_stage', schema=None) as batch_op:
        batch_op.drop_column('team4')
        batch_op.drop_column('team3')
        batch_op.drop_column('team2')
        batch_op.drop_column('team1')

    # ### end Alembic commands ###