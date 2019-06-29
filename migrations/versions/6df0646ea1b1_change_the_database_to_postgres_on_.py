"""change the database to Postgres on docker

Revision ID: 6df0646ea1b1
Revises: 30cbe9364822
Create Date: 2019-06-26 16:35:19.362050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6df0646ea1b1'
down_revision = '30cbe9364822'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_image_link', sa.String(length=350), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('hash_password', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('date_start', sa.DateTime(), nullable=True),
    sa.Column('date_end', sa.DateTime(), nullable=True),
    sa.Column('level_beg', sa.String(length=6), nullable=True),
    sa.Column('level_end', sa.String(length=6), nullable=True),
    sa.Column('privacy_level', sa.String(length=6), nullable=True),
    sa.Column('post_image_link', sa.String(length=350), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_date_posted'), 'posts', ['date_posted'], unique=False)
    op.create_index(op.f('ix_posts_privacy_level'), 'posts', ['privacy_level'], unique=False)
    op.create_table('post_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'post_id')
    )
    op.create_table('postlinks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link_title', sa.String(length=200), nullable=False),
    sa.Column('link_url', sa.String(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('postviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nbr_views', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('postviews')
    op.drop_table('postlinks')
    op.drop_table('post_tags')
    op.drop_index(op.f('ix_posts_privacy_level'), table_name='posts')
    op.drop_index(op.f('ix_posts_date_posted'), table_name='posts')
    op.drop_table('posts')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('tags')
    # ### end Alembic commands ###