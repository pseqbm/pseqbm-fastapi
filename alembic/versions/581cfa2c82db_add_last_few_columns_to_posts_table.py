"""add last few columns to posts table

Revision ID: 581cfa2c82db
Revises: df5cb8f25866
Create Date: 2022-02-03 23:40:15.067297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '581cfa2c82db'
down_revision = 'df5cb8f25866'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("NOW()")),)


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
