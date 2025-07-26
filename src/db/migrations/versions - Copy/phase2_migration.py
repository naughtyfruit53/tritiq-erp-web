# Revised src/db/migrations/versions/phase2_migration.py
"""Phase 2 migration

Revision ID: phase2
Revises: initial
Create Date: 2025-07-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'phase2'
down_revision = 'initial'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('sales_orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sales_order_number', sa.String(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('sales_order_date', sa.String(), nullable=False),
    sa.Column('delivery_date', sa.String(), nullable=True),
    sa.Column('payment_terms', sa.String(), nullable=True),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('cgst_amount', sa.Float(), nullable=True),
    sa.Column('sgst_amount', sa.Float(), nullable=True),
    sa.Column('igst_amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('updated_at', sa.String(), nullable=True),
    sa.Column('is_deleted', sa.Integer(), nullable=True),
    sa.Column('voucher_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['voucher_type_id'], ['voucher_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sales_order_number')
    )
    op.create_table('sales_order_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sales_order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('gst_rate', sa.Float(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['sales_order_id'], ['sales_orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sales_invoices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sales_inv_number', sa.String(), nullable=False),
    sa.Column('invoice_date', sa.String(), nullable=False),
    sa.Column('sales_order_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('cgst_amount', sa.Float(), nullable=True),
    sa.Column('sgst_amount', sa.Float(), nullable=True),
    sa.Column('igst_amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('voucher_type_id', sa.Integer(), nullable=True),
    sa.Column('voucher_data', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['sales_order_id'], ['sales_orders.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['voucher_type_id'], ['voucher_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sales_inv_number')
    )
    op.create_table('sales_inv_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sales_inv_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('gst_rate', sa.Float(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['sales_inv_id'], ['sales_invoices.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchase_orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('po_number', sa.String(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('po_date', sa.String(), nullable=False),
    sa.Column('delivery_date', sa.String(), nullable=True),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('cgst_amount', sa.Float(), nullable=True),
    sa.Column('sgst_amount', sa.Float(), nullable=True),
    sa.Column('igst_amount', sa.Float(), nullable=True),
    sa.Column('payment_terms', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('updated_at', sa.String(), nullable=True),
    sa.Column('is_deleted', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('po_number')
    )
    op.create_table('po_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('po_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('gst_rate', sa.Float(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['po_id'], ['purchase_orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchase_inv',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pur_inv_number', sa.String(), nullable=False),
    sa.Column('invoice_number', sa.String(), nullable=True),
    sa.Column('invoice_date', sa.String(), nullable=True),
    sa.Column('grn_id', sa.Integer(), nullable=True),
    sa.Column('po_id', sa.Integer(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('pur_inv_date', sa.String(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('cgst_amount', sa.Float(), nullable=True),
    sa.Column('sgst_amount', sa.Float(), nullable=True),
    sa.Column('igst_amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('voucher_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['po_id'], ['purchase_orders.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.ForeignKeyConstraint(['voucher_type_id'], ['voucher_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pur_inv_number')
    )
    op.create_table('purchase_inv_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('purchase_inv_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('gst_rate', sa.Float(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['purchase_inv_id'], ['purchase_inv.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quotes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quotation_number', sa.String(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('quotation_date', sa.String(), nullable=False),
    sa.Column('validity_date', sa.String(), nullable=True),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('cgst_amount', sa.Float(), nullable=True),
    sa.Column('sgst_amount', sa.Float(), nullable=True),
    sa.Column('igst_amount', sa.Float(), nullable=True),
    sa.Column('payment_terms', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('updated_at', sa.String(), nullable=True),
    sa.Column('is_deleted', sa.Integer(), nullable=True),
    sa.Column('voucher_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['voucher_type_id'], ['voucher_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('quotation_number')
    )
    op.create_table('quote_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quote_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('gst_rate', sa.Float(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['quote_id'], ['quotes.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proforma_invoices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('proforma_number', sa.String(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('proforma_date', sa.String(), nullable=False),
    sa.Column('validity_date', sa.String(), nullable=True),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('cgst_amount', sa.Float(), nullable=True),
    sa.Column('sgst_amount', sa.Float(), nullable=True),
    sa.Column('igst_amount', sa.Float(), nullable=True),
    sa.Column('payment_terms', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('updated_at', sa.String(), nullable=True),
    sa.Column('is_deleted', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('proforma_number')
    )
    op.create_table('proforma_invoice_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('proforma_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('gst_rate', sa.Float(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['proforma_id'], ['proforma_invoices.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('credit_notes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cn_number', sa.String(), nullable=False),
    sa.Column('grn_id', sa.Integer(), nullable=False),
    sa.Column('po_id', sa.Integer(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('cn_date', sa.String(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('cgst_amount', sa.Float(), nullable=True),
    sa.Column('sgst_amount', sa.Float(), nullable=True),
    sa.Column('igst_amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('voucher_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grn_id'], ['grn.id'], ),
    sa.ForeignKeyConstraint(['po_id'], ['purchase_orders.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.ForeignKeyConstraint(['voucher_type_id'], ['voucher_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cn_number')
    )
    op.create_table('cn_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cn_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('gst_rate', sa.Float(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['cn_id'], ['credit_notes.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pending',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('po_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['po_id'], ['purchase_orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('pending')
    op.drop_table('cn_items')
    op.drop_table('credit_notes')
    op.drop_table('proforma_invoice_items')
    op.drop_table('proforma_invoices')
    op.drop_table('quote_items')
    op.drop_table('quotes')
    op.drop_table('purchase_inv_items')
    op.drop_table('purchase_inv')
    op.drop_table('po_items')
    op.drop_table('purchase_orders')
    op.drop_table('sales_inv_items')
    op.drop_table('sales_invoices')
    op.drop_table('sales_order_items')
    op.drop_table('sales_orders')