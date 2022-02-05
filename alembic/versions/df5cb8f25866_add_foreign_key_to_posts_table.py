"""add foreign key to posts table

Revision ID: df5cb8f25866
Revises: 09dee9cdb843
Create Date: 2022-02-03 23:27:38.706378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df5cb8f25866'
down_revision = '09dee9cdb843'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    # set up relationship between posts and users # foreign key constraint
    # post_user_fk foreign key created
    # source table of the foreign key
    # remote table / referent_table
    # local column local_cols=["owner_id"] we have created above
    # remote_cols=["id"] from the users table
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
