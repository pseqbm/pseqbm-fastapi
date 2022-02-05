"""add user table

Revision ID: 09dee9cdb843
Revises: 76380a398574
Create Date: 2022-02-03 23:12:51.245619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09dee9cdb843'
down_revision = '76380a398574'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
        )
    pass


def downgrade():
    op.drop_table("users")
    pass
