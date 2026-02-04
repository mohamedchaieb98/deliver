import React from 'react';
import { MapPin, Clock, CheckCircle } from 'lucide-react';

const MobileRoute: React.FC = () => {
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow-sm border p-4">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">
          Today's Route
        </h2>
        <p className="text-sm text-gray-600">
          No route assigned for today
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-medium text-gray-900">Route Status</h3>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
            Not Started
          </span>
        </div>
        
        <div className="space-y-3">
          <div className="flex items-center text-sm text-gray-600">
            <MapPin className="h-4 w-4 mr-2" />
            <span>0 stops total</span>
          </div>
          <div className="flex items-center text-sm text-gray-600">
            <Clock className="h-4 w-4 mr-2" />
            <span>0 completed</span>
          </div>
          <div className="flex items-center text-sm text-gray-600">
            <CheckCircle className="h-4 w-4 mr-2" />
            <span>0 remaining</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border p-4">
        <h3 className="font-medium text-gray-900 mb-3">Quick Actions</h3>
        <div className="space-y-2">
          <button className="w-full bg-primary-600 text-white py-2 px-4 rounded-md text-sm font-medium">
            Start Route
          </button>
          <button className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-md text-sm font-medium">
            View Navigation
          </button>
        </div>
      </div>
    </div>
  );
};

export default MobileRoute;