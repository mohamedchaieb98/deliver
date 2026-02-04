import React from 'react';
import { isMobile } from '../../utils/deviceDetection';
import AdminLayout from './AdminLayout';
import MobileLayout from './MobileLayout';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const mobile = isMobile();

  if (mobile) {
    return <MobileLayout>{children}</MobileLayout>;
  }

  return <AdminLayout>{children}</AdminLayout>;
};

export default Layout;