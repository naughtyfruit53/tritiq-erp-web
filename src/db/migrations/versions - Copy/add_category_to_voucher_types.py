"""add_category_to_voucher_types

Revision ID: add_category_001
Revises: a63b525c453b_phase6_initial_vouchers
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_category_001'
down_revision = 'a63b525c453b_phase6_initial_vouchers'
branch_labels = None
depends_on = None


def upgrade():
    # Add category column to voucher_types table
    op.add_column('voucher_types', sa.Column('category', sa.String(), nullable=False, server_default='internal'))
    
    # Update existing voucher types with appropriate categories based on module_name
    connection = op.get_bind()
    
    # Update sales voucher types
    connection.execute(
        sa.text("UPDATE voucher_types SET category = 'sales' WHERE module_name IN ('sales_order', 'sales_inv', 'quotation', 'proforma_invoice', 'delivery_challan')")
    )
    
    # Update purchase voucher types  
    connection.execute(
        sa.text("UPDATE voucher_types SET category = 'purchase' WHERE module_name IN ('purchase_order', 'purchase_inv', 'grn', 'rejection')")
    )
    
    # Update financial voucher types
    connection.execute(
        sa.text("UPDATE voucher_types SET category = 'financial' WHERE module_name IN ('credit_note', 'receipt', 'payment', 'contra', 'journal', 'debit_note')")
    )
    
    # All others remain 'internal' (default)


def downgrade():
    # Remove category column from voucher_types table
    op.drop_column('voucher_types', 'category')