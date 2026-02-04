import React, { useState, useEffect } from 'react';

// Types for TypeScript
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
    capacity?: string;
  };
  hire_date?: string;
  created_at: string;
}

const DeliverersReal = () => {
  const [deliverers, setDeliverers] = useState<Deliverer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch deliverers from API
  useEffect(() => {
    fetchDeliverers();
  }, []);

  const fetchDeliverers = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('http://localhost:8000/api/v1/deliverers');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setDeliverers(data);
    } catch (err) {
      console.error('Error fetching deliverers:', err);
      setError('Failed to fetch deliverers. Make sure the backend is running on localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '32px' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '24px' }}>
          Deliverers
        </h2>
        <div style={{ 
          background: 'white',
          borderRadius: '8px',
          padding: '48px',
          textAlign: 'center',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}>
          <div style={{ fontSize: '16px', color: '#6b7280' }}>
            Loading deliverers from API...
          </div>
          <div style={{ marginTop: '16px', fontSize: '14px', color: '#9ca3af' }}>
            Connecting to http://localhost:8000/api/v1/deliverers
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '32px' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '24px' }}>
          Deliverers
        </h2>
        <div style={{ 
          background: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '8px',
          padding: '24px',
          marginBottom: '16px'
        }}>
          <h3 style={{ color: '#dc2626', margin: '0 0 8px 0' }}>Connection Error</h3>
          <p style={{ color: '#b91c1c', margin: '0 0 16px 0' }}>{error}</p>
          <button 
            onClick={fetchDeliverers}
            style={{
              background: '#dc2626',
              color: 'white',
              padding: '8px 16px',
              borderRadius: '6px',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            Retry Connection
          </button>
        </div>
        <div style={{ 
          background: '#f3f4f6',
          borderRadius: '8px',
          padding: '16px',
          fontSize: '14px',
          color: '#6b7280'
        }}>
          <strong>Troubleshooting:</strong>
          <ul style={{ margin: '8px 0 0 20px' }}>
            <li>Make sure your backend is running: <code>uvicorn app.main:app --reload</code></li>
            <li>Check backend is accessible at: <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">http://localhost:8000/docs</a></li>
            <li>Verify you have deliverer data with: <code>python seed_database.py</code></li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: '32px' }}>
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '32px'
      }}>
        <div>
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', margin: '0 0 4px 0' }}>
            Deliverers
          </h2>
          <p style={{ color: '#6b7280', margin: 0 }}>
            Manage your delivery staff • {deliverers.length} total
          </p>
        </div>
        <button style={{
          background: '#2563eb',
          color: 'white',
          padding: '8px 16px',
          borderRadius: '6px',
          border: 'none',
          cursor: 'pointer',
          fontSize: '14px',
          fontWeight: '500'
        }}>
          + Add Deliverer
        </button>
      </div>

      {/* Stats Cards */}
      <div style={{ 
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '16px',
        marginBottom: '32px'
      }}>
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '500', color: '#6b7280', margin: '0 0 4px 0' }}>
            Total Deliverers
          </h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#111827', margin: 0 }}>
            {deliverers.length}
          </p>
        </div>
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '500', color: '#6b7280', margin: '0 0 4px 0' }}>
            Available
          </h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#059669', margin: 0 }}>
            {deliverers.filter(d => d.is_available).length}
          </p>
        </div>
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '500', color: '#6b7280', margin: '0 0 4px 0' }}>
            Busy
          </h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#dc2626', margin: 0 }}>
            {deliverers.filter(d => !d.is_available).length}
          </p>
        </div>
      </div>

      {/* Deliverers Table */}
      <div style={{ 
        background: 'white',
        borderRadius: '8px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        overflow: 'hidden'
      }}>
        {deliverers.length === 0 ? (
          <div style={{ padding: '48px', textAlign: 'center' }}>
            <p style={{ color: '#6b7280', margin: '0 0 16px 0' }}>
              No deliverers found in the database.
            </p>
            <button style={{
              background: '#2563eb',
              color: 'white',
              padding: '8px 16px',
              borderRadius: '6px',
              border: 'none',
              cursor: 'pointer'
            }}>
              Add Your First Deliverer
            </button>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ background: '#f9fafb', borderBottom: '1px solid #e5e7eb' }}>
                <tr>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase' }}>
                    Deliverer
                  </th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase' }}>
                    Contact
                  </th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase' }}>
                    Territory
                  </th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase' }}>
                    Vehicle
                  </th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase' }}>
                    Status
                  </th>
                </tr>
              </thead>
              <tbody>
                {deliverers.map((deliverer, index) => (
                  <tr key={deliverer.id} style={{ 
                    borderBottom: index < deliverers.length - 1 ? '1px solid #e5e7eb' : 'none',
                    '&:hover': { background: '#f9fafb' }
                  }}>
                    <td style={{ padding: '16px' }}>
                      <div style={{ display: 'flex', alignItems: 'center' }}>
                        <div style={{
                          width: '40px',
                          height: '40px',
                          borderRadius: '50%',
                          background: '#dbeafe',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          marginRight: '12px'
                        }}>
                          <span style={{ fontSize: '14px', fontWeight: '500', color: '#1d4ed8' }}>
                            {deliverer.name.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div>
                          <div style={{ fontSize: '14px', fontWeight: '500', color: '#111827' }}>
                            {deliverer.name}
                          </div>
                          <div style={{ fontSize: '12px', color: '#6b7280' }}>
                            ID: {deliverer.employee_id}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td style={{ padding: '16px' }}>
                      <div style={{ fontSize: '14px', color: '#111827' }}>
                        {deliverer.email || 'No email'}
                      </div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>
                        {deliverer.phone_number || 'No phone'}
                      </div>
                    </td>
                    <td style={{ padding: '16px' }}>
                      <div style={{ fontSize: '14px', color: '#111827' }}>
                        {deliverer.territory || 'No territory'}
                      </div>
                    </td>
                    <td style={{ padding: '16px' }}>
                      <div style={{ fontSize: '14px', color: '#111827' }}>
                        {deliverer.vehicle_info ? 
                          `${deliverer.vehicle_info.make || ''} ${deliverer.vehicle_info.model || ''}`.trim() || 'Vehicle info' :
                          'No vehicle'
                        }
                      </div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>
                        {deliverer.vehicle_info?.plate_number || ''}
                      </div>
                    </td>
                    <td style={{ padding: '16px' }}>
                      <span style={{
                        display: 'inline-flex',
                        padding: '4px 8px',
                        fontSize: '12px',
                        fontWeight: '500',
                        borderRadius: '12px',
                        background: deliverer.is_available ? '#dcfce7' : '#fee2e2',
                        color: deliverer.is_available ? '#166534' : '#991b1b'
                      }}>
                        {deliverer.is_available ? 'Available' : 'Busy'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Success Message */}
      <div style={{ 
        marginTop: '24px',
        background: '#f0f9ff',
        border: '1px solid #7dd3fc',
        borderRadius: '8px',
        padding: '16px'
      }}>
        <h4 style={{ color: '#0369a1', margin: '0 0 4px 0', fontSize: '14px', fontWeight: '500' }}>
          🎉 API Connection Successful!
        </h4>
        <p style={{ color: '#0284c7', margin: 0, fontSize: '14px' }}>
          Successfully loaded {deliverers.length} deliverers from your backend database.
        </p>
      </div>
    </div>
  );
};

export default DeliverersReal;