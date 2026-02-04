from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        "total_orders": 0,
        "delivered_orders": 0,
        "total_revenue": 0.0,
        "pending_orders": 0,
        "active_deliverers": 0,
        "low_stock_products": 0
    }

@router.get("/recent-orders")
def get_recent_orders():
    """Get recent orders for dashboard"""
    return []

@router.get("/low-stock-alerts")
def get_low_stock_alerts():
    """Get low stock alerts"""
    return []