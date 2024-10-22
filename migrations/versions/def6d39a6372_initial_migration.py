"""Initial migration

Revision ID: def6d39a6372
Revises: 
Create Date: 2024-10-22 13:04:54.962347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'def6d39a6372'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rental')
    op.drop_table('booking')
    op.drop_table('car')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('password', sa.VARCHAR(length=50), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    sa.Column('contact_no', sa.INTEGER(), nullable=True),
    sa.Column('address', sa.VARCHAR(length=100), nullable=True),
    sa.Column('role', sa.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact_no'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('car',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('make', sa.VARCHAR(length=50), nullable=False),
    sa.Column('model', sa.VARCHAR(length=50), nullable=False),
    sa.Column('category', sa.VARCHAR(length=50), nullable=False),
    sa.Column('year', sa.INTEGER(), nullable=False),
    sa.Column('price_per_day', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('car_id', sa.INTEGER(), nullable=False),
    sa.Column('start_date', sa.DATE(), nullable=False),
    sa.Column('end_date', sa.DATE(), nullable=False),
    sa.Column('total_cost', sa.FLOAT(), nullable=False),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rental',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('car_id', sa.INTEGER(), nullable=False),
    sa.Column('start_date', sa.DATE(), nullable=False),
    sa.Column('end_date', sa.DATE(), nullable=True),
    sa.Column('start_time', sa.DATETIME(), nullable=False),
    sa.Column('end_time', sa.DATETIME(), nullable=True),
    sa.Column('total_cost', sa.FLOAT(), nullable=False),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.Column('payment_status', sa.BOOLEAN(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
