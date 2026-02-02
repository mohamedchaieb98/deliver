# Database Schema - Water Delivery Management System (No Authentication)

## Database Design Principles

- **PostgreSQL** as the primary database for ACID compliance and advanced features
- **UUID** primary keys for better scalability and security
- **Timestamps** for all entities to track creation and modification
- **Soft deletes** where appropriate to maintain data integrity
- **Indexes** on frequently queried columns
- **Foreign key constraints** to ensure data integrity
- **No user authentication** - direct access system

## Core Tables

### 1. Deliverers Table (No User Dependency)
```sql
CREATE TABLE deliverers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255),
    vehicle_info JSONB, -- {make, model, year, plate_number, capacity}
    license_number VARCHAR(50),
    phone_number VARCHAR(20),
    hire_date DATE,
    territory VARCHAR(100),
    is_available BOOLEAN DEFAULT true,
    current_location POINT,
    last_location_update TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_deliverers_employee_id ON deliverers(employee_id);
CREATE INDEX idx_deliverers_territory ON deliverers(territory);
CREATE INDEX idx_deliverers_available ON deliverers(is_available);
```

### 3. Clients Table
```sql
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    business_name VARCHAR(200),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    address TEXT NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    client_type VARCHAR(20) DEFAULT 'individual' CHECK (client_type IN ('individual', 'business', 'restaurant', 'office')),
    payment_terms VARCHAR(20) DEFAULT 'cash' CHECK (payment_terms IN ('cash', 'credit_7', 'credit_15', 'credit_30')),
    credit_limit DECIMAL(10, 2) DEFAULT 0,
    outstanding_balance DECIMAL(10, 2) DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_clients_name ON clients(name);
CREATE INDEX idx_clients_type ON clients(client_type);
CREATE INDEX idx_clients_active ON clients(is_active);
CREATE INDEX idx_clients_location ON clients USING GIST(POINT(longitude, latitude));
```

### 4. Resellers Table
```sql
CREATE TABLE resellers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(200),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    address TEXT NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    commission_rate DECIMAL(5, 4) DEFAULT 0.10, -- 10% commission
    payment_terms VARCHAR(20) DEFAULT 'credit_30',
    total_sales DECIMAL(12, 2) DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    contract_start_date DATE,
    contract_end_date DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_resellers_business_name ON resellers(business_name);
CREATE INDEX idx_resellers_active ON resellers(is_active);
```

### 5. Suppliers Table
```sql
CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(200),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    address TEXT,
    payment_terms VARCHAR(20) DEFAULT 'credit_30',
    is_active BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_suppliers_name ON suppliers(name);
CREATE INDEX idx_suppliers_active ON suppliers(is_active);
```

### 6. Products Table
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL CHECK (category IN ('bottled_water', 'gallon', 'dispenser', 'accessories')),
    size VARCHAR(20), -- '500ml', '1L', '5L', '19L', etc.
    unit_price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2), -- Cost price for margin calculation
    supplier_id UUID REFERENCES suppliers(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_active ON products(is_active);
```

### 7. Inventory Table
```sql
CREATE TABLE inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID UNIQUE REFERENCES products(id) ON DELETE CASCADE,
    current_stock INTEGER DEFAULT 0,
    reserved_stock INTEGER DEFAULT 0, -- Stock reserved for pending orders
    minimum_stock INTEGER DEFAULT 10,
    maximum_stock INTEGER DEFAULT 1000,
    last_restock_date TIMESTAMPTZ,
    location VARCHAR(100) DEFAULT 'main_warehouse',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_inventory_product_id ON inventory(product_id);
CREATE INDEX idx_inventory_low_stock ON inventory WHERE current_stock <= minimum_stock;
```

### 8. Orders Table
```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(20) UNIQUE NOT NULL,
    client_id UUID REFERENCES clients(id),
    reseller_id UUID REFERENCES resellers(id),
    deliverer_id UUID REFERENCES deliverers(id),
    order_date TIMESTAMPTZ DEFAULT NOW(),
    requested_delivery_date DATE,
    actual_delivery_date TIMESTAMPTZ,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'assigned', 'in_transit', 'delivered', 'failed', 'cancelled')),
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'partial', 'paid', 'overdue')),
    delivery_address TEXT,
    delivery_latitude DECIMAL(10, 8),
    delivery_longitude DECIMAL(11, 8),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT check_client_or_reseller CHECK ((client_id IS NOT NULL) != (reseller_id IS NOT NULL))
);

