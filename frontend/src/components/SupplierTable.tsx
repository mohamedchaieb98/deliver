import React from 'react';
import { Supplier } from '../types/supplier';
import { Eye, Edit2, Trash2, Mail, Phone, MapPin } from 'lucide-react';

interface Props {
  suppliers: Supplier[];
  onDelete: (id: string) => void;
  onEdit: (supplier: Supplier) => void;
  onView: (id: string) => void;
}

const SupplierTable: React.FC<Props> = ({ suppliers, onDelete, onEdit, onView }) => (
  <div className="overflow-x-auto bg-white rounded-lg border border-gray-100 shadow-sm">
    <table className="w-full text-left border-collapse">
      <thead className="bg-gray-50 border-b">
        <tr>
          <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Fournisseur</th>
          <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Contact</th>
          <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Statut</th>
          <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Actions</th>
        </tr>
      </thead>
      <tbody>
        {suppliers.map((s) => (
          <tr key={s.id} className="hover:bg-gray-50 border-b border-gray-50 transition-colors">
            {/* Nom + Adresse */}
            <td className="p-4">
              <div className="flex items-center">
                <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center mr-3 font-bold shadow-sm">
                  {s.name.charAt(0).toUpperCase()}
                </div>
                <div>
                  <div className="font-semibold text-gray-800 text-sm">{s.name}</div>
                  <div className="flex items-center text-xs text-gray-400 mt-0.5">
                    <MapPin size={12} className="mr-1" /> {s.address || 'N/A'}
                  </div>
                </div>
              </div>
            </td>

            {/* Contact (Mail + Phone) */}
            <td className="p-4">
              <div className="flex items-center text-sm text-gray-700">
                <Mail size={14} className="mr-2 text-blue-500" /> {s.email || 'N/A'}
              </div>
              <div className="flex items-center text-xs text-gray-500 mt-1">
                <Phone size={14} className="mr-2 text-green-500" /> {s.phone_number || 'N/A'}
              </div>
            </td>

            {/* Statut */}
            <td className="p-4">
              <div className="flex items-center">
                <div className={`w-2 h-2 rounded-full mr-2 ${s.is_active ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${s.is_active ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                  {s.is_active ? 'Actif' : 'Inactif'}
                </span>
              </div>
            </td>

            {/* Actions */}
            <td className="p-4 text-right">
              <div className="flex justify-end gap-1">
                <button onClick={() => onView(s.id)} className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors" title="Voir"><Eye size={18} /></button>
                <button onClick={() => onEdit(s)} className="p-2 text-gray-400 hover:text-amber-600 hover:bg-amber-50 rounded transition-colors" title="Modifier"><Edit2 size={18} /></button>
                <button onClick={() => onDelete(s.id)} className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors" title="Supprimer"><Trash2 size={18} /></button>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export default SupplierTable;