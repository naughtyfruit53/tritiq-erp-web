# src/api/v1/erp/__init__.py
from fastapi import APIRouter

erp_router = APIRouter()

# Add all ERP routers
from .users import router as users_router
erp_router.include_router(users_router, prefix="/users")

from .company_details import router as company_router
erp_router.include_router(company_router, prefix="/company")

from .products import router as products_router
erp_router.include_router(products_router, prefix="/products")

from .vendors import router as vendors_router
erp_router.include_router(vendors_router, prefix="/vendors")

from .customers import router as customers_router
erp_router.include_router(customers_router, prefix="/customers")

from .voucher_types import router as voucher_types_router
erp_router.include_router(voucher_types_router, prefix="/voucher_types")

from .voucher_columns import router as voucher_columns_router
erp_router.include_router(voucher_columns_router, prefix="/voucher_columns")

from .sales_orders import router as sales_orders_router
erp_router.include_router(sales_orders_router, prefix="/sales_orders")

from .sales_invoices import router as sales_invoices_router
erp_router.include_router(sales_invoices_router, prefix="/sales_invoices")

from .purchase_orders import router as purchase_orders_router
erp_router.include_router(purchase_orders_router, prefix="/purchase_orders")

from .purchase_inv import router as purchase_inv_router
erp_router.include_router(purchase_inv_router, prefix="/purchase_inv")

from .quotations import router as quotations_router
erp_router.include_router(quotations_router, prefix="/quotations")

from .proforma_invoices import router as proforma_invoices_router
erp_router.include_router(proforma_invoices_router, prefix="/proforma_invoices")

from .credit_notes import router as credit_notes_router
erp_router.include_router(credit_notes_router, prefix="/credit_notes")

from .pending import router as pending_router
erp_router.include_router(pending_router, prefix="/pending")

from .delivery_challan import router as delivery_challan_router
erp_router.include_router(delivery_challan_router, prefix="/delivery_challan")

from .grn import router as grn_router
erp_router.include_router(grn_router, prefix="/grn")

from .rejections import router as rejections_router
erp_router.include_router(rejections_router, prefix="/rejections")

from .stock import router as stock_router
erp_router.include_router(stock_router, prefix="/stock")

from .voucher_management import router as voucher_management_router
erp_router.include_router(voucher_management_router, prefix="/voucher_management")

from .manufacturing import router as manufacturing_router
erp_router.include_router(manufacturing_router, prefix="/manufacturing")

from .backup import router as backup_router
erp_router.include_router(backup_router, prefix="/backup")