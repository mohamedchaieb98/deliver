import React, { useState } from 'react';
import DeliverersReal from './components/DeliverersReal.tsx';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');

  const renderPage = () => {
    switch(currentPage) {
      case 'deliverers':
        // Now showing REAL deliverer data from API
        return <DeliverersReal />;
      case 'dashboard':
      default:
        return (
          <div style={{ padding: '32px' }}>
            <h1 style={{ 
              fontSize: '30px', 
              fontWeight: 'bold', 
              color: '#111827',
              marginBottom: '32px'
            }}>
              Water Delivery Management System
            </h1>
            <div style={{ 
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '24px',
              marginBottom: '32px'
            }}>
              <div style={{ 
                background: 'white',
                padding: '24px',
                borderRadius: '8px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                border: '1px solid #e5e7eb'
              }}>
                <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>Dashboard</h3>
                <p style={{ color: '#6b7280', marginBottom: '16px' }}>View system overview</p>
                <span style={{ fontSize: '14px', color: '#059669' }}>✓ You are here</span>
              </div>
              <div 
                style={{ 
                  background: 'white',
                  padding: '24px',
                  borderRadius: '8px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                  border: '1px solid #e5e7eb',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onClick={() => setCurrentPage('deliverers')}
                onMouseOver={e => e.target.style.background = '#eff6ff'}
                onMouseOut={e => e.target.style.background = 'white'}
              >
                <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>🚚 Deliverers</h3>
                <p style={{ color: '#6b7280', marginBottom: '16px' }}>Manage delivery staff</p>
                <span style={{ fontSize: '14px', color: '#2563eb', fontWeight: '600' }}>
                  Click to view REAL API data →
                </span>
              </div>
              <div style={{ 
                background: 'white',
                padding: '24px',
                borderRadius: '8px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                border: '1px solid #e5e7eb'
              }}>
                <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>Orders</h3>
                <p style={{ color: '#6b7280', marginBottom: '16px' }}>Manage customer orders</p>
                <span style={{ fontSize: '14px', color: '#9ca3af' }}>Coming soon</span>
              </div>
            </div>
            
            <div style={{ 
              background: '#f0f9ff',
              border: '1px solid #7dd3fc',
              borderRadius: '8px',
              padding: '16px'
            }}>
              <h4 style={{ color: '#0369a1', margin: '0 0 8px 0', fontWeight: '600' }}>
                🎉 System Status
              </h4>
              <p style={{ color: '#0284c7', margin: '0 0 4px 0' }}>
                Frontend and Backend are connected!
              </p>
              <p style={{ color: '#0284c7', margin: '0 0 8px 0' }}>
                Backend API: <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
                  http://localhost:8000/docs
                </a>
              </p>
              <p style={{ color: '#0284c7', margin: 0 }}>
                <strong>🚀 Ready:</strong> Click "Deliverers" above to see live database data!
              </p>
            </div>
          </div>
        );
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f3f4f6' }}>
      {/* Navigation */}
      <nav style={{ 
        background: 'white', 
        boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
        borderBottom: '1px solid #e5e7eb'
      }}>
        <div style={{ 
          maxWidth: '1280px',
          margin: '0 auto',
          padding: '0 16px',
          display: 'flex',
          justifyContent: 'space-between',
          height: '64px',
          alignItems: 'center'
        }}>
          <h1 style={{ fontSize: '20px', fontWeight: 'bold', color: '#2563eb', margin: 0 }}>
            💧 Water Delivery System
          </h1>
          <div style={{ display: 'flex', gap: '16px' }}>
            <button
              onClick={() => setCurrentPage('dashboard')}
              style={{
                padding: '8px 12px',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '500',
                border: 'none',
                cursor: 'pointer',
                background: currentPage === 'dashboard' ? '#dbeafe' : 'transparent',
                color: currentPage === 'dashboard' ? '#1d4ed8' : '#6b7280'
              }}
            >
              📊 Dashboard
            </button>
            <button
              onClick={() => setCurrentPage('deliverers')}
              style={{
                padding: '8px 12px',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '500',
                border: 'none',
                cursor: 'pointer',
                background: currentPage === 'deliverers' ? '#dbeafe' : 'transparent',
                color: currentPage === 'deliverers' ? '#1d4ed8' : '#6b7280'
              }}
            >
              🚚 Deliverers
            </button>
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <main>
        {renderPage()}
      </main>
    </div>
  );
}

export default App;