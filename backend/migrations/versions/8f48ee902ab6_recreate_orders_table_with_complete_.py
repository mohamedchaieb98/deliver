"""recreate orders table with complete structure

Revision ID: 8f48ee902ab6
Revises: 4b45faa8dbc5
Create Date: 2026-02-26 14:39:46.851501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f48ee902ab6'
down_revision = '4b45faa8dbc5'
branch_labels = None
depends_on = None


def upgrade():
    # First, let's check if orders table exists and has the right structure
    connection = op.get_bind()
    
    # Drop and recreate orders table with all required fields
    op.drop_table('orders')
    
    op.create_table(
        'orders',
        sa.Column('id', sa.String(36), primary_key=True, index=True),
        sa.Column('order_number', sa.String(20), unique=True, nullable=False),
        sa.Column('client_id', sa.String(36), nullable=True, index=True),
        sa.Column('reseller_id', sa.String(36), nullable=True, index=True),
        sa.Column('deliverer_id', sa.String(36), nullable=True, index=True),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('order_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('delivery_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('delivery_address', sa.String(500), nullable=True),
        sa.Column('total_amount', sa.Numeric(10, 2), nullable=False, default=0),
        sa.Column('notes', sa.String(1000), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKey('resellers.id', name='fk_orders_reseller_id')
    )
    
    # Create customer_order_items table
    op.create_table(
        'customer_order_items',
        sa.Column('id', sa.String(36), primary_key=True, index=True),
        sa.Column('order_id', sa.String(36), sa.ForeignKey('orders.id'), nullable=False, index=True),
        sa.Column('product_name', sa.String(200), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('unit_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('total_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )
    
    # Create indexes
    op.create_index('ix_orders_client_id', 'orders', ['client_id'])
    op.create_index('ix_orders_deliverer_id', 'orders', ['deliverer_id'])
    op.create_index('ix_customer_order_items_order_id', 'customer_order_items', ['order_id'])


def downgrade():
    # Drop indexes
    op.drop_index('ix_customer_order_items_order_id')
    op.drop_index('ix_orders_deliverer_id')
    op.drop_index('ix_orders_client_id')
    
    # Drop tables
    op.drop_table('customer_order_items')
    
    # Recreate old simple orders table
    op.drop_table('orders')
    op.create_table(
        'orders',
        sa.Column('id', sa.String(36), primary_key=True, index=True),
        sa.Column('order_number', sa.String(20), unique=True, nullable=False),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reseller_id', sa.String(36), sa.ForeignKey('resellers.id'), nullable=False, index=True)
    )
