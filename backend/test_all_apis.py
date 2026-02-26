#!/usr/bin/env python3
"""
Comprehensive API Test Script
Tests all endpoints with all HTTP methods (GET, POST, PUT, DELETE)
"""

import time
from datetime import date, datetime

import requests

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}


class Colors:
    """ANSI color codes for terminal output"""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def print_header(text):
    """Print a colored header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")


def print_test(method, endpoint, description=""):
    """Print test information"""
    print(f"\n{Colors.CYAN}🧪 Testing: {Colors.BOLD}{method} {endpoint}{Colors.END}")
    if description:
        print(f"   {Colors.YELLOW}📝 {description}{Colors.END}")


def print_result(success, message, status_code=None, response_data=None):
    """Print test result"""
    if success:
        status = f"{Colors.GREEN}✅ SUCCESS{Colors.END}"
        if status_code:
            status += f" (HTTP {status_code})"
    else:
        status = f"{Colors.RED}❌ FAILED{Colors.END}"
        if status_code:
            status += f" (HTTP {status_code})"

    print(f"   {status} - {message}")
    if response_data and len(str(response_data)) < 200:
        print(f"   {Colors.WHITE}📄 Response: {response_data}{Colors.END}")


def make_request(method, endpoint, data=None, params=None):
    """Make HTTP request and return response"""
    url = f"{BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, params=params)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS)
        else:
            raise ValueError(f"Unsupported method: {method}")

        return response
    except requests.exceptions.ConnectionError:
        return None


def test_endpoint(
    method, endpoint, data=None, params=None, description="", expect_status=None
):
    """Test a single endpoint"""
    print_test(method, endpoint, description)

    response = make_request(method, endpoint, data, params)

    if response is None:
        print_result(False, "Connection failed - Is the server running?")
        return None

    # Determine if test passed
    if expect_status:
        success = response.status_code == expect_status
    else:
        success = 200 <= response.status_code < 400

    # Get response data
    try:
        response_data = response.json() if response.content else {}
    except (ValueError, TypeError):
        response_data = response.text

    print_result(success, "Request completed", response.status_code, response_data)

    return response if success else None


# Test Data Templates
def get_test_data():
    """Get test data for all entities"""
    return {
        "deliverer": {
            "name": "Test Deliverer",
            "employee_id": f"EMP{int(time.time())}",
            "email": "test.deliverer@example.com",
            "phone_number": "+1234567890",
            "territory": "Test Zone",
            "is_available": True,
        },
        "client": {
            "name": "Test Client",
            "business_name": "Test Business",
            "email": "test.client@example.com",
            "phone_number": "+1234567891",
            "address": "123 Test Street, Test City",
            "client_type": "business",
            "payment_terms": "net30",
        },
        "expense": {
            "description": "Test Expense - Gas for delivery",
            "amount": 25.50,
            "expense_date": str(date.today()),
            "status": "pending",
            "location": "Test Location",
            "is_reimbursable": True,
        },
        "product": {
            "name": "Test Water Bottle",
            "description": "Test product for API testing",
            "category": "beverages",
            "size": "500ml",
            "sku": f"TEST-{int(time.time())}",
            "is_active": True,
        },
        "supplier": {
            "name": "Test Supplier",
            "contact_person": "John Doe",
            "email": "test.supplier@example.com",
            "phone_number": "+1234567892",
            "address": "456 Supplier St, Supply City",
        },
        "reseller": {
            "business_name": "Test Reseller Business",
            "contact_person": "Jane Smith",
            "email": "test.reseller@example.com",
            "phone_number": "+1234567893",
        },
        "order": {
            "order_number": f"ORD-{int(time.time())}",
            "status": "pending",
            "client_id": None,  # Will be filled dynamically
            "reseller_id": None,  # Will be filled dynamically
            "deliverer_id": None,
            "order_date": str(datetime.now().isoformat()),
            "delivery_date": None,
            "delivery_address": "123 Test Delivery Address",
            "total_amount": 25.00,
            "notes": "Test order from API testing",
            "items": [
                {
                    "product_name": "Water Bottle",
                    "quantity": 1,
                    "unit_price": 25.00,
                    "total_price": 25.00,
                }
            ],
        },
    }


def test_deliverers_api():
    """Test all deliverer endpoints"""
    print_header("TESTING DELIVERERS API")

    # GET /deliverers - List all
    response = test_endpoint("GET", "/deliverers", description="Get all deliverers")

    # POST /deliverers - Create new
    deliverer_data = get_test_data()["deliverer"]
    response = test_endpoint(
        "POST",
        "/deliverers",
        data=deliverer_data,
        description="Create new deliverer",
        expect_status=201,
    )

    deliverer_id = None
    if response:
        try:
            deliverer_id = response.json().get("id")
        except (ValueError, KeyError, TypeError):
            pass

    if deliverer_id:
        # GET /deliverers/{id} - Get specific
        test_endpoint(
            "GET", f"/deliverers/{deliverer_id}", description="Get deliverer by ID"
        )

        # PUT /deliverers/{id} - Update
        update_data = {"name": "Updated Test Deliverer", "is_available": False}
        test_endpoint(
            "PUT",
            f"/deliverers/{deliverer_id}",
            data=update_data,
            description="Update deliverer",
        )

        # DELETE /deliverers/{id} - Delete
        test_endpoint(
            "DELETE", f"/deliverers/{deliverer_id}", description="Delete deliverer"
        )

    # GET /deliverers/stats/summary - Stats
    test_endpoint("GET", "/deliverers/stats/summary", description="Get deliverer stats")


def test_clients_api():
    """Test all client endpoints"""
    print_header("TESTING CLIENTS API")

    # GET /clients - List all
    test_endpoint("GET", "/clients", description="Get all clients")

    # POST /clients - Create new
    client_data = get_test_data()["client"]
    response = test_endpoint(
        "POST",
        "/clients",
        data=client_data,
        description="Create new client",
        expect_status=201,
    )

    client_id = None
    if response:
        try:
            client_id = response.json().get("id")
        except (ValueError, KeyError, TypeError):
            pass

    if client_id:
        # GET /clients/{id} - Get specific
        test_endpoint("GET", f"/clients/{client_id}", description="Get client by ID")

        # PUT /clients/{id} - Update
        update_data = {"name": "Updated Test Client", "client_type": "individual"}
        test_endpoint(
            "PUT",
            f"/clients/{client_id}",
            data=update_data,
            description="Update client",
        )

        # DELETE /clients/{id} - Delete (soft delete)
        test_endpoint("DELETE", f"/clients/{client_id}", description="Delete client")


def test_expenses_api():
    """Test all expense endpoints"""
    print_header("TESTING EXPENSES API")

    # GET /expenses - List all
    test_endpoint("GET", "/expenses", description="Get all expenses")

    # POST /expenses - Create new
    expense_data = get_test_data()["expense"]
    response = test_endpoint(
        "POST",
        "/expenses",
        data=expense_data,
        description="Create new expense",
        expect_status=201,
    )

    expense_id = None
    if response:
        try:
            expense_id = response.json().get("id")
        except (ValueError, KeyError, TypeError):
            pass

    if expense_id:
        # GET /expenses/{id} - Get specific
        test_endpoint("GET", f"/expenses/{expense_id}", description="Get expense by ID")

        # PUT /expenses/{id} - Update
        update_data = {"description": "Updated Test Expense", "amount": 35.75}
        test_endpoint(
            "PUT",
            f"/expenses/{expense_id}",
            data=update_data,
            description="Update expense",
        )

        # DELETE /expenses/{id} - Delete
        test_endpoint("DELETE", f"/expenses/{expense_id}", description="Delete expense")


def test_products_api():
    """Test all product endpoints"""
    print_header("TESTING PRODUCTS API")

    # GET /products - List all
    test_endpoint("GET", "/products", description="Get all products")

    # POST /products - Create new
    product_data = get_test_data()["product"]
    response = test_endpoint(
        "POST",
        "/products",
        data=product_data,
        description="Create new product",
        expect_status=201,
    )

    product_id = None
    if response:
        try:
            product_id = response.json().get("id")
        except (ValueError, KeyError, TypeError):
            pass

    if product_id:
        # GET /products/{id} - Get specific
        test_endpoint("GET", f"/products/{product_id}", description="Get product by ID")

        # PUT /products/{id} - Update
        update_data = {"name": "Updated Test Product", "size": "1L"}
        test_endpoint(
            "PUT",
            f"/products/{product_id}",
            data=update_data,
            description="Update product",
        )

        # DELETE /products/{id} - Delete
        test_endpoint("DELETE", f"/products/{product_id}", description="Delete product")


def test_suppliers_api():
    """Test all supplier endpoints"""
    print_header("TESTING SUPPLIERS API")

    # GET /suppliers - List all
    test_endpoint("GET", "/suppliers", description="Get all suppliers")

    # POST /suppliers - Create new
    supplier_data = get_test_data()["supplier"]
    response = test_endpoint(
        "POST",
        "/suppliers",
        data=supplier_data,
        description="Create new supplier",
        expect_status=201,
    )

    supplier_id = None
    if response:
        try:
            supplier_id = response.json().get("id")
        except (ValueError, KeyError, TypeError):
            pass

    if supplier_id:
        # GET /suppliers/{id} - Get specific
        test_endpoint(
            "GET", f"/suppliers/{supplier_id}", description="Get supplier by ID"
        )

        # PUT /suppliers/{id} - Update
        update_data = {
            "name": "Updated Test Supplier",
            "contact_person": "John Updated",
        }
        test_endpoint(
            "PUT",
            f"/suppliers/{supplier_id}",
            data=update_data,
            description="Update supplier",
        )

        # DELETE /suppliers/{id} - Delete
        test_endpoint(
            "DELETE", f"/suppliers/{supplier_id}", description="Delete supplier"
        )


def test_resellers_api():
    """Test all reseller endpoints"""
    print_header("TESTING RESELLERS API")

    # GET /resellers - List all
    test_endpoint("GET", "/resellers", description="Get all resellers")

    # POST /resellers - Create new
    reseller_data = get_test_data()["reseller"]
    response = test_endpoint(
        "POST",
        "/resellers",
        data=reseller_data,
        description="Create new reseller",
        expect_status=201,
    )

    reseller_id = None
    if response:
        try:
            reseller_id = response.json().get("id")
        except (ValueError, KeyError, TypeError):
            pass

    if reseller_id:
        # GET /resellers/{id} - Get specific
        test_endpoint(
            "GET", f"/resellers/{reseller_id}", description="Get reseller by ID"
        )

        # PUT /resellers/{id} - Update
        update_data = {
            "business_name": "Updated Test Reseller",
            "contact_person": "Jane Updated",
        }
        test_endpoint(
            "PUT",
            f"/resellers/{reseller_id}",
            data=update_data,
            description="Update reseller",
        )

        # DELETE /resellers/{id} - Delete
        test_endpoint(
            "DELETE", f"/resellers/{reseller_id}", description="Delete reseller"
        )

    # GET /resellers/stats/summary - Stats
    test_endpoint("GET", "/resellers/stats/summary", description="Get reseller stats")


def test_orders_api():
    """Test all order endpoints"""
    print_header("TESTING ORDERS API")

    # First create a client for the order
    client_data = get_test_data()["client"]
    client_data["name"] = "Order Test Client"
    client_response = test_endpoint(
        "POST",
        "/clients",
        data=client_data,
        description="Create client for order test",
        expect_status=201,
    )

    client_id = None
    if client_response:
        try:
            client_id = client_response.json().get("id")
        except (ValueError, KeyError, TypeError):
            pass

    # GET /orders - List all
    test_endpoint("GET", "/orders", description="Get all orders")

    if client_id:
        # POST /orders - Create new
        order_data = get_test_data()["order"]
        order_data["client_id"] = client_id
        response = test_endpoint(
            "POST",
            "/orders",
            data=order_data,
            description="Create new order",
            expect_status=201,
        )

        order_id = None
        if response:
            try:
                order_id = response.json().get("id")
            except (ValueError, KeyError, TypeError):
                pass

        if order_id:
            # GET /orders/{id} - Get specific
            test_endpoint("GET", f"/orders/{order_id}", description="Get order by ID")

            # PUT /orders/{id} - Update
            update_data = {"status": "confirmed", "notes": "Updated order notes"}
            test_endpoint(
                "PUT",
                f"/orders/{order_id}",
                data=update_data,
                description="Update order",
            )

            # DELETE /orders/{id} - Delete
            test_endpoint("DELETE", f"/orders/{order_id}", description="Delete order")


def test_other_endpoints():
    """Test other available endpoints"""
    print_header("TESTING OTHER ENDPOINTS")

    # Dashboard endpoints
    test_endpoint("GET", "/dashboard/stats", description="Get dashboard stats")

    # Routes endpoints
    test_endpoint("GET", "/routes", description="Get all routes")
    test_endpoint("GET", "/routes/categories", description="Get route categories")

    # Inventory endpoints
    test_endpoint("GET", "/inventory", description="Get inventory")
    test_endpoint("GET", "/inventory/low-stock", description="Get low stock items")

    # Payments endpoints
    test_endpoint("GET", "/payments", description="Get all payments")

    # Expenses categories
    test_endpoint("GET", "/expenses/categories", description="Get expense categories")


def test_server_connection():
    """Test if server is running"""
    print_header("TESTING SERVER CONNECTION")

    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health", timeout=5)
        if response.status_code == 200:
            print_result(True, f"Server is running on {BASE_URL}")
            return True
        else:
            print_result(False, f"Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_result(False, f"Cannot connect to server at {BASE_URL}")
        print(f"{Colors.YELLOW}💡 Make sure the server is running with:{Colors.END}")
        print(f"{Colors.WHITE}   cd backend{Colors.END}")
        print(f"{Colors.WHITE}   .\\venv\\Scripts\\activate{Colors.END}")
        print(f"{Colors.WHITE}   uvicorn app.main:app --reload --port 8000{Colors.END}")
        return False


def main():
    """Main test function"""
    print(f"{Colors.BOLD}{Colors.PURPLE}")
    print("🚀 WATER DELIVERY MANAGEMENT SYSTEM - API TEST SUITE")
    print("=" * 60)
    print(f"{Colors.END}")

    # Test server connection first
    if not test_server_connection():
        return

    # Run all tests
    try:
        test_deliverers_api()
        test_clients_api()
        test_expenses_api()
        test_products_api()
        test_suppliers_api()
        test_resellers_api()
        test_orders_api()
        test_other_endpoints()

        print_header("🎉 ALL TESTS COMPLETED!")
        print(f"{Colors.GREEN}✅ API testing finished. Check results above.{Colors.END}")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Tests interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Test suite error: {str(e)}{Colors.END}")


if __name__ == "__main__":
    main()
