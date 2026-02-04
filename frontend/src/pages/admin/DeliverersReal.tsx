import React, { useState, useEffect } from 'react';
import { delivererAPI } from '../../services/api';

interface Deliverer {
  id: string;
  name: string;
  employee_id: string;
  email?: string;
  phone_number?: string;
  territory?: string;
  is_available: boolean;
  vehicle_info?: {
    make?: string;
    model?: string;
    plate_number?: string;
  };
  hire_date?: string;
  created_at: string;
}

const DeliverersPage: React.FC = () => {
  const [deliverers, setDeliverers] = useState<Deliverer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch deliverers when component mounts
  useEffect(() => {
    fetchDeliverers();
  }, []);

  const fetchDeliverers = async () => {
    try {
      setLoading(true);
      const data = await delivererAPI.getAll();
      setDeliverers(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch deliverers. Make sure the backend is running.');
      console.error('Error fetching deliverers:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div>
        <div className="md:flex md:items-center md:justify-between mb-8">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Deliverers
            </h2>
          </div>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <div className="text-center py-8">
            <p className="text-gray-500">Loading deliverers...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <div className="md:flex md:items-center md:justify-between mb-8">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Deliverers
            </h2>
          </div>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <div className="text-center py-8">
            <p className="text-red-500">{error}</p>
            <button 
              onClick={fetchDeliverers}
              className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="md:flex md:items-center md:justify-between mb-8">
        <div className="flex-1 min-w-0">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            Deliverers
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Manage your delivery staff
          </p>
        </div>
        <div className="mt-4 flex md:mt-0 md:ml-4">
          <button
            type="button"
            className="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Add Deliverer
          </button>
        </div>
      </div>

      {/* Deliverers List */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        {deliverers.length === 0 ? (
          <div className="px-4 py-5 sm:p-6">
            <div className="text-center py-8">
              <p className="text-gray-500">No deliverers found. Add your first deliverer!</p>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Deliverer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contact
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Territory
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Vehicle
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {deliverers.map((deliverer) => (
                  <tr key={deliverer.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <span className="text-sm font-medium text-blue-700">
                              {deliverer.name.charAt(0)}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {deliverer.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            ID: {deliverer.employee_id}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{deliverer.email || 'N/A'}</div>
                      <div className="text-sm text-gray-500">{deliverer.phone_number || 'N/A'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{deliverer.territory || 'N/A'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {deliverer.vehicle_info ? 
                          `${deliverer.vehicle_info.make} ${deliverer.vehicle_info.model}` : 
                          'N/A'
                        }
                      </div>
                      <div className="text-sm text-gray-500">
                        {deliverer.vehicle_info?.plate_number || ''}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        deliverer.is_available 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {deliverer.is_available ? 'Available' : 'Busy'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button className="text-blue-600 hover:text-blue-900 mr-4">
                        Edit
                      </button>
                      <button className="text-red-600 hover:text-red-900">
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Summary Stats */}
      {deliverers.length > 0 && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-6 rounded-lg shadow border">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Total Deliverers
            </h3>
            <p className="text-3xl font-bold text-blue-600">{deliverers.length}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow border">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Available
            </h3>
            <p className="text-3xl font-bold text-green-600">
              {deliverers.filter(d => d.is_available).length}
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow border">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Busy
            </h3>
            <p className="text-3xl font-bold text-red-600">
              {deliverers.filter(d => !d.is_available).length}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default DeliverersPage;