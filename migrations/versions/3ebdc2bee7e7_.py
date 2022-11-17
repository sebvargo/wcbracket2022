"""empty message

Revision ID: 3ebdc2bee7e7
Revises: 133630b69e63
Create Date: 2022-11-16 13:04:28.303476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ebdc2bee7e7'
down_revision = '133630b69e63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stage',
    sa.Column('stage_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stage_type', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('winner', sa.String(length=3), nullable=True),
    sa.Column('runner_up', sa.String(length=3), nullable=True),
    sa.Column('pts_winner_outcome', sa.Integer(), nullable=True),
    sa.Column('pts_runner_score', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('stage_id')
    )
    op.create_table('team',
    sa.Column('team_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('country_code', sa.String(length=3), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('goals_scored', sa.Integer(), nullable=True),
    sa.Column('goal_difference', sa.Integer(), nullable=True),
    sa.Column('stage_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['stage_id'], ['stage.stage_id'], ),
    sa.PrimaryKeyConstraint('team_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team')
    op.drop_table('stage')
    # ### end Alembic commands ###