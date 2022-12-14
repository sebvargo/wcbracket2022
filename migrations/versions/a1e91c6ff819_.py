"""empty message

Revision ID: a1e91c6ff819
Revises: ef00d958c52b
Create Date: 2022-11-18 16:20:33.917350

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1e91c6ff819'
down_revision = 'ef00d958c52b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('local_time', sa.DateTime(), nullable=True))
        batch_op.drop_index('ix_game_utc_time')
        batch_op.create_index(batch_op.f('ix_game_local_time'), ['local_time'], unique=False)
        batch_op.drop_column('utc_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('utc_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_index(batch_op.f('ix_game_local_time'))
        batch_op.create_index('ix_game_utc_time', ['utc_time'], unique=False)
        batch_op.drop_column('local_time')

    # ### end Alembic commands ###
