"""Initial migration - create deliverers table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create deliverers table
    op.create_table(
        'deliverers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('employee_id', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('vehicle_info', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('license_number', sa.String(length=50), nullable=True),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('hire_date', sa.Date(), nullable=True),
        sa.Column('territory', sa.String(length=100), nullable=True),
        sa.Column('is_available', sa.Boolean(), default=True),
        sa.Column('current_location', sa.String(length=100), nullable=True),
        sa.Column('last_location_update', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('idx_deliverers_employee_id', 'deliverers', ['employee_id'], unique=True)
    op.create_index('idx_deliverers_territory', 'deliverers', ['territory'])
    op.create_index('idx_deliverers_available', 'deliverers', ['is_available'])


def downgrade() -> None:
    op.drop_table('deliverers')