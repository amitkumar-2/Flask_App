"""Initial Migration

Revision ID: 107edea6e9bd
Revises: 
Create Date: 2023-09-01 12:25:06.659051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '107edea6e9bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_color', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('favorite_color')

    # ### end Alembic commands ###
