from fastapi import APIRouter

api_router = APIRouter()

# Include ERP subrouters (adjust based on your files)
from .erp.users import router as users_router
api_router.include_router(users_router, prefix="/users")

from .erp.company_details import router as company_router
api_router.include_router(company_router, prefix="/company")

from .erp.products import router as products_router
api_router.include_router(products_router, prefix="/products")

from .erp.vendors import router as vendors_router
api_router.include_router(vendors_router, prefix="/vendors")

from .erp.customers import router as customers_router
api_router.include_router(customers_router, prefix="/customers")

from .erp.voucher_types import router as voucher_types_router
api_router.include_router(voucher_types_router, prefix="/voucher_types")

from .erp.voucher_columns import router as voucher_columns_router
api_router.include_router(voucher_columns_router, prefix="/voucher_columns")

from .erp.sales_orders import router as sales_orders_router
api_router.include_router(sales_orders_router, prefix="/sales_orders")

from .erp.sales_invoices import router as sales_invoices_router
api_router.include_router(sales_invoices_router, prefix="/sales_invoices")

from .erp.purchase_orders import router as purchase_orders_router
api_router.include_router(purchase_orders_router, prefix="/purchase_orders")

from .erp.purchase_inv import router as purchase_inv_router
api_router.include_router(purchase_inv_router, prefix="/purchase_inv")

from .erp.quotations import router as quotations_router
api_router.include_router(quotations_router, prefix="/quotations")

from .erp.proforma_invoices import router as proforma_invoices_router
api_router.include_router(proforma_invoices_router, prefix="/proforma_invoices")

from .erp.credit_notes import router as credit_notes_router
api_router.include_router(credit_notes_router, prefix="/credit_notes")

from .erp.pending import router as pending_router
api_router.include_router(pending_router, prefix="/pending")

from .erp.delivery_challan import router as delivery_challan_router
api_router.include_router(delivery_challan_router, prefix="/delivery_challan")

from .erp.grn import router as grn_router
api_router.include_router(grn_router, prefix="/grn")

from .erp.rejections import router as rejections_router
api_router.include_router(rejections_router, prefix="/rejections")

from .erp.stock import router as stock_router
api_router.include_router(stock_router, prefix="/stock")

from .erp.voucher_management import router as voucher_management_router
api_router.include_router(voucher_management_router, prefix="/voucher_management")

from .erp.manufacturing import router as manufacturing_router
api_router.include_router(manufacturing_router, prefix="/manufacturing")

from .erp.backup import router as backup_router
api_router.include_router(backup_router, prefix="/backup")

# Include CRM subrouters
from .crm.leads import router as leads_router
api_router.include_router(leads_router, prefix="/leads")

from .crm.contacts import router as contacts_router
api_router.include_router(contacts_router, prefix="/contacts")

from .crm.tickets import router as tickets_router
api_router.include_router(tickets_router, prefix="/tickets")

from .crm.follow_ups import router as follow_ups_router
api_router.include_router(follow_ups_router, prefix="/follow_ups")