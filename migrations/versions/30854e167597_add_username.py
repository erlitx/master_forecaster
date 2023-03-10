"""Add username

Revision ID: 30854e167597
Revises: 5e9775abe164
Create Date: 2023-02-22 15:39:51.282278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30854e167597'
down_revision = '5e9775abe164'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=20), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
