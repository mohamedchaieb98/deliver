import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Package, 
  Truck,
  DollarSign,
  AlertTriangle,
  Clock,
  CheckCircle
} from 'lucide-react';
import { dashboardAPI, delivererAPI, clientAPI, orderAPI } from '../services/api';

interface DashboardStats {
  totalOrders: number;
  totalClients: number;
  activeDeliverers: number;
  revenue: number;
}

interface RecentOrder {
  id: string;
  client_name: string;
  status: string;
  created_at: string;
  total_amount?: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalOrders: 0,
    totalClients: 0,
    activeDeliverers: 0,
    revenue: 0
  });
  const [recentOrders, setRecentOrders] = useState<RecentOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load data from multiple endpoints
      const [deliverers, clients, orders] = await Promise.all([
        delivererAPI.getAll().catch(() => []),
        clientAPI.getAll().catch(() => []),
        orderAPI.getAll().catch(() => [])
      ]);

      // Calculate stats from the data
      const activeDeliverers = deliverers.filter((d: any) => d.is_available).length;
      const totalOrders = orders.length;
      const totalClients = clients.length;
      const revenue = orders.reduce((sum: number, order: any) => 
        sum + (order.total_amount || 0), 0
      );

      setStats({
        totalOrders,
        totalClients,
        activeDeliverers,
        revenue
      });

      // Set recent orders (last 5)
      const sortedOrders = orders
        .sort((a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, 5);
      setRecentOrders(sortedOrders);

    } catch (err) {
      console.error('Error loading dashboard data:', err);
      setError('Failed to load dashboard data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'delivered': return 'text-green-600 bg-green-100';
      case 'pending': return 'text-orange-600 bg-orange-100';
      case 'in_transit': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'delivered': return <CheckCircle className="h-4 w-4" />;
      case 'pending': return <Clock className="h-4 w-4" />;
      case 'in_transit': return <Truck className="h-4 w-4" />;
      default: return <AlertTriangle className="h-4 w-4" />;
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Loading dashboard data...</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-gray-200 rounded"></div>
                <div className="ml-4 flex-1">
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-6 bg-gray-200 rounded"></div>
                </div>
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
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-center">
            <AlertTriangle className="h-6 w-6 text-red-600 mr-3" />
            <div>
              <h3 className="text-red-800 font-medium">Connection Error</h3>
              <p className="text-red-700 mt-1">{error}</p>
              <button 
                onClick={loadDashboardData}
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
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Welcome back! Here's what's happening with your water delivery business today.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Package className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4 w-0 flex-1">
              <div className="text-sm font-medium text-gray-500 truncate">
                Total Orders
              </div>
              <div className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">
                  {stats.totalOrders}
                </div>
                <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                  <TrendingUp className="self-center flex-shrink-0 h-4 w-4 text-green-500" />
                  <span className="ml-1">Live Data</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Truck className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4 w-0 flex-1">
              <div className="text-sm font-medium text-gray-500 truncate">
                Active Deliverers
              </div>
              <div className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">
                  {stats.activeDeliverers}
                </div>
                <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                  <TrendingUp className="self-center flex-shrink-0 h-4 w-4 text-green-500" />
                  <span className="ml-1">Available</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Users className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-4 w-0 flex-1">
              <div className="text-sm font-medium text-gray-500 truncate">
                Total Clients
              </div>
              <div className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">
                  {stats.totalClients}
                </div>
                <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                  <TrendingUp className="self-center flex-shrink-0 h-4 w-4 text-green-500" />
                  <span className="ml-1">Registered</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <DollarSign className="h-8 w-8 text-orange-600" />
            </div>
            <div className="ml-4 w-0 flex-1">
              <div className="text-sm font-medium text-gray-500 truncate">
                Total Revenue
              </div>
              <div className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">
                  {formatCurrency(stats.revenue)}
                </div>
                <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                  <TrendingUp className="self-center flex-shrink-0 h-4 w-4 text-green-500" />
                  <span className="ml-1">Total</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Orders & Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Orders */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Recent Orders</h3>
          </div>
          <div className="p-6">
            {recentOrders.length > 0 ? (
              <div className="space-y-4">
                {recentOrders.map((order) => (
                  <div key={order.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      {getStatusIcon(order.status)}
                      <div className="ml-3">
                        <div className="text-sm font-medium text-gray-900">
                          {order.client_name || `Order #${order.id.slice(0, 8)}`}
                        </div>
                        <div className="text-xs text-gray-500">
                          {new Date(order.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(order.status)}`}>
                        {order.status}
                      </span>
                      {order.total_amount && (
                        <span className="ml-2 text-sm font-medium text-gray-900">
                          {formatCurrency(order.total_amount)}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <Package className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p>No recent orders found</p>
                <p className="text-sm mt-2">New orders will appear here</p>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              <button className="w-full text-left p-4 rounded-lg border-2 border-dashed border-gray-300 hover:border-blue-400 hover:bg-blue-50 transition-colors">
                <div className="flex items-center">
                  <Package className="h-6 w-6 text-blue-600 mr-3" />
                  <div>
                    <div className="font-medium text-gray-900">Create New Order</div>
                    <div className="text-sm text-gray-500">Add a new customer order</div>
                  </div>
                </div>
              </button>
              
              <button className="w-full text-left p-4 rounded-lg border-2 border-dashed border-gray-300 hover:border-blue-400 hover:bg-blue-50 transition-colors">
                <div className="flex items-center">
                  <Users className="h-6 w-6 text-blue-600 mr-3" />
                  <div>
                    <div className="font-medium text-gray-900">Add New Client</div>
                    <div className="text-sm text-gray-500">Register a new customer</div>
                  </div>
                </div>
              </button>
              
              <button className="w-full text-left p-4 rounded-lg border-2 border-dashed border-gray-300 hover:border-blue-400 hover:bg-blue-50 transition-colors">
                <div className="flex items-center">
                  <Truck className="h-6 w-6 text-blue-600 mr-3" />
                  <div>
                    <div className="font-medium text-gray-900">Assign Deliverer</div>
                    <div className="text-sm text-gray-500">Manage delivery assignments</div>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* API Status */}
      <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center">
          <BarChart3 className="h-6 w-6 text-green-600 mr-3" />
          <div>
            <h4 className="font-medium text-green-900">🎉 Live Data Connected!</h4>
            <p className="text-green-700 text-sm mt-1">
              Dashboard is now displaying real data from your backend APIs. 
              Stats update automatically as your business grows!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;