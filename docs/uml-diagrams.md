# UML Diagrams - Water Delivery Management System

## 1. Use Case Diagram

```mermaid
graph TB
    Admin((Admin))
    Deliverer((Deliverer))
    
    %% Admin Use Cases
    Admin --> UC1[Create Orders for Clients]
    Admin --> UC2[Create Orders for Resellers]
    Admin --> UC3[Manage Inventory]
    Admin --> UC4[Manage Clients/Resellers]
    Admin --> UC5[Assign Routes to Deliverers]
    Admin --> UC6[Track Payments]
    Admin --> UC7[View Analytics Dashboard]
    Admin --> UC8[Generate Reports]
    Admin --> UC9[Manage Deliverer Accounts]
    Admin --> UC10[Manage Suppliers]
    
    %% Deliverer Use Cases (Mobile)
    Deliverer --> UC11[View Daily Route]
    Deliverer --> UC12[Update Delivery Status]
    Deliverer --> UC13[Log Expenses on Route]
    Deliverer --> UC14[Record Payment Collections]
    Deliverer --> UC15[Report Issues/Problems]
    Deliverer --> UC16[View Inventory Levels]
    Deliverer --> UC17[Sync Offline Data]
```

## 2. Enhanced Class Diagram (No Authentication)

```mermaid
classDiagram
    class Deliverer {
        +id: UUID
        +name: String
        +employeeId: String
        +vehicleInfo: String
        +licenseNumber: String
        +phoneNumber: String
        +hireDate: Date
        +territory: String
        +isAvailable: Boolean
        +currentLocation: Point
        +updateLocation()
        +markAvailable()
    }
    
    class Client {
        +id: UUID
        +name: String
        +businessName: String
        +email: String
        +phoneNumber: String
        +address: Address
        +clientType: ClientType
        +paymentTerms: PaymentTerms
        +creditLimit: Decimal
        +isActive: Boolean
        +outstandingBalance: Decimal
        +calculateBalance()
        +applyPayment()
    }
    
    class Reseller {
        +id: UUID
        +businessName: String
        +contactPerson: String
        +email: String
        +phoneNumber: String
        +address: Address
        +commissionRate: Decimal
        +paymentTerms: PaymentTerms
        +isActive: Boolean
        +totalSales: Decimal
        +calculateCommission()
    }
    
    class Product {
        +id: UUID
        +name: String
        +description: String
        +category: ProductCategory
        +size: String
        +unitPrice: Decimal
        +cost: Decimal
        +supplierId: UUID
        +isActive: Boolean
        +updatePrice()
        +calculateMargin()
    }
    
    class Inventory {
        +id: UUID
        +productId: UUID
        +currentStock: Integer
        +reservedStock: Integer
        +minimumStock: Integer
        +maximumStock: Integer
        +lastRestockDate: DateTime
        +location: String
        +addStock()
        +reserveStock()
        +releaseStock()
        +isLowStock()
    }
    
    class Order {
        +id: UUID
        +orderNumber: String
        +clientId: UUID
        +delivererId: UUID
        +orderDate: DateTime
        +requestedDeliveryDate: DateTime
        +actualDeliveryDate: DateTime
        +status: OrderStatus
        +totalAmount: Decimal
        +paymentStatus: PaymentStatus
        +notes: String
        +calculateTotal()
        +updateStatus()
    }
    
    class OrderItem {
        +id: UUID
        +orderId: UUID
        +productId: UUID
        +quantity: Integer
        +unitPrice: Decimal
        +totalPrice: Decimal
        +deliveredQuantity: Integer
        +calculateTotal()
    }
    
    class DeliveryRoute {
        +id: UUID
        +routeName: String
        +delivererId: UUID
        +routeDate: Date
        +status: RouteStatus
        +plannedStartTime: Time
        +actualStartTime: Time
        +estimatedDuration: Integer
        +actualDuration: Integer
        +totalDistance: Decimal
        +optimizeRoute()
        +calculateETA()
    }
    
    class RouteStop {
        +id: UUID
        +routeId: UUID
        +orderId: UUID
        +stopNumber: Integer
        +address: Address
        +estimatedArrival: DateTime
        +actualArrival: DateTime
        +status: StopStatus
        +notes: String
        +markCompleted()
    }
    
    class Payment {
        +id: UUID
        +orderId: UUID
        +amount: Decimal
        +paymentMethod: PaymentMethod
        +paymentDate: DateTime
        +transactionId: String
        +status: PaymentStatus
        +validatePayment()
    }
    
    class Expense {
        +id: UUID
        +delivererId: UUID
        +categoryId: UUID
        +amount: Decimal
        +description: String
        +expenseDate: Date
        +receiptPhoto: String
        +location: Point
        +isReimbursable: Boolean
        +status: ExpenseStatus
        +submitForApproval()
    }
    
    class ExpenseCategory {
        +id: UUID
        +name: String
        +description: String
        +isReimbursable: Boolean
        +requiresReceipt: Boolean
        +isActive: Boolean
    }
    
    class Supplier {
        +id: UUID
        +name: String
        +contactPerson: String
        +email: String
        +phoneNumber: String
        +address: Address
        +paymentTerms: PaymentTerms
        +isActive: Boolean
        +addProduct()
    }
    
    class Address {
        +street: String
        +city: String
        +state: String
        +zipCode: String
        +country: String
        +latitude: Decimal
        +longitude: Decimal
        +getCoordinates()
        +calculateDistance()
    }
    
    %% Relationships
    Deliverer ||--o{ DeliveryRoute : "assigned"
    DeliveryRoute ||--o{ RouteStop : "contains"
    RouteStop ||--|| Order : "delivers"
    
    Order ||--|| Client : "placed by"
    Order ||--o{ OrderItem : "contains"
    Order ||--o{ Payment : "paid through"
    OrderItem ||--|| Product : "for"
    
    Product ||--|| Supplier : "supplied by"
    Product ||--|| Inventory : "tracked in"
    
    Deliverer ||--o{ Expense : "incurs"
    ExpenseCategory ||--o{ Expense : "categorizes"
    
    Client ||--|| Address : "located at"
    Reseller ||--|| Address : "located at"
    Supplier ||--|| Address : "located at"
```

