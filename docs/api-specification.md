# API Specification - Water Delivery Management System (No Authentication)

## API Overview

- **Framework**: FastAPI
- **Base URL**: `https://api.waterdelivery.com/v1`
- **Authentication**: None (Internal use only)
- **Content Type**: `application/json`
- **Documentation**: Auto-generated via FastAPI (Swagger/OpenAPI)

## Core API Endpoints

### Deliverers Management

#### Get All Deliverers
```http
GET /deliverers?active=true&territory=

Response:
{
  "deliverers": [
    {
      "id": "uuid",
      "name": "Mike Driver",
      "employee_id": "EMP001",
      "phone_number": "+1234567890",
      "territory": "Downtown",
      "is_available": true,
      "vehicle_info": {
        "make": "Ford",
        "model": "Transit",
        "year": 2022,
        "plate_number": "ABC-123"
      }
    }
  ]
}
```

### Clients Management

#### Get All Clients
```http
GET /clients?page=1&limit=20&search=&active=true

Response:
{
  "items": [
    {
      "id": "uuid",
      "name": "John Doe",
      "business_name": "ABC Corp",
      "email": "john@abc.com",
      "phone_number": "+1234567890",
      "address": "123 Main St, City",
      "client_type": "business",
      "outstanding_balance": 150.00,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

#### Create Client
```http
POST /clients
Content-Type: application/json

{
  "name": "John Doe",
  "business_name": "ABC Corp",
  "email": "john@abc.com",
  "phone_number": "+1234567890",
  "address": "123 Main St, City",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "client_type": "business",
  "payment_terms": "credit_30",
  "credit_limit": 1000.00,
  "notes": "Important client"
}

