"""add_tags_list_column_in_post_table

Revision ID: 0843d433f9f1
Revises: cce5a16aa469
Create Date: 2023-04-10 20:12:42.584953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0843d433f9f1'
down_revision = 'cce5a16aa469'
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.add_column('posts', sa.Column('tags', sa.ARRAY(sa.String()), nullable=True, default='none'),)
    # ### end Alembic commands ###


def downgrade() -> None:
    
    op.drop_column('posts', 'tags')

    # ### end Alembic commands ###
