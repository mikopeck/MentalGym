"""initial migration

Revision ID: 88a4c978da15
Revises: 
Create Date: 2023-09-17 01:37:24.478444

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '88a4c978da15'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('system_role',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('current_lesson',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=500),
               existing_nullable=True)
        batch_op.drop_column('achievements')
        batch_op.drop_column('actions')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('actions', mysql.VARCHAR(length=500), nullable=True))
        batch_op.add_column(sa.Column('achievements', mysql.VARCHAR(length=500), nullable=True))
        batch_op.alter_column('current_lesson',
               existing_type=sa.String(length=500),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.alter_column('system_role',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###
