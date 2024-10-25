"""empty message

Revision ID: a0be5475a3b9
Revises: 3bfe56d16f60
Create Date: 2024-06-04 10:46:03.075149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0be5475a3b9'
down_revision = '3bfe56d16f60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_time', sa.DateTime(), nullable=True),
    sa.Column('comment_score', sa.Float(), nullable=False),
    sa.Column('comment_content', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
