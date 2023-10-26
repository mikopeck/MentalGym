"""Updating models

Revision ID: 33b780396f6e
Revises: c7089d606dfb
Create Date: 2023-10-26 03:23:55.519562

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '33b780396f6e'
down_revision = 'c7089d606dfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_content', sa.String(length=500), nullable=True))
        batch_op.drop_column('current_lesson')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_lesson', mysql.VARCHAR(length=500), nullable=True))
        batch_op.drop_column('current_content')

    # ### end Alembic commands ###
