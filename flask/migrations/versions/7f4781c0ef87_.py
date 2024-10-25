"""empty message

Revision ID: 7f4781c0ef87
Revises: 28a75346eff0
Create Date: 2024-06-02 18:01:15.615121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f4781c0ef87'
down_revision = '28a75346eff0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('total_rent_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car', 'total_rent_number')
    # ### end Alembic commands ###