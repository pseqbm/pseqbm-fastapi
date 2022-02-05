"""create posts table

Revision ID: 65f1c81a3e14
Revises: 
Create Date: 2022-02-03 20:34:21.647876

"""
from alembic import op # op is an object from alembic
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65f1c81a3e14' # alembic_version table keeps track of all revisions and stores this number in a table 
down_revision = None
branch_labels = None
depends_on = None

# runs the commands to make a changes we want # create a logic to create a post table within this function
# upgrade hanles the changes
def upgrade():
    # op access object from alembic
    # sa sqlalchemy object
    op.create_table("posts", 
    sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
    sa.Column("title", sa.String(), nullable=False))
    pass

# downgrade handles rolling it back
# all of the logic to handle removing the table
def downgrade():
    #undoing changes
    op.drop_table("posts")
    pass
