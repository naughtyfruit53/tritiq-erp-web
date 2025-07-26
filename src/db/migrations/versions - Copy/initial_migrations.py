# src/db/migrations/versions/initial_migration.py
"""Initial migration

Revision ID: initial
Revises: 
Create Date: 2025-07-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('must_change_password', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    # Create company_details table
    op.create_table('company_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('address1', sa.String(), nullable=False),
        sa.Column('address2', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('pin', sa.String(), nullable=False),
        sa.Column('state_code', sa.String(), nullable=False),
        sa.Column('gst_no', sa.String(), nullable=True),
        sa.Column('pan_no', sa.String(), nullable=True),
        sa.Column('contact_no', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('logo_path', sa.String(), nullable=True),
        sa.Column('default_directory', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # Create products table
    op.create_table('products',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('hsn_code', sa.String(), nullable=True),
        sa.Column('unit', sa.String(), nullable=False),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('gst_rate', sa.Float(), nullable=False),
        sa.Column('is_gst_inclusive', sa.String(), nullable=False),
        sa.Column('reorder_level', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('is_manufactured', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    # Create vendors table
    op.create_table('vendors',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('contact_no', sa.String(), nullable=False),
        sa.Column('address1', sa.String(), nullable=False),
        sa.Column('address2', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('pin', sa.String(), nullable=False),
        sa.Column('state_code', sa.String(), nullable=False),
        sa.Column('gst_no', sa.String(), nullable=True),
        sa.Column('pan_no', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    # Create customers table
    op.create_table('customers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('contact_no', sa.String(), nullable=False),
        sa.Column('address1', sa.String(), nullable=False),
        sa.Column('address2', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('state_code', sa.String(), nullable=False),
        sa.Column('pin', sa.String(), nullable=False),
        sa.Column('gst_no', sa.String(), nullable=True),
        sa.Column('pan_no', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    # Create voucher_types table
    op.create_table('voucher_types',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('is_default', sa.Boolean(), nullable=False),
        sa.Column('module_name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    # Create voucher_columns table
    op.create_table('voucher_columns',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('voucher_type_id', sa.Integer(), nullable=False),
        sa.Column('column_name', sa.String(), nullable=False),
        sa.Column('data_type', sa.String(), nullable=False),
        sa.Column('is_mandatory', sa.Boolean(), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('is_calculated', sa.Boolean(), nullable=False),
        sa.Column('calculation_logic', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['voucher_type_id'], ['voucher_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('voucher_columns')
    op.drop_table('voucher_types')
    op.drop_table('customers')
    op.drop_table('vendors')
    op.drop_table('products')
    op.drop_table('company_details')
    op.drop_table('users')