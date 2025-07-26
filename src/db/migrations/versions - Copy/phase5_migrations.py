# src/db/migrations/versions/phase5_migrations.py
"""Phase 5 CRM tables

revision = 'phase5'
down_revision = 'phase4'
Create Date: 2025-07-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'phase5'
down_revision = 'phase4'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('leads',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('priority', sa.String(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('follow_ups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('follow_ups')
    op.drop_table('tickets')
    op.drop_table('contacts')
    op.drop_table('leads')