## 3. Sequence Diagram - Create Order and Assign Route

```mermaid
sequenceDiagram
    participant A as Admin
    participant Web as Responsive Web App
    participant API as FastAPI Backend
    participant DB as PostgreSQL
    participant Mobile as Mobile Interface
    participant D as Deliverer
    
    A->>Web: Open admin dashboard
    Web->>API: GET /clients (get client list)
    API->>DB: Fetch active clients
    DB-->>API: Client list
    API-->>Web: Client options
    
    Web->>API: GET /products (get available products)
    API->>DB: Fetch products with inventory
    DB-->>API: Products with stock levels
    API-->>Web: Product options with availability
    
    A->>Web: Fill order form (client, products, quantities)
    Web->>API: POST /orders (create order)
    API->>API: Validate order data
    API->>DB: Check inventory availability
    DB-->>API: Stock confirmation
    API->>DB: Reserve inventory & create order
    DB-->>API: Order ID
    API-->>Web: Order created successfully
    
    A->>Web: Assign order to deliverer route
    Web->>API: GET /deliverers/available
    API->>DB: Get available deliverers
    DB-->>API: Available deliverer list
    API-->>Web: Deliverer options
    
    A->>Web: Select deliverer and assign
    Web->>API: POST /routes (create/update route)
    API->>DB: Create route with order
    DB-->>API: Route ID
    API->>Mobile: WebSocket notification (new order assigned)
    API-->>Web: Route assigned successfully
    
    Mobile->>D: Real-time update: New order assigned
    D->>Mobile: Open mobile view to see route
    Mobile->>API: GET /routes/deliverer/{deliverer_id} (get today's route)
    API->>DB: Fetch deliverer's route
    DB-->>API: Route with orders
    API-->>Mobile: Route details with GPS coordinates
```

## 4. Activity Diagram - Mobile Delivery Process

