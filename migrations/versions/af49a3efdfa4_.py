"""empty message

Revision ID: af49a3efdfa4
Revises: bcac9c071e26
Create Date: 2017-12-11 22:24:21.040000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'af49a3efdfa4'
down_revision = 'bcac9c071e26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('father_node', sa.Integer(), nullable=True))
    op.drop_column('categories', 'belong_to')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('belong_to', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('categories', 'father_node')
    # ### end Alembic commands ###
