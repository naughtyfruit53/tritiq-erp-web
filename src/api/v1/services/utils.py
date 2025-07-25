import os

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def get_log_path():
    logs_dir = os.path.join(get_project_root(), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, 'erp_app.log')

def get_static_path(filename):
    static_dir = os.path.join(get_project_root(), 'static')
    os.makedirs(static_dir, exist_ok=True)
    return os.path.join(static_dir, filename)

VOUCHER_COLUMNS = [
    "Voucher Number", "Voucher Date", "Due Date", "Reference Number",
    "Party Name", "Ledger Account", "Item Description", "Item Code",
    "HSN/SAC Code", "Quantity", "Unit of Measure", "Unit Price",
    "Total Amount", "Discount Percentage", "Discount Amount", "Tax Rate",
    "Tax Amount", "CGST Amount", "SGST Amount", "IGST Amount",
    "Cess Amount", "GSTIN", "Narration", "Payment Terms",
    "Shipping Address", "Billing Address", "Place of Supply",
    "Terms and Conditions", "Round Off", "Net Amount", "Freight Charges",
    "Packing Charges", "Insurance Charges", "Batch Number", "Expiry Date",
    "Serial Number", "Warranty Period", "E-Way Bill Number", "Transport Mode",
    "Vehicle Number", "LR/RR Number", "PO Number", "GRN Number",
    "Invoice Number", "Credit Period", "TDS Amount", "TCS Amount",
    "Cost Center", "Project Code", "Currency", "Exchange Rate",
    "Bank Details", "Reverse Charge", "Export Type", "Port Code",
    "Shipping Bill Number", "Country of Origin"
]