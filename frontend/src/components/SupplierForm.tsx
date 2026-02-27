import React, { useState } from 'react';
import { Supplier } from '../types/supplier';

interface Props {
  onSubmit: (data: Partial<Supplier>) => void;
  onCancel: () => void;
}

const SupplierForm: React.FC<Props> = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone_number: '',
    address: '',
    is_active: true
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
      <h3 className="text-lg font-bold mb-5 text-gray-800">Add Supplier</h3>
      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-gray-500 uppercase tracking-tight">Nom *</label>
          <input required className="p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ex: Pizza Hut" onChange={e => setFormData({...formData, name: e.target.value})} />
        </div>
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-gray-500 uppercase tracking-tight">Email</label>
          <input type="email" className="p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="email@fournisseur.com" onChange={e => setFormData({...formData, email: e.target.value})} />
        </div>
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-gray-500 uppercase tracking-tight">Téléphone</label>
          <input className="p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="+216 ..." onChange={e => setFormData({...formData, phone_number: e.target.value})} />
        </div>
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-gray-500 uppercase tracking-tight">Adresse</label>
          <input className="p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ex: Rue 123, Tunis" onChange={e => setFormData({...formData, address: e.target.value})} />
        </div>
        <div className="md:col-span-2 flex justify-end gap-3 pt-2">
          <button type="button" onClick={onCancel} className="px-5 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">Annuler</button>
          <button type="submit" className="px-5 py-2 text-sm font-bold bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-md transition-all">Enregistrer</button>
        </div>
      </form>
    </div>
  );
};

export default SupplierForm;