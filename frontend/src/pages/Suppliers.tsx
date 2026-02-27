import React, { useState, useEffect } from 'react';
import { SupplierAPI } from '../services/api';
import { Supplier } from '../types/supplier';
import SupplierTable from '../components/SupplierTable';
import SupplierForm from '../components/SupplierForm';
import { Plus, X, Users } from 'lucide-react';

const SuppliersPage = () => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await SupplierAPI.getAll();
      setSuppliers(data);
    } catch (err) { console.error(err); } 
    finally { setLoading(false); }
  };

  const handleAdd = async (data: Partial<Supplier>) => {
    try {
      await SupplierAPI.create(data);
      setShowForm(false);
      loadData();
    } catch (err) { alert("Erreur d'ajout"); }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm("Supprimer ce fournisseur ?")) {
      await SupplierAPI.delete(id);
      loadData();
    }
  };

  return (
    <div className="p-8 bg-[#f9fafb] min-h-screen font-sans">
      <div className="flex justify-between items-end mb-10">
        <div>
          <h1 className="text-3xl font-black text-gray-900 flex items-center gap-3">
            <Users className="text-blue-600" size={32} /> SUPPLIERS
          </h1>
          <p className="text-gray-500 font-medium ml-11">Gestion de la base de données fournisseurs</p>
        </div>
        <button 
          onClick={() => setShowForm(!showForm)}
          className={`flex items-center gap-2 px-6 py-3 rounded-2xl font-bold transition-all ${
            showForm ? 'bg-white text-gray-500 border border-gray-200' : 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-100'
          }`}
        >
          {showForm ? <><X size={20} /> FERMER</> : <><Plus size={20} /> Add Supplier</>}
        </button>
      </div>

      {showForm && (
        <div className="mb-10 animate-in slide-in-from-top-4 duration-300">
          <SupplierForm onSubmit={handleAdd} onCancel={() => setShowForm(false)} />
        </div>
      )}

      {loading ? (
        <div className="py-20 text-center text-gray-400 font-medium">Synchronisation avec le serveur...</div>
      ) : (
        <SupplierTable 
          suppliers={suppliers} 
          onDelete={handleDelete} 
          onEdit={(s) => console.log(s)} 
          onView={(id) => console.log(id)} 
        />
      )}
    </div>
  );
};

export default SuppliersPage;