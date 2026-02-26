import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AdminLayout from './components/Layout/AdminLayout';
import Dashboard from './pages/Dashboard';
import Clients from './pages/Clients';
import Orders from './pages/Orders';
import DeliverersReal from './components/DeliverersReal';

interface PlaceholderPageProps {
  title: string;
}

// Placeholder component for unimplemented pages
const PlaceholderPage: React.FC<PlaceholderPageProps> = ({ title }) => {
  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
        <p className="text-gray-600 mt-2">
          {title} management page coming soon.
        </p>
      </div>
      
      <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
        <div className="text-6xl mb-4">🚧</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          {title} Management Coming Soon
        </h3>
        <p className="text-gray-600 mb-6 max-w-md mx-auto">
          This page is ready for implementation with your backend API.
        </p>
        <div className="space-y-2 text-sm text-gray-500">
          <p>Backend API: /api/v1/{title.toLowerCase()}</p>
          <p>Ready for implementation</p>
        </div>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <AdminLayout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/deliverers" element={<DeliverersReal />} />
        <Route path="/clients" element={<Clients />} />
        <Route path="/orders" element={<Orders />} />
        <Route path="/inventory" element={<PlaceholderPage title="Inventory" />} />
        <Route path="/routes" element={<PlaceholderPage title="Routes" />} />
        <Route path="/expenses" element={<PlaceholderPage title="Expenses" />} />
        <Route path="/suppliers" element={<PlaceholderPage title="Suppliers" />} />
      </Routes>
    </AdminLayout>
  );
};

export default App;