"""empty message

Revision ID: d15237421575
Revises: 
Create Date: 2024-06-01 20:47:54.797710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd15237421575'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('register_time', sa.DateTime(), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.Column('ip', sa.String(length=15), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('audit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('op_time', sa.DateTime(), nullable=True),
    sa.Column('op_ip', sa.String(length=15), nullable=False),
    sa.Column('op_user', sa.String(length=32), nullable=False),
    sa.Column('op_module', sa.String(length=32), nullable=False),
    sa.Column('op_event', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('brand',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('photo', sa.String(length=48), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('notice',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('content', sa.String(length=1024), nullable=False),
    sa.Column('release_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('permission_ids', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('register_time', sa.DateTime(), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.Column('ip', sa.String(length=15), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('car',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=False),
    sa.Column('license_plate_number', sa.String(length=7), nullable=False),
    sa.Column('car_type', sa.String(length=8), nullable=True),
    sa.Column('color', sa.String(length=16), nullable=True),
    sa.Column('parking_type', sa.Integer(), nullable=True),
    sa.Column('is_skylight', sa.Boolean(), nullable=True),
    sa.Column('seat_number', sa.Integer(), nullable=False),
    sa.Column('daily_rent', sa.Integer(), nullable=False),
    sa.Column('photo', sa.String(length=48), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('license_plate_number')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('car', sa.Integer(), nullable=False),
    sa.Column('tenant', sa.Integer(), nullable=False),
    sa.Column('lease_time', sa.DateTime(), nullable=True),
    sa.Column('imputed_rent', sa.Integer(), nullable=False),
    sa.Column('lease_duration', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car'], ['car.id'], ),
    sa.ForeignKeyConstraint(['tenant'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_table('car')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('notice')
    op.drop_table('brand')
    op.drop_table('audit')
    op.drop_table('admin')
    # ### end Alembic commands ###
