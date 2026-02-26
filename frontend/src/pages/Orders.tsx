import React, { useState, useEffect } from 'react';
import { ShoppingCart, Plus, Filter, Edit, Trash2, Eye, Calendar, User, MapPin, Truck, X } from 'lucide-react';
import { orderAPI, clientAPI } from '../services/api';
import { Order, OrderCreate, OrderUpdate, ORDER_STATUS_OPTIONS } from '../types/order';
import OrderForm from '../components/OrderForm';

const Orders: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [dateFilter, setDateFilter] = useState<string>('all');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingOrder, setEditingOrder] = useState<Order | undefined>();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [viewOrder, setViewOrder] = useState<Order | null>(null);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load orders and related data
      const [ordersData, clientsData] = await Promise.all([
        orderAPI.getAll(),
        clientAPI.getAll().catch(() => [])
      ]);
      
      // Enhance orders with client names
      const enhancedOrders = ordersData.map((order: Order) => {
        const client = clientsData.find((c: any) => c.id === order.client_id);
        return {
          ...order,
          client_name: client?.name || null
        };
      });
      
      console.log('Enhanced orders:', enhancedOrders);
      setOrders(enhancedOrders);
    } catch (err) {
      console.error('Error loading orders:', err);
      setError('Failed to load orders. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (orderData: OrderCreate | OrderUpdate) => {
    console.log('handleSave called with:', orderData);
    
    try {
      setIsSubmitting(true);
      
      if (editingOrder) {
        console.log('Updating order:', editingOrder.id);
        // Update existing order
        const updatedOrder = await orderAPI.update(editingOrder.id, orderData as OrderUpdate);
        console.log('Order updated:', updatedOrder);
        setOrders(prev => prev.map(order => 
          order.id === editingOrder.id ? updatedOrder : order
        ));
        setEditingOrder(undefined);
      } else {
        console.log('Creating new order');
        // Create new order
        const newOrder = await orderAPI.create(orderData as OrderCreate);
        console.log('Order created - Raw response:', newOrder);
        
        // Enhance the new order with client name
        const clients = await clientAPI.getAll().catch(() => []);
        const client = clients.find((c: any) => c.id === newOrder.client_id);
        const enhancedNewOrder = {
          ...newOrder,
          client_name: client?.name || null
        };
        
        console.log('Enhanced new order:', enhancedNewOrder);
        setOrders(prev => [enhancedNewOrder, ...prev]);
      }
    } catch (error) {
      console.error('Error saving order:', error);
      throw error;
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (orderId: string) => {
    try {
      await orderAPI.delete(orderId);
      setOrders(prev => prev.filter(order => order.id !== orderId));
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Error deleting order:', error);
    }
  };

  const openCreateForm = () => {
    setEditingOrder(undefined);
    setIsFormOpen(true);
  };

  const openEditForm = (order: Order) => {
    setEditingOrder(order);
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
    setEditingOrder(undefined);
  };

  const getStatusBadge = (status: string) => {
    const statusOption = ORDER_STATUS_OPTIONS.find(option => option.value === status);
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
        statusOption?.color || 'bg-gray-100 text-gray-800'
      }`}>
        {statusOption?.label || status}
      </span>
    );
  };

  const formatCurrency = (amount: number) => {
    if (amount === null || amount === undefined || isNaN(amount)) {
      return '$0.00';
    }
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return 'No date';
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Invalid date';
      return date.toLocaleDateString();
    } catch (error) {
      return 'Invalid date';
    }
  };

  // Filter orders
  const filteredOrders = orders.filter(order => {
    const matchesStatus = statusFilter === 'all' || order.status === statusFilter;
    
    let matchesDate = true;
    if (dateFilter === 'today') {
      const today = new Date().toDateString();
      matchesDate = new Date(order.order_date).toDateString() === today;
    } else if (dateFilter === 'week') {
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      matchesDate = new Date(order.order_date) >= weekAgo;
    } else if (dateFilter === 'month') {
      const monthAgo = new Date();
      monthAgo.setMonth(monthAgo.getMonth() - 1);
      matchesDate = new Date(order.order_date) >= monthAgo;
    }
    
    return matchesStatus && matchesDate;
  });

  // Calculate stats
  const stats = {
    total: orders.length,
    pending: orders.filter(o => o.status === 'pending').length,
    inTransit: orders.filter(o => o.status === 'in_transit').length,
    delivered: orders.filter(o => o.status === 'delivered').length,
    totalRevenue: orders.reduce((sum, order) => sum + order.total_amount, 0)
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Orders</h1>
          <p className="text-gray-600 mt-2">Loading orders...</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
              <div className="flex items-center justify-between mb-4">
                <div className="w-20 h-6 bg-gray-200 rounded"></div>
                <div className="w-16 h-6 bg-gray-200 rounded-full"></div>
              </div>
              <div className="space-y-2">
                <div className="h-4 bg-gray-200 rounded"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Orders</h1>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-center">
            <ShoppingCart className="h-6 w-6 text-red-600 mr-3" />
            <div>
              <h3 className="text-red-800 font-medium">Connection Error</h3>
              <p className="text-red-700 mt-1">{error}</p>
              <button 
                onClick={loadOrders}
                className="mt-3 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-8">
                  <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Orders</h1>
              <p className="text-gray-600 mt-2">
                Track and manage customer orders • {orders.length} total orders
              </p>
            </div>
            <div className="flex space-x-3">
              <button 
                onClick={async () => {
                  console.log('Test button clicked');
                  try {
                    // First get a real client ID
                    const clientsData = await clientAPI.getAll();
                    console.log('Available clients:', clientsData);
                    
                    if (clientsData.length === 0) {
                      console.error('No clients available. Please create a client first.');
                      alert('No clients available. Please create a client first.');
                      return;
                    }
                    
                    const testOrder = {
                      order_number: `ORD-${Date.now()}`, // Generate unique order number
                      client_id: clientsData[0].id, // Use real client ID
                      reseller_id: clientsData[0].id, // Use same client as reseller for now
                      delivery_address: 'Test address 123 Main St',
                      order_date: new Date().toISOString().split('T')[0], // Today's date
                      status: 'pending',
                      total_amount: 50.00,
                      items: [{ 
                        product_name: 'Test Water Bottle', 
                        quantity: 2, 
                        unit_price: 25.00, 
                        total_price: 50.00 
                      }]
                    };
                    console.log('Creating test order:', testOrder);
                    const result = await orderAPI.create(testOrder);
                    console.log('Test order created successfully:', result);
                    alert('Test order created successfully!');
                    loadOrders(); // Refresh the orders list
                  } catch (error) {
                    console.error('Test order error:', error);
                    // Let's see what the backend actually returned
                    if (error instanceof Error && 'response' in error) {
                      const response = (error as any).response;
                      console.error('Backend response:', response);
                    }
                  }
                }}
                className="bg-green-600 text-white px-3 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm"
              >
                Test Create
              </button>
              <button 
                onClick={openCreateForm}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
              >
                <Plus className="h-5 w-5 mr-2" />
                New Order
              </button>
            </div>
          </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
          <div className="text-sm text-gray-600">Total Orders</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="text-2xl font-bold text-orange-600">{stats.pending}</div>
          <div className="text-sm text-gray-600">Pending</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="text-2xl font-bold text-blue-600">{stats.inTransit}</div>
          <div className="text-sm text-gray-600">In Transit</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="text-2xl font-bold text-green-600">{stats.delivered}</div>
          <div className="text-sm text-gray-600">Delivered</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="text-2xl font-bold text-purple-600">{formatCurrency(stats.totalRevenue)}</div>
          <div className="text-sm text-gray-600">Total Revenue</div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <select 
            value={statusFilter} 
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Status</option>
            {ORDER_STATUS_OPTIONS.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <select 
            value={dateFilter} 
            onChange={(e) => setDateFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Dates</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
          <div className="flex items-center text-sm text-gray-500">
            Showing {filteredOrders.length} of {orders.length} orders
          </div>
        </div>
      </div>

      {/* Orders Grid */}
      {filteredOrders.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
          <ShoppingCart className="mx-auto h-24 w-24 text-gray-400 mb-6" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {orders.length === 0 ? 'No orders found' : 'No matching orders'}
          </h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            {orders.length === 0 
              ? 'Get started by creating your first order.'
              : 'Try adjusting your filter criteria.'
            }
          </p>
          {orders.length === 0 && (
            <button 
              onClick={openCreateForm}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Create Your First Order
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredOrders.map((order) => (
            <div key={order.id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow">
              {/* Order Header */}
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="font-semibold text-gray-900">
                    Order #{order.id.slice(0, 8)}
                  </h3>
                  <div className="text-sm text-gray-500">
                    {formatDate(order.order_date)}
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusBadge(order.status)}
                  <div className="flex space-x-1">
                    <button
                      onClick={() => setViewOrder(order)}
                      className="text-gray-600 hover:text-gray-800 transition-colors"
                      title="View details"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => openEditForm(order)}
                      className="text-blue-600 hover:text-blue-800 transition-colors"
                      title="Edit order"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => setDeleteConfirm(order.id)}
                      className="text-red-600 hover:text-red-800 transition-colors"
                      title="Delete order"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Order Details */}
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center">
                  <User className="h-4 w-4 mr-2" />
                  {order.client_name || `Client ID: ${order.client_id?.slice(0, 8) || 'Unknown'}`}
                </div>
                <div className="flex items-center">
                  <MapPin className="h-4 w-4 mr-2" />
                  <span className="truncate">{order.delivery_address || 'No address specified'}</span>
                </div>
                {order.deliverer_name && (
                  <div className="flex items-center">
                    <Truck className="h-4 w-4 mr-2" />
                    {order.deliverer_name}
                  </div>
                )}
                {order.delivery_date && (
                  <div className="flex items-center">
                    <Calendar className="h-4 w-4 mr-2" />
                    Delivery: {formatDate(order.delivery_date)}
                  </div>
                )}
                <div className="pt-2 border-t border-gray-100">
                  <div className="flex justify-between items-center">
                    <span className="font-medium text-gray-900">
                      {(order.items && order.items.length > 0) ? order.items.length : 0} items
                    </span>
                    <span className="font-bold text-lg text-green-600">
                      {formatCurrency(order.total_amount || 0)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Order Form Modal */}
      <OrderForm
        order={editingOrder}
        isOpen={isFormOpen}
        onClose={closeForm}
        onSave={handleSave}
        isLoading={isSubmitting}
      />

      {/* View Order Modal */}
      {viewOrder && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 max-h-screen overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  Order #{viewOrder.id.slice(0, 8)}
                </h3>
                <button
                  onClick={() => setViewOrder(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Status</label>
                    <div className="mt-1">{getStatusBadge(viewOrder.status)}</div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Order Date</label>
                    <div className="mt-1">{formatDate(viewOrder.order_date)}</div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Client</label>
                    <div className="mt-1">{viewOrder.client_name || 'N/A'}</div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Deliverer</label>
                    <div className="mt-1">{viewOrder.deliverer_name || 'Not assigned'}</div>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Delivery Address</label>
                  <div className="mt-1">{viewOrder.delivery_address}</div>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Items</label>
                  <div className="mt-2 space-y-2">
                    {viewOrder.items?.map((item, index) => (
                      <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <div>
                          <div className="font-medium">{item.product_name}</div>
                          <div className="text-sm text-gray-500">Qty: {item.quantity}</div>
                        </div>
                        <div className="text-right">
                          <div className="font-medium">{formatCurrency(item.total_price)}</div>
                          <div className="text-sm text-gray-500">
                            {formatCurrency(item.unit_price)}/unit
                          </div>
                        </div>
                      </div>
                    )) || <div className="text-gray-500">No items</div>}
                  </div>
                </div>
                
                <div className="pt-4 border-t border-gray-200">
                  <div className="flex justify-between items-center text-lg font-bold">
                    <span>Total Amount:</span>
                    <span className="text-green-600">{formatCurrency(viewOrder.total_amount)}</span>
                  </div>
                </div>
                
                {viewOrder.notes && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Notes</label>
                    <div className="mt-1 p-3 bg-gray-50 rounded">{viewOrder.notes}</div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Delete Order
              </h3>
              <p className="text-gray-600 mb-6">
                Are you sure you want to delete this order? This action cannot be undone.
              </p>
              <div className="flex space-x-3">
                <button
                  onClick={() => setDeleteConfirm(null)}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={() => handleDelete(deleteConfirm)}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Orders;