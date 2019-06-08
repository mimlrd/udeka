"""Corrected the database added self.user_id in post, date_posted, indexes, etc

Revision ID: 5fc1dea03270
Revises: 014f2e27ab06
Create Date: 2019-05-30 12:04:10.203867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fc1dea03270'
down_revision = '014f2e27ab06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('date_posted', sa.DateTime(), nullable=False))
    op.add_column('posts', sa.Column('post_image_link', sa.String(length=350), nullable=True))
    op.create_index(op.f('ix_posts_date_posted'), 'posts', ['date_posted'], unique=False)
    op.add_column('users', sa.Column('profile_image_link', sa.String(length=350), nullable=True))
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_column('users', 'profile_image_link')
    op.drop_index(op.f('ix_posts_date_posted'), table_name='posts')
    op.drop_column('posts', 'post_image_link')
    op.drop_column('posts', 'date_posted')
    # ### end Alembic commands ###