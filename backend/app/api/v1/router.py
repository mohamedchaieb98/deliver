from fastapi import APIRouter

from app.api.v1.endpoints import (
    clients,
    dashboard,
    deliverers,
    expenses,
    inventory,
    orders,
    payments,
    products,
    resellers,
    routes,
    suppliers,
)

api_router = APIRouter()
# Ici :
# 'prefix' est pour l'URL (/api/v1/clients)
# 'tags' est pour l'affichage Swagger
api_router.include_router(deliverers.router, prefix="/deliverers", tags=["deliverers"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(resellers.router, prefix="/resellers", tags=["resellers"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(routes.router, prefix="/routes", tags=["routes"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
