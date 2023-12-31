"""Add Post Model

Revision ID: 6976bf9a1368
Revises: abdb77623f25
Create Date: 2023-09-06 11:02:35.408355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6976bf9a1368'
down_revision = 'abdb77623f25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author', sa.String(length=255), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('mobile', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('mobile', name='user_mobile_key')
    )
    op.drop_table('posts')
    # ### end Alembic commands ###
