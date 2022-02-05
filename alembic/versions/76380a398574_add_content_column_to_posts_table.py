"""add content column to posts table

Revision ID: 76380a398574
Revises: 65f1c81a3e14
Create Date: 2022-02-03 22:52:59.634788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76380a398574'
down_revision = '65f1c81a3e14'
branch_labels = None
depends_on = None


def upgrade():
    # adding new column
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
