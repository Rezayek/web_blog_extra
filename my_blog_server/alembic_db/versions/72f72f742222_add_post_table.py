"""add_post_table

Revision ID: 72f72f742222
Revises: 2f8d9b375145
Create Date: 2023-04-02 01:43:10.955377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72f72f742222'
down_revision = '2f8d9b375145'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('attached_img', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        )
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass

    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('posts')
    pass
    # ### end Alembic commands ###
