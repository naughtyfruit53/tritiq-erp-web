# src/db/models/base.py
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Import all models to ensure they're discovered by Alembic
from . import (
    users, company_details, customers, vendors, products,
    sales_orders, sales_order_items, sales_invoices, sales_inv_items,
    purchase_orders, po_items, purchase_inv, purchase_inv_items,
    quotations, quotation_form, proforma_invoice, proforma_invoice_items,
    credit_notes, cn_items, delivery_challans, delivery_challan_items,
    grn, grn_items, rejections, stock, bom, bom_components,
    work_orders, material_transactions, voucher_types, voucher_instances,
    voucher_columns, doc_sequences, audit_log, crm
)