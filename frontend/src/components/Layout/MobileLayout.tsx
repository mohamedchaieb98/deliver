import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MapPin, Receipt } from 'lucide-react';

interface MobileLayoutProps {
  children: React.ReactNode;
}

const MobileLayout: React.FC<MobileLayoutProps> = ({ children }) => {
  const location = useLocation();

  const navigation = [
    { name: 'Route', href: '/mobile/route', icon: MapPin },
    { name: 'Expenses', href: '/mobile/expenses', icon: Receipt },
  ];

  const isActive = (href: string) => location.pathname === href;

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="px-4 py-3">
          <h1 className="text-lg font-semibold text-gray-900">
            Water Delivery
          </h1>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        <div className="p-4">
          {children}
        </div>
      </main>

      {/* Bottom navigation */}
      <nav className="bg-white border-t border-gray-200">
        <div className="grid grid-cols-2">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`${
                  isActive(item.href)
                    ? 'text-primary-600 bg-primary-50'
                    : 'text-gray-600 hover:text-gray-900'
                } flex flex-col items-center py-3 px-4 text-xs font-medium`}
              >
                <Icon className="h-6 w-6 mb-1" />
                {item.name}
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
};

export default MobileLayout;