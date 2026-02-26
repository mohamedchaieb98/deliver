"""merge heads

Revision ID: 4b45faa8dbc5
Revises: 9ee19dbda1cb, add_customer_order_items
Create Date: 2026-02-26 14:33:20.608325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b45faa8dbc5'
down_revision = ('9ee19dbda1cb', 'add_customer_order_items')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