CREATE INDEX idx_orders_number ON orders(order_number);
CREATE INDEX idx_orders_client_id ON orders(client_id);
CREATE INDEX idx_orders_reseller_id ON orders(reseller_id);
CREATE INDEX idx_orders_deliverer_id ON orders(deliverer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(order_date);
```

### 9. Order Items Table
```sql
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    delivered_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```

### 10. Delivery Routes Table
```sql
CREATE TABLE delivery_routes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_name VARCHAR(100),
    deliverer_id UUID REFERENCES deliverers(id),
    route_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'planned' CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled')),
    planned_start_time TIME,
    actual_start_time TIME,
    estimated_duration INTEGER, -- minutes
    actual_duration INTEGER, -- minutes
    total_distance DECIMAL(8, 2), -- kilometers
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_routes_deliverer_id ON delivery_routes(deliverer_id);
CREATE INDEX idx_routes_date ON delivery_routes(route_date);
CREATE INDEX idx_routes_status ON delivery_routes(status);
```

### 11. Route Stops Table
```sql
CREATE TABLE route_stops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id UUID REFERENCES delivery_routes(id) ON DELETE CASCADE,
    order_id UUID REFERENCES orders(id),
    stop_number INTEGER NOT NULL,
    address TEXT NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    estimated_arrival TIMESTAMPTZ,
    actual_arrival TIMESTAMPTZ,
    departure_time TIMESTAMPTZ,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'arrived', 'completed', 'failed', 'skipped')),
    notes TEXT,
    delivery_photo_path VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_route_stops_route_id ON route_stops(route_id);
CREATE INDEX idx_route_stops_order_id ON route_stops(order_id);
CREATE INDEX idx_route_stops_status ON route_stops(status);
```

### 12. Payments Table
```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL CHECK (payment_method IN ('cash', 'card', 'bank_transfer', 'check', 'digital')),
    payment_date TIMESTAMPTZ DEFAULT NOW(),
    transaction_id VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'failed', 'refunded')),
    processed_by UUID REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_payments_method ON payments(payment_method);
CREATE INDEX idx_payments_status ON payments(status);
```

### 13. Expenses Table
```sql
CREATE TABLE expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deliverer_id UUID REFERENCES deliverers(id),
    category_id UUID REFERENCES expense_categories(id),
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT NOT NULL,
    expense_date DATE NOT NULL,
    receipt_photo_path VARCHAR(500),
    location POINT,
    is_reimbursable BOOLEAN DEFAULT true,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'paid')),
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_expenses_deliverer_id ON expenses(deliverer_id);
CREATE INDEX idx_expenses_category_id ON expenses(category_id);
CREATE INDEX idx_expenses_date ON expenses(expense_date);
CREATE INDEX idx_expenses_status ON expenses(status);
```

### 14. Expense Categories Table
```sql
CREATE TABLE expense_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_reimbursable BOOLEAN DEFAULT true,
    requires_receipt BOOLEAN DEFAULT true,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_expense_categories_name ON expense_categories(name);
CREATE INDEX idx_expense_categories_active ON expense_categories(is_active);
```

### 15. Inventory Movements Table (Audit Trail)
```sql
CREATE TABLE inventory_movements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id),
    movement_type VARCHAR(20) NOT NULL CHECK (movement_type IN ('restock', 'sale', 'adjustment', 'return', 'damage')),
    quantity_change INTEGER NOT NULL, -- Positive for increase, negative for decrease
    reference_id UUID, -- Could be order_id, adjustment_id, etc.
    reference_type VARCHAR(20), -- 'order', 'adjustment', 'return', etc.
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_inventory_movements_product_id ON inventory_movements(product_id);
CREATE INDEX idx_inventory_movements_type ON inventory_movements(movement_type);
CREATE INDEX idx_inventory_movements_date ON inventory_movements(created_at);
```

## Views for Common Queries

### 1. Deliverer Performance View
```sql
CREATE VIEW deliverer_performance AS
SELECT 
    d.id,
    u.first_name,
    u.last_name,
    COUNT(DISTINCT dr.id) as total_routes,
    COUNT(DISTINCT o.id) as total_deliveries,
    COUNT(CASE WHEN o.status = 'delivered' THEN 1 END) as successful_deliveries,
    ROUND(
        COUNT(CASE WHEN o.status = 'delivered' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(DISTINCT o.id), 0), 2
    ) as success_rate,
    SUM(CASE WHEN o.status = 'delivered' THEN o.total_amount ELSE 0 END) as total_sales,
    SUM(e.amount) as total_expenses
