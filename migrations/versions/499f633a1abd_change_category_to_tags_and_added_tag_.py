"""Change category to tags and added Tag table many-to-many relationships

Revision ID: 499f633a1abd
Revises: 75f38c3f555f
Create Date: 2019-06-21 16:53:08.688826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '499f633a1abd'
down_revision = '75f38c3f555f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'post_id')
    )
    op.drop_column('posts', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('category', sa.VARCHAR(), nullable=True))
    op.drop_table('post_tags')
    op.drop_table('tags')
    # ### end Alembic commands ###