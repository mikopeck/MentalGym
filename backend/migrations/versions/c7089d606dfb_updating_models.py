"""Updating models

Revision ID: c7089d606dfb
Revises: 8519fd8702cc
Create Date: 2023-10-12 19:13:47.082515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7089d606dfb'
down_revision = '8519fd8702cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.add_column(sa.Column('system_role', sa.String(length=100), nullable=True))

    with op.batch_alter_table('user_action', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lesson_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'lesson', ['lesson_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_action', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('lesson_id')

    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.drop_column('system_role')

    # ### end Alembic commands ###
