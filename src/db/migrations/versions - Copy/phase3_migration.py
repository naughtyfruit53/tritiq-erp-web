# src/db/migrations/versions/phase3_erp_stock_manufacturing.py
"""Phase 3 ERP Stock, Manufacturing, Material Flow

Revision ID: phase3
Revises: phase2
Create Date: 2025-07-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'phase3'
down_revision = 'phase2'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('grn',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('po_id', sa.Integer(), nullable=False),
    sa.Column('grn_number', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['po_id'], ['purchase_orders.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('grn_number')
    )
    op.create_table('grn_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('grn_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('po_item_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('accepted_quantity', sa.Float(), nullable=False),
    sa.Column('rejected_quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('total_cost', sa.Float(), nullable=False),
    sa.Column('remarks', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['grn_id'], ['grn.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['po_item_id'], ['po_items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rejections',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('grn_id', sa.Integer(), nullable=False),
    sa.Column('po_item_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['grn_id'], ['grn.id'], ),
    sa.ForeignKeyConstraint(['po_item_id'], ['po_items.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('last_updated', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bom',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('manufactured_product_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['manufactured_product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bom_components',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('bom_id', sa.Integer(), nullable=False),
    sa.Column('component_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['bom_id'], ['bom.id'], ),
    sa.ForeignKeyConstraint(['component_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('work_orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('bom_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.Column('closed_at', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['bom_id'], ['bom.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('material_transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('doc_number', sa.String(), nullable=False),
    sa.Column('delivery_challan_number', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('purpose', sa.String(), nullable=True),
    sa.Column('remarks', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doc_number')
    )

def downgrade():
    op.drop_table('material_transactions')
    op.drop_table('work_orders')
    op.drop_table('bom_components')
    op.drop_table('bom')
    op.drop_table('stock')
    op.drop_table('rejections')
    op.drop_table('grn_items')
    op.drop_table('grn')