```mermaid
graph TD
    Start([Start: Begin Route]) --> CheckRoute{Route Available?}
    CheckRoute -->|No| WaitForRoute[Wait for Route Assignment]
    WaitForRoute --> CheckRoute
    CheckRoute -->|Yes| StartRoute[Mark Route as Started]
    
    StartRoute --> GetNextStop[Get Next Route Stop]
    GetNextStop --> Navigate[Navigate to Location]
    Navigate --> Arrived{Arrived at Location?}
    Arrived -->|No| UpdateLocation[Update GPS Location]
    UpdateLocation --> Navigate
    
    Arrived -->|Yes| MarkArrived[Mark Arrived at Stop]
    MarkArrived --> ContactCustomer[Contact Customer]
    ContactCustomer --> CustomerAvailable{Customer Available?}
    
    CustomerAvailable -->|No| RescheduleDelivery[Schedule Redelivery]
    RescheduleDelivery --> UpdateOrderStatus[Update Order Status]
    
    CustomerAvailable -->|Yes| DeliverProducts[Deliver Products]
    DeliverProducts --> TakePhoto[Take Delivery Confirmation Photo]
    TakePhoto --> CollectPayment{Payment Required?}
    
    CollectPayment -->|Yes| ProcessPayment[Record Payment Collection]
    ProcessPayment --> UpdateInventory[Update Mobile Inventory]
    CollectPayment -->|No| UpdateInventory
    
    UpdateInventory --> MarkCompleted[Mark Stop as Completed]
    MarkCompleted --> UpdateOrderStatus
    UpdateOrderStatus --> SyncData[Sync Data with Server]
    SyncData --> MoreStops{More Stops in Route?}
    
    MoreStops -->|Yes| GetNextStop
    MoreStops -->|No| CompleteRoute[Mark Route as Completed]
    CompleteRoute --> SubmitExpenses[Submit Route Expenses]
    SubmitExpenses --> End([End Route])
    
    RescheduleDelivery --> MoreStops
```

## 5. Enhanced Entity Relationship Diagram

```mermaid
erDiagram
    USERS {
        uuid id PK
        string email UK
        string password_hash
        string first_name
        string last_name
        enum role
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }
    
    DELIVERERS {
        uuid id PK
        uuid user_id FK
        string employee_id UK
        string vehicle_info
        string license_number
        string phone_number
        date hire_date
        string territory
        boolean is_available
        point current_location
        timestamp last_location_update
    }
    
    CLIENTS {
        uuid id PK
        string name
        string business_name
        string email
        string phone_number
        text address
        decimal latitude
        decimal longitude
        enum client_type
        enum payment_terms
        decimal credit_limit
        decimal outstanding_balance
        boolean is_active
        timestamp created_at
    }
    
    RESELLERS {
        uuid id PK
        string business_name
        string contact_person
        string email
        string phone_number
        text address
        decimal latitude
        decimal longitude
        decimal commission_rate
        enum payment_terms
        decimal total_sales
        boolean is_active
        timestamp created_at
    }
    
    SUPPLIERS {
        uuid id PK
        string name
        string contact_person
        string email
        string phone_number
        text address
        enum payment_terms
        boolean is_active
        timestamp created_at
    }
    
    PRODUCTS {
        uuid id PK
        string name
        text description
        enum category
        string size
        decimal unit_price
        decimal cost
        uuid supplier_id FK
        boolean is_active
        timestamp created_at
    }
    
    INVENTORY {
        uuid id PK
        uuid product_id FK
        integer current_stock
        integer reserved_stock
        integer minimum_stock
        integer maximum_stock
        datetime last_restock_date
        string location
        timestamp updated_at
    }
    
    ORDERS {
        uuid id PK
        string order_number UK
        uuid client_id FK
        uuid reseller_id FK
        uuid deliverer_id FK
        datetime order_date
        datetime requested_delivery_date
        datetime actual_delivery_date
        enum status
        decimal total_amount
        enum payment_status
        text notes
        timestamp created_at
    }
    
    ORDER_ITEMS {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        integer quantity
        decimal unit_price
        decimal total_price
        integer delivered_quantity
    }
    
    DELIVERY_ROUTES {
        uuid id PK
        string route_name
        uuid deliverer_id FK
        date route_date
        enum status
        time planned_start_time
        time actual_start_time
        integer estimated_duration
        integer actual_duration
        decimal total_distance
        timestamp created_at
    }
    
    ROUTE_STOPS {
        uuid id PK
        uuid route_id FK
        uuid order_id FK
        integer stop_number
        text address
        decimal latitude
        decimal longitude
        datetime estimated_arrival
        datetime actual_arrival
        enum status
        text notes
    }
    
    PAYMENTS {
        uuid id PK
        uuid order_id FK
        decimal amount
        enum payment_method
        datetime payment_date
        string transaction_id
        enum status
        uuid processed_by FK
        timestamp created_at
    }
    
    EXPENSES {
        uuid id PK
        uuid deliverer_id FK
        uuid category_id FK
        decimal amount
        text description
        date expense_date
        string receipt_photo
        point location
        boolean is_reimbursable
        enum status
        timestamp created_at
    }
    
    EXPENSE_CATEGORIES {
        uuid id PK
        string name
        text description
        boolean is_reimbursable
        boolean requires_receipt
        boolean is_active
    }
    
    %% Relationships
    USERS ||--o| DELIVERERS : "one-to-zero-or-one"
    DELIVERERS ||--o{ DELIVERY_ROUTES : "one-to-many"
    DELIVERY_ROUTES ||--o{ ROUTE_STOPS : "one-to-many"
    ROUTE_STOPS ||--|| ORDERS : "one-to-one"
    
    CLIENTS ||--o{ ORDERS : "one-to-many"
    RESELLERS ||--o{ ORDERS : "one-to-many"
    DELIVERERS ||--o{ ORDERS : "one-to-many"
    ORDERS ||--o{ ORDER_ITEMS : "one-to-many"
    ORDERS ||--o{ PAYMENTS : "one-to-many"
    
    SUPPLIERS ||--o{ PRODUCTS : "one-to-many"
    PRODUCTS ||--|| INVENTORY : "one-to-one"
    PRODUCTS ||--o{ ORDER_ITEMS : "one-to-many"
    
    DELIVERERS ||--o{ EXPENSES : "one-to-many"
    EXPENSE_CATEGORIES ||--o{ EXPENSES : "one-to-many"
    USERS ||--o{ PAYMENTS : "processed-by"
```

