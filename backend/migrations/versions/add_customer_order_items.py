"""Add customer order items table

Revision ID: add_customer_order_items
Revises: 075c477d839b
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'add_customer_order_items'
down_revision = '075c477d839b'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to orders table with proper SQLite handling
    op.add_column('orders', sa.Column('client_id', sa.String(36), nullable=True))
    op.add_column('orders', sa.Column('deliverer_id', sa.String(36), nullable=True))
    op.add_column('orders', sa.Column('order_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('orders', sa.Column('delivery_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('orders', sa.Column('delivery_address', sa.String(500), nullable=True))
    op.add_column('orders', sa.Column('total_amount', sa.Numeric(10, 2), nullable=True))
    op.add_column('orders', sa.Column('notes', sa.String(1000), nullable=True))
    
    # Update existing records with default values
    connection = op.get_bind()
    connection.execute(sa.text("UPDATE orders SET total_amount = 0 WHERE total_amount IS NULL"))
    connection.execute(sa.text("UPDATE orders SET order_date = datetime('now') WHERE order_date IS NULL"))
    
    # Now make total_amount NOT NULL
    op.alter_column('orders', 'total_amount', nullable=False)
    
    # Modify reseller_id to be nullable
    op.alter_column('orders', 'reseller_id', nullable=True)
    
    # Create indexes
    op.create_index('ix_orders_client_id', 'orders', ['client_id'])
    op.create_index('ix_orders_deliverer_id', 'orders', ['deliverer_id'])
    
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
    
    # Create indexes for customer_order_items
    op.create_index('ix_customer_order_items_order_id', 'customer_order_items', ['order_id'])


def downgrade():
    # Drop customer_order_items table
    op.drop_index('ix_customer_order_items_order_id')
    op.drop_table('customer_order_items')
    
    # Drop indexes
    op.drop_index('ix_orders_client_id')
    op.drop_index('ix_orders_deliverer_id')
    
    # Remove columns from orders table
    op.drop_column('orders', 'notes')
    op.drop_column('orders', 'total_amount')
    op.drop_column('orders', 'delivery_address')
    op.drop_column('orders', 'delivery_date')
    op.drop_column('orders', 'order_date')
    op.drop_column('orders', 'deliverer_id')
    op.drop_column('orders', 'client_id')
    
    # Make reseller_id not nullable again
    op.alter_column('orders', 'reseller_id', nullable=False)