import React, { useState, useEffect } from 'react';
import { SupplierAPI } from '../services/api';
import { Supplier } from '../types/supplier';
import SupplierTable from '../components/SupplierTable';
import SupplierForm from '../components/SupplierForm';
import { Plus, X, Users, Search, Building, Mail, Phone, MapPin, Edit, Trash2, Eye } from 'lucide-react';

const SuppliersPage = () => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState<Supplier | undefined>();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [viewSupplier, setViewSupplier] = useState<Supplier | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await SupplierAPI.getAll();
      setSuppliers(data);
    } catch (err) {
      console.error('Error loading suppliers:', err);
      setError('Failed to load suppliers. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (supplierData: Partial<Supplier>) => {
    try {
      setIsSubmitting(true);
      
      if (editingSupplier) {
        // Update existing supplier
        const updatedSupplier = await SupplierAPI.update(editingSupplier.id, supplierData);
        setSuppliers(prev => prev.map(supplier => 
          supplier.id === editingSupplier.id ? updatedSupplier : supplier
        ));
        setEditingSupplier(undefined);
      } else {
        // Create new supplier
        const newSupplier = await SupplierAPI.create(supplierData);
        setSuppliers(prev => [newSupplier, ...prev]);
      }
      setShowForm(false);
    } catch (error) {
      console.error('Error saving supplier:', error);
      throw error;
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (supplierId: string) => {
    try {
      await SupplierAPI.delete(supplierId);
      setSuppliers(prev => prev.filter(supplier => supplier.id !== supplierId));
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Error deleting supplier:', error);
    }
  };

  const openCreateForm = () => {
    setEditingSupplier(undefined);
    setShowForm(true);
  };

  const openEditForm = (supplier: Supplier) => {
    setEditingSupplier(supplier);
    setShowForm(true);
  };

  const closeForm = () => {
    setShowForm(false);
    setEditingSupplier(undefined);
  };

    // Filter suppliers based on search and status
  const filteredSuppliers = suppliers.filter(supplier => {
    const matchesSearch = supplier.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         supplier.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         supplier.address?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || 
                         (statusFilter === 'active' && supplier.is_active) ||
                         (statusFilter === 'inactive' && !supplier.is_active);
    
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return (
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Suppliers</h1>
          <p className="text-gray-600 mt-2">Loading suppliers...</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gray-200 rounded-full"></div>
                <div className="ml-4 flex-1">
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="h-3 bg-gray-200 rounded"></div>
                <div className="h-3 bg-gray-200 rounded w-3/4"></div>
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
          <h1 className="text-3xl font-bold text-gray-900">Suppliers</h1>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-center">
            <Users className="h-6 w-6 text-red-600 mr-3" />
            <div>
              <h3 className="text-red-800 font-medium">Connection Error</h3>
              <p className="text-red-700 mt-1">{error}</p>
              <button 
                onClick={loadData}
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
            <h1 className="text-3xl font-bold text-gray-900">Suppliers</h1>
            <p className="text-gray-600 mt-2">
              Manage your supplier database • {suppliers.length} total suppliers
            </p>
          </div>
          <button 
            onClick={openCreateForm}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Supplier
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="text-2xl font-bold text-gray-900">{suppliers.length}</div>
          <div className="text-sm text-gray-600">Total Suppliers</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="text-2xl font-bold text-green-600">
            {suppliers.filter(s => s.is_active).length}
          </div>
          <div className="text-sm text-gray-600">Active</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="text-2xl font-bold text-gray-600">
            {suppliers.filter(s => !s.is_active).length}
          </div>
          <div className="text-sm text-gray-600">Inactive</div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Search suppliers by name, email, or address..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
          <select 
            value={statusFilter} 
            onChange={(e) => setStatusFilter(e.target.value as 'all' | 'active' | 'inactive')}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </div>

      {/* Suppliers Grid */}
      {filteredSuppliers.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
          <Users className="mx-auto h-24 w-24 text-gray-400 mb-6" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {suppliers.length === 0 ? 'No suppliers found' : 'No matching suppliers'}
          </h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            {suppliers.length === 0 
              ? 'Get started by adding your first supplier to the system.'
              : 'Try adjusting your search or filter criteria.'
            }
          </p>
          {suppliers.length === 0 && (
            <button 
              onClick={openCreateForm}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Add Your First Supplier
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSuppliers.map((supplier) => (
            <div key={supplier.id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow">
              {/* Supplier Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                    <Building className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="font-semibold text-gray-900">{supplier.name}</h3>
                    <span className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${
                      supplier.is_active 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {supplier.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => setViewSupplier(supplier)}
                    className="text-gray-600 hover:text-gray-800 transition-colors"
                    title="View details"
                  >
                    <Eye className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => openEditForm(supplier)}
                    className="text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => setDeleteConfirm(supplier.id)}
                    className="text-red-600 hover:text-red-800 transition-colors"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {/* Supplier Details */}
              <div className="space-y-2 text-sm text-gray-600">
                {supplier.email && (
                  <div className="flex items-center">
                    <Mail className="h-4 w-4 mr-2" />
                    {supplier.email}
                  </div>
                )}
                {supplier.phone_number && (
                  <div className="flex items-center">
                    <Phone className="h-4 w-4 mr-2" />
                    {supplier.phone_number}
                  </div>
                )}
                {supplier.address && (
                  <div className="flex items-center">
                    <MapPin className="h-4 w-4 mr-2" />
                    <span className="truncate">{supplier.address}</span>
                  </div>
                )}
                <div className="text-xs text-gray-400 pt-2">
                  Added {new Date(supplier.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Supplier Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 max-h-screen overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  {editingSupplier ? 'Edit Supplier' : 'Add New Supplier'}
                </h3>
                <button
                  onClick={closeForm}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              <SupplierForm 
                supplier={editingSupplier}
                onSubmit={handleSave} 
                onCancel={closeForm}
                isLoading={isSubmitting}
              />
            </div>
          </div>
        </div>
      )}

      {/* View Supplier Modal */}
      {viewSupplier && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 max-h-screen overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  Supplier Details
                </h3>
                <button
                  onClick={() => setViewSupplier(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                    <Building className="h-8 w-8 text-blue-600" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">{viewSupplier.name}</h2>
                    <span className={`inline-block px-3 py-1 text-sm font-medium rounded-full ${
                      viewSupplier.is_active 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {viewSupplier.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
                
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {viewSupplier.email && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Email</label>
                      <div className="mt-1 flex items-center">
                        <Mail className="h-4 w-4 mr-2 text-gray-400" />
                        <a href={`mailto:${viewSupplier.email}`} className="text-blue-600 hover:underline">
                          {viewSupplier.email}
                        </a>
                      </div>
                    </div>
                  )}
                  
                  {viewSupplier.phone_number && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Phone</label>
                      <div className="mt-1 flex items-center">
                        <Phone className="h-4 w-4 mr-2 text-gray-400" />
                        <a href={`tel:${viewSupplier.phone_number}`} className="text-blue-600 hover:underline">
                          {viewSupplier.phone_number}
                        </a>
                      </div>
                    </div>
                  )}
                  
                  {viewSupplier.contact_person && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Contact Person</label>
                      <div className="mt-1">{viewSupplier.contact_person}</div>
                    </div>
                  )}
                </div>
                
                {viewSupplier.address && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Address</label>
                    <div className="mt-1 flex items-start">
                      <MapPin className="h-4 w-4 mr-2 text-gray-400 mt-0.5" />
                      <span>{viewSupplier.address}</span>
                    </div>
                  </div>
                )}
                
                <div className="pt-4 border-t border-gray-200">
                  <div className="text-sm text-gray-500">
                    Added on {new Date(viewSupplier.created_at).toLocaleDateString()}
                  </div>
                </div>
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
                Delete Supplier
              </h3>
              <p className="text-gray-600 mb-6">
                Are you sure you want to delete this supplier? This action cannot be undone.
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

export default SuppliersPage;