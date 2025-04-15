"""merge multiple heads

Revision ID: 3c9698d217c2
Revises: 1a31ce608336, add_workflow_tables
Create Date: 2025-04-15 17:25:55.615042

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '3c9698d217c2'
down_revision = ('1a31ce608336', 'add_workflow_tables')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
