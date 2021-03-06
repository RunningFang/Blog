"""empty message

Revision ID: 77402c9c992c
Revises: 116be73789e6
Create Date: 2017-12-15 23:40:22.667000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77402c9c992c'
down_revision = '116be73789e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'articles_ibfk_4', 'articles', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(u'articles_ibfk_4', 'articles', 'categories', ['second_category_id'], ['id'])
    # ### end Alembic commands ###
