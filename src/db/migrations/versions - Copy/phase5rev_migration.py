# src/db/migrations/versions/20250724100000_phase5rev_migration.py
"""Add voucher_instances table

Revision ID: phase5rev
Revises: phase5
Create Date: 2025-07-24 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'phase5rev'
down_revision = 'phase5'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'voucher_instances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('voucher_type_id', sa.Integer(), nullable=False),
        sa.Column('voucher_number', sa.Text(), nullable=False),  # Changed to Text for flexibility
        sa.Column('data_json', sa.Text(), nullable=False),  # Changed to Text for JSON
        sa.Column('module_name', sa.Text(), nullable=False),
        sa.Column('record_id', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['voucher_type_id'], ['voucher_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('voucher_instances')