FROM deliverers d
JOIN users u ON d.user_id = u.id
LEFT JOIN delivery_routes dr ON d.id = dr.deliverer_id
LEFT JOIN orders o ON d.id = o.deliverer_id
LEFT JOIN expenses e ON d.id = e.deliverer_id
GROUP BY d.id, u.first_name, u.last_name;
```

### 2. Low Stock Alert View
```sql
CREATE VIEW low_stock_alerts AS
SELECT 
    p.id,
    p.name,
    p.category,
    i.current_stock,
    i.minimum_stock,
    i.last_restock_date,
    (i.minimum_stock - i.current_stock) as shortage_quantity
FROM products p
JOIN inventory i ON p.id = i.product_id
WHERE i.current_stock <= i.minimum_stock
AND p.is_active = true;
```

### 3. Daily Sales Summary View
```sql
CREATE VIEW daily_sales_summary AS
SELECT 
    DATE(o.order_date) as sale_date,
    COUNT(*) as total_orders,
    COUNT(CASE WHEN o.status = 'delivered' THEN 1 END) as delivered_orders,
    SUM(o.total_amount) as total_revenue,
    SUM(CASE WHEN o.status = 'delivered' THEN o.total_amount ELSE 0 END) as confirmed_revenue,
    COUNT(DISTINCT o.deliverer_id) as active_deliverers
FROM orders o
GROUP BY DATE(o.order_date)
ORDER BY sale_date DESC;
```

## Triggers and Functions

### 1. Update Inventory on Order Completion
```sql
CREATE OR REPLACE FUNCTION update_inventory_on_delivery()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'delivered' AND OLD.status != 'delivered' THEN
        -- Update inventory for each order item
        UPDATE inventory 
        SET current_stock = current_stock - oi.delivered_quantity,
            updated_at = NOW()
        FROM order_items oi
        WHERE oi.order_id = NEW.id 
        AND inventory.product_id = oi.product_id;
        
        -- Create inventory movement records
        INSERT INTO inventory_movements (product_id, movement_type, quantity_change, reference_id, reference_type, created_at)
        SELECT 
            oi.product_id,
            'sale',
            -oi.delivered_quantity,
            NEW.id,
            'order',
            NOW()
        FROM order_items oi
        WHERE oi.order_id = NEW.id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_inventory_on_delivery
    AFTER UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_inventory_on_delivery();
```

### 2. Update Outstanding Balance on Payment
```sql
CREATE OR REPLACE FUNCTION update_outstanding_balance()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'confirmed' THEN
        UPDATE clients 
        SET outstanding_balance = outstanding_balance - NEW.amount,
            updated_at = NOW()
        FROM orders o
        WHERE o.id = NEW.order_id 
        AND clients.id = o.client_id;
        
        UPDATE resellers 
        SET outstanding_balance = outstanding_balance - NEW.amount,
            updated_at = NOW()
        FROM orders o
        WHERE o.id = NEW.order_id 
        AND resellers.id = o.reseller_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_outstanding_balance
    AFTER INSERT OR UPDATE ON payments
    FOR EACH ROW
    EXECUTE FUNCTION update_outstanding_balance();
```

## Initial Data Seeds

### Default Expense Categories
```sql
INSERT INTO expense_categories (name, description, is_reimbursable, requires_receipt) VALUES
('Fuel', 'Vehicle fuel expenses', true, true),
('Vehicle Maintenance', 'Repairs and maintenance', true, true),
('Toll Fees', 'Road toll charges', true, true),
('Parking', 'Parking fees', true, true),
('Phone/Communication', 'Mobile phone and communication costs', true, true),
('Meals', 'Meal expenses during work', false, false),
('Other', 'Miscellaneous expenses', true, true);
```

### Sample Products
```sql
-- Assuming we have a supplier first
INSERT INTO suppliers (name, contact_person, phone_number, email) VALUES
('Pure Water Co.', 'John Smith', '+1234567890', 'john@purewater.com');

-- Then products
INSERT INTO products (name, description, category, size, unit_price, cost, supplier_id) VALUES
('Premium Bottled Water', 'Pure spring water in 500ml bottles', 'bottled_water', '500ml', 1.50, 0.80, (SELECT id FROM suppliers WHERE name = 'Pure Water Co.' LIMIT 1)),
('Large Water Jug', '19-liter water jug for dispensers', 'gallon', '19L', 8.00, 4.50, (SELECT id FROM suppliers WHERE name = 'Pure Water Co.' LIMIT 1)),
('Water Dispenser', 'Cold/hot water dispenser', 'dispenser', 'Standard', 150.00, 90.00, (SELECT id FROM suppliers WHERE name = 'Pure Water Co.' LIMIT 1));
```

This database schema provides a solid foundation for the water delivery management system with proper indexing, constraints, and audit trails.