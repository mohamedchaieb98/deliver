import React from 'react';
import { Plus, Receipt } from 'lucide-react';

const MobileExpenses: React.FC = () => {
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow-sm border p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            Expenses
          </h2>
          <button className="bg-primary-600 text-white p-2 rounded-md">
            <Plus className="h-4 w-4" />
          </button>
        </div>
        
        <div className="text-center py-8">
          <Receipt className="h-12 w-12 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500 mb-4">No expenses recorded today</p>
          <button className="bg-primary-600 text-white py-2 px-4 rounded-md text-sm font-medium">
            Add First Expense
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border p-4">
        <h3 className="font-medium text-gray-900 mb-3">Today's Summary</h3>
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Total Expenses:</span>
            <span className="font-medium">$0.00</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Reimbursable:</span>
            <span className="font-medium">$0.00</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Personal:</span>
            <span className="font-medium">$0.00</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MobileExpenses;