## 6. System Architecture Diagram

```mermaid
graph TB
    subgraph "Client Devices"
        Desktop[Desktop Browser - Admin]
        Mobile[Mobile Browser - Deliverers]
    end
    
    subgraph "Frontend - Single Responsive Web App"
        React[React Application]
        AdminUI[Admin Interface Components]
        MobileUI[Mobile Interface Components]
        PWA[PWA Features]
        Router[React Router]
        State[State Management]
    end
    
    subgraph "API Layer"
        FastAPI[FastAPI Backend]
        WebSocket[Real-time Updates]
        FileUpload[File Upload Handler]
        CORS[CORS Handler]
    end
    
    subgraph "Business Logic"
        OrderService[Order Management]
        RouteService[Route Optimization]
        InventoryService[Inventory Management]
        PaymentService[Payment Processing]
        NotificationService[Notification System]
    end
    
    subgraph "Data Layer"
        PostgreSQL[(PostgreSQL Database)]
        Redis[(Redis Cache)]
        FileStorage[(File Storage - Photos)]
    end
    
    subgraph "External Services"
        MapsAPI[Google Maps API]
        SMSService[SMS Notifications]
        EmailService[Email Service]
    end
    
    %% Connections
    Desktop --> React
    Mobile --> React
    React --> AdminUI
    React --> MobileUI
    React --> Router
    React --> State
    React --> PWA
    React --> FastAPI
    
    FastAPI --> CORS
    FastAPI --> WebSocket
    FastAPI --> OrderService
    FastAPI --> RouteService
    FastAPI --> InventoryService
    FastAPI --> PaymentService
    FastAPI --> NotificationService
    
    OrderService --> PostgreSQL
    RouteService --> PostgreSQL
    InventoryService --> PostgreSQL
    PaymentService --> PostgreSQL
    NotificationService --> Redis
    
    FastAPI --> Redis
    FileUpload --> FileStorage
    
    RouteService --> MapsAPI
    NotificationService --> SMSService
    NotificationService --> EmailService
    
    PWA --> FileStorage
```

This comprehensive UML documentation covers all the enhanced requirements including inventory management, route planning, mobile support, and payment tracking. Would you like me to elaborate on any specific diagram or create additional ones?