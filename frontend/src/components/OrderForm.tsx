import React, { useState, useEffect } from 'react';
import { X, Save, User, MapPin, Calendar, DollarSign, Plus, Trash2, Package } from 'lucide-react';
import { Order, OrderCreate, OrderUpdate, OrderItem, ORDER_STATUS_OPTIONS } from '../types/order';
import { Client } from '../types/client';
import { clientAPI, delivererAPI } from '../services/api';

interface OrderFormProps {
  order?: Order;
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: OrderCreate | OrderUpdate) => Promise<void>;
  isLoading?: boolean;
}

const OrderForm: React.FC<OrderFormProps> = ({ 
  order, 
  isOpen, 
  onClose, 
  onSave, 
  isLoading = false 
}) => {
  const [clients, setClients] = useState<Client[]>([]);
  const [deliverers, setDeliverers] = useState<any[]>([]);
  const [formData, setFormData] = useState({
    order_number: order?.order_number || `ORD-${Date.now()}`,
    client_id: order?.client_id || '',
    reseller_id: order?.reseller_id || '',
    deliverer_id: order?.deliverer_id || '',
    status: order?.status || 'pending',
    order_date: order?.order_date ? order.order_date.split('T')[0] : new Date().toISOString().split('T')[0],
    delivery_date: order?.delivery_date ? order.delivery_date.split('T')[0] : '',
    delivery_address: order?.delivery_address || '',
    notes: order?.notes || '',
    items: order?.items || [{ product_name: 'Water Bottle', quantity: 1, unit_price: 25.00, total_price: 25.00 }]
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (isOpen) {
      loadClients();
      loadDeliverers();
    }
  }, [isOpen]);

  const loadClients = async () => {
    try {
      const data = await clientAPI.getAll();
      setClients(data.filter((client: Client) => client.is_active));
    } catch (error) {
      console.error('Error loading clients:', error);
    }
  };

  const loadDeliverers = async () => {
    try {
      const data = await delivererAPI.getAll();
      setDeliverers(data.filter((deliverer: any) => deliverer.is_available));
    } catch (error) {
      console.error('Error loading deliverers:', error);
    }
  };

  const calculateTotal = (items: OrderItem[]) => {
    return items.reduce((sum, item) => sum + item.total_price, 0);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log('Form submitted with data:', formData);
    console.log('Items data:', formData.items);
    console.log('Total amount will be:', calculateTotal(formData.items));
    
    // Basic validation
    const newErrors: Record<string, string> = {};
    if (!formData.client_id) newErrors.client_id = 'Client is required';
    if (!formData.delivery_address.trim()) newErrors.delivery_address = 'Delivery address is required';
    if (formData.items.length === 0) newErrors.items = 'At least one item is required';
    
    // Validate items
    formData.items.forEach((item, index) => {
      if (!item.product_name.trim()) {
        newErrors[`item_${index}_product`] = 'Product name is required';
      }
      if (item.quantity <= 0) {
        newErrors[`item_${index}_quantity`] = 'Quantity must be greater than 0';
      }
      if (item.unit_price <= 0) {
        newErrors[`item_${index}_price`] = 'Unit price must be greater than 0';
      }
    });

    console.log('Validation errors:', newErrors);

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const total_amount = calculateTotal(formData.items);
    
    const orderData = {
      ...formData,
      total_amount,
      items: formData.items
    };
    
    console.log('Sending order data:', orderData);

    try {
      await onSave(orderData);
      console.log('Order saved successfully');
      onClose();
      // Reset form
      setFormData({
        order_number: `ORD-${Date.now()}`,
        client_id: '',
        reseller_id: '',
        deliverer_id: '',
        status: 'pending',
        order_date: new Date().toISOString().split('T')[0],
        delivery_date: '',
        delivery_address: '',
        notes: '',
        items: [{ product_name: 'Water Bottle', quantity: 1, unit_price: 25.00, total_price: 25.00 }]
      });
      setErrors({});
    } catch (error) {
      console.error('Error saving order:', error);
      // Show error to user
      setErrors({ general: 'Failed to save order. Please try again.' });
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleItemChange = (index: number, field: keyof OrderItem, value: string | number) => {
    const newItems = [...formData.items];
    newItems[index] = { ...newItems[index], [field]: value };
    
    // Recalculate total price for this item
    if (field === 'quantity' || field === 'unit_price') {
      newItems[index].total_price = newItems[index].quantity * newItems[index].unit_price;
    }
    
    setFormData(prev => ({ ...prev, items: newItems }));
  };

  const addItem = () => {
    setFormData(prev => ({
      ...prev,
      items: [...prev.items, { product_name: 'Water Bottle', quantity: 1, unit_price: 25.00, total_price: 25.00 }]
    }));
  };

  const removeItem = (index: number) => {
    if (formData.items.length > 1) {
      setFormData(prev => ({
        ...prev,
        items: prev.items.filter((_, i) => i !== index)
      }));
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl mx-4 my-8">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            {order ? 'Edit Order' : 'Create New Order'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Client Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <User className="inline h-4 w-4 mr-2" />
                Client *
              </label>
              <select
                name="client_id"
                value={formData.client_id}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  errors.client_id ? 'border-red-500' : 'border-gray-300'
                }`}
              >
                <option value="">Select a client</option>
                {clients.map((client) => (
                  <option key={client.id} value={client.id}>
                    {client.name} {client.company_name && `(${client.company_name})`}
                  </option>
                ))}
              </select>
              {errors.client_id && (
                <p className="text-red-500 text-sm mt-1">{errors.client_id}</p>
              )}
            </div>

            {/* Deliverer Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Package className="inline h-4 w-4 mr-2" />
                Deliverer
              </label>
              <select
                name="deliverer_id"
                value={formData.deliverer_id}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Assign later</option>
                {deliverers.map((deliverer) => (
                  <option key={deliverer.id} value={deliverer.id}>
                    {deliverer.name} - {deliverer.employee_id}
                  </option>
                ))}
              </select>
            </div>

            {/* Reseller Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <User className="inline h-4 w-4 mr-2" />
                Reseller
              </label>
              <select
                name="reseller_id"
                value={formData.reseller_id}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select reseller (optional)</option>
                {clients.map((client) => (
                  <option key={client.id} value={client.id}>
                    {client.name} {client.company_name && `(${client.company_name})`}
                  </option>
                ))}
              </select>
            </div>

            {/* Order Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="inline h-4 w-4 mr-2" />
                Order Date *
              </label>
              <input
                type="date"
                name="order_date"
                value={formData.order_date}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Delivery Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="inline h-4 w-4 mr-2" />
                Delivery Date
              </label>
              <input
                type="date"
                name="delivery_date"
                value={formData.delivery_date}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Status */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                {ORDER_STATUS_OPTIONS.map((status) => (
                  <option key={status.value} value={status.value}>
                    {status.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Delivery Address */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <MapPin className="inline h-4 w-4 mr-2" />
              Delivery Address *
            </label>
            <textarea
              name="delivery_address"
              value={formData.delivery_address}
              onChange={handleChange}
              rows={2}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                errors.delivery_address ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Full delivery address"
            />
            {errors.delivery_address && (
              <p className="text-red-500 text-sm mt-1">{errors.delivery_address}</p>
            )}
          </div>

          {/* Order Items */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <label className="block text-sm font-medium text-gray-700">
                Order Items *
              </label>
              <button
                type="button"
                onClick={addItem}
                className="bg-green-600 text-white px-3 py-1 rounded-lg hover:bg-green-700 transition-colors flex items-center text-sm"
              >
                <Plus className="h-4 w-4 mr-1" />
                Add Item
              </button>
            </div>
            
            <div className="space-y-3">
              {formData.items.map((item, index) => (
                <div key={index} className="grid grid-cols-12 gap-3 items-end">
                  <div className="col-span-5">
                    <input
                      type="text"
                      placeholder="Product name"
                      value={item.product_name}
                      onChange={(e) => handleItemChange(index, 'product_name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div className="col-span-2">
                    <input
                      type="number"
                      placeholder="Qty"
                      value={item.quantity}
                      onChange={(e) => handleItemChange(index, 'quantity', parseInt(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      min="1"
                    />
                  </div>
                  <div className="col-span-2">
                    <input
                      type="number"
                      placeholder="Unit Price"
                      value={item.unit_price}
                      onChange={(e) => handleItemChange(index, 'unit_price', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      min="0"
                      step="0.01"
                    />
                  </div>
                  <div className="col-span-2">
                    <div className="px-3 py-2 bg-gray-50 rounded-lg text-sm font-medium">
                      {formatCurrency(item.total_price)}
                    </div>
                  </div>
                  <div className="col-span-1">
                    {formData.items.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeItem(index)}
                        className="text-red-600 hover:text-red-800 transition-colors"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Total */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex justify-between items-center">
                <span className="text-lg font-medium text-gray-900">Total Amount:</span>
                <span className="text-xl font-bold text-blue-600">
                  {formatCurrency(calculateTotal(formData.items))}
                </span>
              </div>
            </div>
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Notes
            </label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Additional notes or special instructions"
            />
          </div>

          {/* Error Display */}
          {errors.general && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-600 text-sm">{errors.general}</p>
            </div>
          )}

          {/* Buttons */}
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors flex items-center justify-center"
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  {order ? 'Update Order' : 'Create Order'}
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default OrderForm;