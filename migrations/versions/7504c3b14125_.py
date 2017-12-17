"""empty message

Revision ID: 7504c3b14125
Revises: 77402c9c992c
Create Date: 2017-12-17 11:54:19.439000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7504c3b14125'
down_revision = '77402c9c992c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('keywords', sa.TEXT(), nullable=True))
    op.drop_column('articles', 'keys')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('keys', mysql.TEXT(), nullable=True))
    op.drop_column('articles', 'keywords')
    # ### end Alembic commands ###
