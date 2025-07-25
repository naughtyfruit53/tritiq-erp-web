import os
import logging
import json
import re
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.company_details import CompanyDetail  # Assume import; adjust to ..db.models.company_details
# Removed: from src.config import get_db_path, get_log_path

logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'app.log'), level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

UNITS: List[str] = [
    "pcs", "g", "kg", "m", "l", "ml",
    "cm", "mm", "sqm", "cft", "unit"
]

STATES: List[Tuple[str, str]] = [
    ("Andaman and Nicobar Islands", "35"), ("Andhra Pradesh", "37"),
    ("Arunachal Pradesh", "12"), ("Assam", "18"),
    ("Bihar", "10"), ("Chandigarh", "04"),
    ("Chhattisgarh", "22"), ("Dadra and Nagar Haveli", "26"),
    ("Daman and Diu", "25"), ("Delhi", "07"),
    ("Goa", "30"), ("Gujarat", "24"),
    ("Haryana", "06"), ("Himachal Pradesh", "02"),
    ("Jammu and Kashmir", "01"), ("Jharkhand", "20"),
    ("Karnataka", "29"), ("Kerala", "32"),
    ("Lakshadweep", "31"), ("Madhya Pradesh", "23"),
    ("Maharashtra", "27"), ("Manipur", "14"),
    ("Meghalaya", "17"), ("Mizoram", "15"),
    ("Nagaland", "13"), ("Odisha", "21"),
    ("Puducherry", "34"), ("Punjab", "03"),
    ("Rajasthan", "08"), ("Sikkim", "11"),
    ("Tamil Nadu", "33"), ("Telangana", "36"),
    ("Tripura", "16"), ("Uttar Pradesh", "09"),
    ("Uttarakhand", "05"), ("West Bengal", "19")
]

VENDOR_COLUMNS: List[str] = [
    "Name", "Contact No", "Address Line 1", "Address Line 2",
    "City", "State", "State Code", "PIN Code",
    "GST No", "PAN No", "Email"
]

CUSTOMER_COLUMNS: List[str] = [
    "Name", "Contact No", "Address Line 1", "Address Line 2",
    "City", "State", "State Code", "PIN Code",
    "GST No", "PAN No", "Email"
]

PRODUCT_COLUMNS = [
    ("Name", "TEXT", True, 1, False, None),
    ("HSN Code", "TEXT", False, 2, False, None),
    ("Qty", "REAL", True, 3, False, None),
    ("Unit", "TEXT", True, 4, False, None),
    ("Unit Price", "REAL", True, 5, False, None),
    ("GST Rate", "REAL", False, 6, False, None),
    ("Amount", "REAL", True, 7, True, json.dumps({"type": "net_amount", "inputs": ["Unit Price", "Qty"], "output": "Amount"}))
]

PRODUCT_VOUCHER_COLUMNS = [
    "Discount Amount", "Tax Amount", "GST Rate", "CGST Amount", "SGST Amount",
    "IGST Amount", "Batch Number", "TDS Amount", "Freight Charges", "E-Way Bill Number",
    "Serial Number", "Expiry Date"
]

VOUCHER_COLUMNS = [
    "Voucher Number", "Voucher Date", "Due Date", "Reference Number", "Party Name",
    "Ledger Account", "Item Description", "Item Code", "HSN/SAC Code", "Quantity",
    "Unit of Measure", "Unit Price", "Total Amount", "Discount Percentage", "Discount Amount",
    "Tax Rate", "Tax Amount", "CGST Amount", "SGST Amount", "IGST Amount", "Cess Amount",
    "GSTIN", "Narration", "Payment Terms", "Shipping Address", "Billing Address",
    "Place of Supply", "Terms and Conditions", "Round Off", "Net Amount", "Freight Charges",
    "Packing Charges", "Insurance Charges", "Batch Number", "Expiry Date", "Serial Number",
    "Warranty Period", "E-Way Bill Number", "Transport Mode", "Vehicle Number", "LR/RR Number",
    "PO Number", "GRN Number", "Invoice Number", "Credit Period", "TDS Amount", "TCS Amount",
    "Cost Center", "Project Code", "Currency", "Exchange Rate", "Bank Details", "Reverse Charge",
    "Export Type", "Port Code", "Shipping Bill Number", "Country of Origin"
]

LEDGER_COLUMNS = [
    "Ledger Name", "Ledger Group", "Opening Balance", "Address", "City", "State",
    "State Code", "PIN Code", "GSTIN", "PAN Number", "Contact Number", "Email",
    "Bank Account Number", "IFSC Code", "Bank Name", "Credit Limit", "Credit Period",
    "Tax Type", "MSME Registration", "LUT Number", "Vendor Code", "Customer Code",
    "Taxable Amount", "Discount Percentage", "Discount Amount", "CGST Amount",
    "SGST Amount", "IGST Amount", "Cess Amount", "Total Amount", "Round Off",
    "Net Amount", "Narration", "Terms of Payment", "Delivery Terms", "Freight Charges",
    "Insurance Charges", "Place of Supply", "Reverse Charge Applicable", "E-Way Bill Number",
    "Transport Mode", "Vehicle Number", "LR/RR Number", "Project Code", "Cost Center",
    "Due Date", "TDS Amount", "TCS Amount", "Invoice Number", "Reference Number",
    "Payment Status", "Tax Rate", "HSN/SAC Code", "Item Description", "Quantity",
    "Unit of Measure", "Unit Price"
]

PREDEFINED_COLUMNS = [
    "Sales Invoice Number", "Invoice Number", "Invoice Date", "Sales Order Number",
    "Customer Name", "Total Amount", "CGST Amount", "SGST Amount", "IGST Amount"
]