Response: 201
{
  "id": "uuid",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Update Client
```http
PUT /clients/{client_id}

{
  "name": "John Doe Updated",
  "credit_limit": 1500.00
}

Response: 200
```

#### Delete Client
```http
DELETE /clients/{client_id}

Response: 204 No Content
```

### Products & Inventory Management

#### Get All Products
```http
GET /products?category=&active=true&low_stock=false

Response:
{
  "items": [
    {
      "id": "uuid",
      "name": "Premium Water 500ml",
      "category": "bottled_water",
      "size": "500ml",
      "unit_price": 1.50,
      "cost": 0.80,
      "supplier": {
        "id": "uuid",
        "name": "Pure Water Co."
      },
      "inventory": {
        "current_stock": 500,
        "minimum_stock": 100,
        "is_low_stock": false
      },
      "is_active": true
    }
  ],
  "total": 25
}
```

#### Create Product
```http
POST /products

{
  "name": "Premium Water 500ml",
  "description": "Pure spring water",
  "category": "bottled_water",
  "size": "500ml",
  "unit_price": 1.50,
  "cost": 0.80,
  "supplier_id": "uuid"
}

Response: 201
```

#### Update Inventory
```http
POST /inventory/{product_id}/adjust

{
  "quantity_change": 100,
  "movement_type": "restock",
  "notes": "Weekly restock"
}

Response: 200
{
  "product_id": "uuid",
  "new_stock": 600,
  "movement_id": "uuid"
}
```

### Order Management

#### Get All Orders
```http
GET /orders?status=&deliverer_id=&date_from=&date_to=&page=1&limit=20

Response:
{
  "items": [
    {
      "id": "uuid",
      "order_number": "ORD-2024-001",
      "client": {
        "id": "uuid",
        "name": "John Doe",
        "address": "123 Main St"
      },
      "deliverer": {
        "id": "uuid",
        "name": "Mike Driver"
      },
      "status": "pending",
      "total_amount": 45.00,
      "payment_status": "pending",
      "order_date": "2024-01-01T10:00:00Z",
      "requested_delivery_date": "2024-01-01",
      "items": [
        {
          "product_name": "Premium Water 500ml",
          "quantity": 30,
          "unit_price": 1.50
        }
      ]
    }
  ],
  "total": 150
}
```

#### Create Order
```http
POST /orders

{
  "client_id": "uuid",
  "requested_delivery_date": "2024-01-02",
  "delivery_address": "123 Main St, City",
  "delivery_latitude": 40.7128,
  "delivery_longitude": -74.0060,
  "items": [
    {
      "product_id": "uuid",
      "quantity": 30,
      "unit_price": 1.50
    }
  ],
  "notes": "Deliver to back door"
}

Response: 201
{
  "id": "uuid",
  "order_number": "ORD-2024-001",
  "total_amount": 45.00
}
```

#### Assign Order to Deliverer
```http
POST /orders/{order_id}/assign

{
  "deliverer_id": "uuid",
  "route_date": "2024-01-02"
}

Response: 200
```

### Route Management

#### Get All Routes
```http
GET /routes?deliverer_id=&date=2024-01-02&status=

Response:
{
  "items": [
    {
      "id": "uuid",
      "route_name": "Route A - Downtown",
      "deliverer": {
        "id": "uuid",
        "name": "Mike Driver"
      },
      "route_date": "2024-01-02",
      "status": "in_progress",
      "total_stops": 8,
      "completed_stops": 3,
      "estimated_duration": 480,
      "stops": [
        {
          "id": "uuid",
          "stop_number": 1,
          "order": {
            "id": "uuid",
            "order_number": "ORD-2024-001",
            "client_name": "John Doe"
          },
          "address": "123 Main St",
          "status": "completed",
          "estimated_arrival": "2024-01-02T09:00:00Z",
          "actual_arrival": "2024-01-02T09:05:00Z"
        }
      ]
    }
  ]
}
```

#### Create Route
```http
POST /routes

{
  "route_name": "Route A - Downtown",
  "deliverer_id": "uuid",
  "route_date": "2024-01-02",
  "order_ids": ["uuid1", "uuid2", "uuid3"]
}

Response: 201
```

#### Optimize Route
```http
POST /routes/{route_id}/optimize

Response: 200
{
  "optimized_distance": 25.5,
  "estimated_duration": 420,
  "stops": [
    {
      "stop_number": 1,
      "order_id": "uuid",
      "estimated_arrival": "2024-01-02T09:00:00Z"
    }
  ]
}
```

### Analytics & Reports

#### Dashboard Statistics
```http
GET /dashboard/stats?date_from=2024-01-01&date_to=2024-01-31

Response:
{
  "total_orders": 500,
  "delivered_orders": 475,
  "total_revenue": 12500.00,
  "pending_orders": 25,
  "active_deliverers": 5,
  "low_stock_products": 3,
  "outstanding_payments": 2500.00,
  "daily_stats": [
    {
      "date": "2024-01-01",
      "orders": 15,
      "revenue": 375.00,
      "deliveries": 14
    }
  ]
}
```

#### Financial Report
```http
GET /reports/financial?date_from=2024-01-01&date_to=2024-01-31

Response:
{
  "total_revenue": 12500.00,
  "total_expenses": 3200.00,
  "gross_profit": 9300.00,
  "profit_margin": 74.4,
  "revenue_by_product": [
    {
      "product_name": "Premium Water 500ml",
      "revenue": 8500.00,
      "units_sold": 5667
    }
  ],
  "expenses_by_category": [
    {
      "category": "Fuel",
      "amount": 1500.00
    }
  ]
}
```

## Mobile API Endpoints (Deliverers)

### Route Management

#### Get Deliverer Route
```http
GET /deliverers/{deliverer_id}/routes/today

Response:
{
  "id": "uuid",
  "route_name": "Route A - Downtown",
  "route_date": "2024-01-02",
  "status": "planned",
  "total_stops": 8,
  "completed_stops": 0,
  "current_stop": 1,
  "stops": [
    {
      "id": "uuid",
      "stop_number": 1,
      "order": {
        "id": "uuid",
        "order_number": "ORD-2024-001",
        "client": {
          "name": "John Doe",
          "phone_number": "+1234567890"
        },
        "items": [
          {
            "product_name": "Premium Water 500ml",
            "quantity": 30
          }
        ],
        "total_amount": 45.00,
        "payment_status": "pending"
      },
      "address": "123 Main St, City",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "estimated_arrival": "2024-01-02T09:00:00Z",
      "status": "pending",
      "special_instructions": "Deliver to back door"
    }
  ]
}
```

#### Start Route
```http
POST /mobile/routes/{route_id}/start
Authorization: Bearer <token>

{
  "start_location": {
    "latitude": 40.7000,
    "longitude": -74.0000
  }
}

Response: 200
```

#### Update Location
```http
POST /mobile/location/update
Authorization: Bearer <token>

{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timestamp": "2024-01-02T09:00:00Z"
}

Response: 200
```

### Delivery Management

#### Mark Arrived at Stop
```http
POST /mobile/stops/{stop_id}/arrived
Authorization: Bearer <token>

{
  "arrival_time": "2024-01-02T09:05:00Z",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  }
}

Response: 200
```

#### Complete Delivery
```http
POST /mobile/stops/{stop_id}/complete
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "delivered_quantities": [
    {
      "product_id": "uuid",
      "delivered_quantity": 30
    }
  ],
  "completion_time": "2024-01-02T09:15:00Z",
  "notes": "Delivered successfully",
  "delivery_photo": <file>,
  "payment_collected": {
    "amount": 45.00,
    "method": "cash"
  }
}

Response: 200
{
  "status": "completed",
  "next_stop_id": "uuid"
}
```

#### Report Delivery Issue
```http
POST /mobile/stops/{stop_id}/issue
Authorization: Bearer <token>

{
  "issue_type": "customer_not_available",
  "description": "Customer not home, will reschedule",
  "reschedule_date": "2024-01-03"
}

Response: 200
```

### Expense Management

#### Get Expense Categories
```http
GET /mobile/expenses/categories
Authorization: Bearer <token>

Response:
{
  "categories": [
    {
      "id": "uuid",
      "name": "Fuel",
      "requires_receipt": true,
      "is_reimbursable": true
    }
  ]
}
```

#### Log Expense
```http
POST /mobile/expenses
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "category_id": "uuid",
  "amount": 45.50,
  "description": "Gas station fill-up",
  "expense_date": "2024-01-02",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "receipt_photo": <file>
}

Response: 201
```

#### Get My Expenses
```http
GET /mobile/expenses?date_from=2024-01-01&date_to=2024-01-31
Authorization: Bearer <token>

Response:
{
  "expenses": [
    {
      "id": "uuid",
      "category": "Fuel",
      "amount": 45.50,
      "description": "Gas station fill-up",
      "expense_date": "2024-01-02",
      "status": "approved",
      "receipt_photo_url": "https://..."
    }
  ],
  "total_amount": 325.75,
  "pending_amount": 45.50
}
```

## WebSocket Events

### Real-time Updates
```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://api.waterdelivery.com/ws');

// Events sent to admin dashboard
{
  "type": "location_update",
  "deliverer_id": "uuid",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timestamp": "2024-01-02T09:00:00Z"
}

{
  "type": "delivery_completed",
  "stop_id": "uuid",
  "order_id": "uuid",
  "deliverer_id": "uuid",
  "completion_time": "2024-01-02T09:15:00Z"
}

{
  "type": "inventory_alert",
  "product_id": "uuid",
  "product_name": "Premium Water 500ml",
  "current_stock": 5,
  "minimum_stock": 10
}

// Events sent to mobile apps
{
  "type": "route_updated",
  "route_id": "uuid",
  "message": "New order added to your route"
}

{
  "type": "order_cancelled",
  "order_id": "uuid",
  "stop_id": "uuid"
}
```

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "message": "Invalid email format"
    }
  },
  "timestamp": "2024-01-02T09:00:00Z",
  "path": "/admin/clients"
}
```

### Error Codes
- `AUTHENTICATION_FAILED`: Invalid credentials
- `AUTHORIZATION_FAILED`: Insufficient permissions
- `VALIDATION_ERROR`: Request validation failed
- `NOT_FOUND`: Resource not found
- `CONFLICT`: Resource conflict (e.g., duplicate email)
- `INSUFFICIENT_STOCK`: Not enough inventory
- `ORDER_NOT_ASSIGNABLE`: Order cannot be assigned to route
- `ROUTE_IN_PROGRESS`: Cannot modify active route

## Rate Limiting

- **Admin API**: 1000 requests per hour
- **Mobile API**: 500 requests per hour
- **Authentication**: 10 attempts per minute per IP
- **File Uploads**: 50 MB max file size, 10 files per minute

## API Versioning

- Current version: `v1`
- Version specified in URL: `/v1/admin/orders`
- Backward compatibility maintained for 2 major versions
- Deprecation notices provided 6 months before removal