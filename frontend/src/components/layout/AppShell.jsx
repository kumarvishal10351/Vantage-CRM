import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import ErrorBoundary from '../common/ErrorBoundary';

export const AppShell = () => {
  return (
    <div className="min-h-screen bg-background text-on-surface antialiased">
      <Sidebar />
      <div className="pl-64">
        <Header />
        <main className="relative pt-14 min-h-screen px-space-lg py-space-md">
          <ErrorBoundary>
            <Outlet />
          </ErrorBoundary>
        </main>
      </div>
    </div>
  );
};

export default AppShell;