VOUCHER_TYPES = [
    "Payment Voucher", "Receipt Voucher", "Journal Voucher", "Contra Voucher",
    "Bank Reconciliation Voucher", "Petty Cash Voucher", "Advance Payment Voucher",
    "Refund Voucher", "Sales Invoice", "Export Invoice", "Sales Return Voucher",
    "Proforma Invoice", "Delivery Note", "Sales Order Voucher", "Tax-Free Sales Voucher",
    "Purchase Invoice", "Import Invoice", "Purchase Return Voucher", "Purchase Order Voucher",
    "Goods Receipt Note", "Reverse Charge Voucher", "Stock Journal Voucher",
    "Physical Stock Voucher", "Material Issue Voucher", "Material Receipt Voucher",
    "Stock Transfer Voucher", "Damaged Stock Voucher", "Credit Note Voucher",
    "Debit Note Voucher", "GST Adjustment Voucher", "E-Way Bill Voucher",
    "Input Tax Credit Voucher", "Production Voucher", "Bill of Materials Voucher",
    "Work-in-Progress Voucher", "Scrap Voucher", "Salary Voucher", "Bonus Voucher",
    "Expense Reimbursement Voucher", "PF/ESIC Contribution Voucher",
    "Foreign Exchange Voucher", "Exchange Gain/Loss Voucher", "Fixed Asset Voucher",
    "Depreciation Voucher", "Loan Voucher", "Interest Voucher", "Budget Voucher",
    "Cost Center Voucher", "Custom Voucher"
]

MODULE_VOUCHER_TYPES = {
    "purchase_inv": ["Purchase Invoice", "Import Invoice", "Purchase Return Voucher", "Goods Receipt Note"],
    "sales_inv": ["Sales Invoice", "Export Invoice", "Sales Return Voucher", "Proforma Invoice"],
    "payment": ["Payment Voucher", "Advance Payment Voucher"],
    "receipt": ["Receipt Voucher", "Refund Voucher"],
    "journal": ["Journal Voucher", "GST Adjustment Voucher"],
    "stock": ["Stock Journal Voucher", "Stock Transfer Voucher", "Damaged Stock Voucher"],
    "general": ["Contra Voucher", "Credit Note Voucher", "Debit Note Voucher"]
}

def number_to_words(num: float) -> str:
    """Convert a number to words (for amounts up to 100 crore)."""
    try:
        num = float(num)
        if num < 0:
            logger.warning(f"Negative number provided to number_to_words: {num}")
            return "Negative Amount"
        if num == 0:
            return "Zero"

        units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        thousands = ["", "Thousand", "Lakh", "Crore"]

        def convert_less_than_thousand(n: int) -> str:
            if n == 0:
                return ""
            elif n < 10:
                return units[n]
            elif n < 20:
                return teens[n - 10]
            elif n < 100:
                return tens[n // 10] + (" " + units[n % 10] if n % 10 else "")
            else:
                return units[n // 100] + " Hundred" + (" " + convert_less_than_thousand(n % 100) if n % 100 else "")

        parts = []
        i = 0
        whole = int(num)
        while whole > 0:
            if whole % 1000 != 0:
                part = convert_less_than_thousand(whole % 1000)
                if i > 0:
                    part += " " + thousands[i]
                parts.append(part)
            whole //= 1000
            i += 1

        words = " ".join(reversed(parts)).strip() or "Zero"

        decimal = round((num - int(num)) * 100)
        if decimal > 0:
            words += " and " + convert_less_than_thousand(decimal) + " Paise"

        return words + " Only"

    except ValueError as e:
        logger.error(f"Error converting number to words: {e}")
        return "Invalid Amount"

def update_state_code(state: str) -> str:
    """Update state code based on selected state."""
    try:
        for s, code in STATES:
            if s.lower() == state.lower():
                return code
        return ""
    except Exception as e:
        logger.error(f"Error updating state code: {e}")
        return ""

def add_unit(unit: str):
    """Add a new unit to the UNITS list if it doesn't exist."""
    try:
        global UNITS
        unit = unit.strip().lower()
        if unit and unit not in UNITS:
            UNITS.append(unit)
            logger.info(f"Added unit: {unit}")
    except Exception as e:
        logger.error(f"Error adding unit: {e}")

async def get_default_directory(db: AsyncSession) -> str:
    """Fetch the default directory from company details."""
    try:
        result = await db.execute(select(CompanyDetails.default_directory).where(CompanyDetails.id == 1))
        result = result.scalar_one_or_none()
        return result if result else os.path.expanduser("~/Documents/ERP")
    except Exception as e:
        logger.error(f"Error fetching default directory: {e}")
        return os.path.expanduser("~/Documents/ERP")

def create_module_directory(module_name: str) -> str:
    """Create a directory for the specified module under the default directory."""
    try:
        default_dir = os.path.expanduser("~/Documents/ERP")  # Sync version; for async, pass db and await get_default_directory
        if not default_dir:
            raise ValueError("Default directory not set")
        module_dir = os.path.join(default_dir, module_name.replace(" ", "_"))
        os.makedirs(module_dir, exist_ok=True)
        logger.debug(f"Created module directory: {module_dir}")
        return module_dir
    except (OSError, ValueError) as e:
        logger.error(f"Error creating module directory {module_name}: {e}")
        return None

async def fetch_company_name(db: AsyncSession) -> str:
    """Fetch the company name from the database."""
    try:
        result = await db.execute(select(CompanyDetails.company_name).where(CompanyDetails.id == 1))
        result = result.scalar_one_or_none()
        return result if result else "Your Company"
    except Exception as e:
        logger.error(f"Error fetching company name: {e}")
        return "Your Company"