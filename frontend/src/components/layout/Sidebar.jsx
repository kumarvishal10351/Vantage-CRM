import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';

const navSections = [
  {
    title: 'Workspace',
    items: [
      { name: 'Overview', path: '/', icon: 'dashboard' },
      { name: 'Pipeline', path: '/pipeline', icon: 'view_kanban' },
      { name: 'Opportunities', path: '/opportunities', icon: 'monetization_on' },
      { name: 'Accounts', path: '/accounts', icon: 'corporate_fare' },
      { name: 'Priorities', path: '/priorities', icon: 'flag' },
      { name: 'Work Queue', path: '/workqueue', icon: 'checklist' },
    ],
  },
  {
    title: 'Sales Organization',
    items: [
      { name: 'Sales Agents', path: '/agents', icon: 'support_agent' },
      { name: 'Managers', path: '/managers', icon: 'supervisor_account' },
      { name: 'Products', path: '/products', icon: 'inventory_2' },
    ],
  },
  {
    title: 'Operations',
    items: [
      { name: 'Aging Analysis', path: '/aging', icon: 'hourglass_empty' },
      { name: 'Performance', path: '/performance', icon: 'analytics' },
    ],
  },
];

const footerItems = [
  { name: 'Settings', path: '/settings', icon: 'settings' },
  { name: 'Help & Docs', path: '/help-docs', icon: 'menu_book' },
];

export const Sidebar = () => {
  const location = useLocation();

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-surface-container-lowest border-r border-outline-variant/40 z-50 flex flex-col justify-between select-none">
      <div className="flex flex-col flex-1 min-h-0">
        {/* Logo / Header */}
        <div className="h-14 px-space-base flex items-center gap-space-sm border-b border-outline-variant/30">
          <div className="w-8 h-8 rounded bg-primary-container text-on-primary flex items-center justify-center font-bold text-base shadow-xs">
            <span className="material-symbols-outlined text-[20px]">insights</span>
          </div>
          <div className="flex flex-col min-w-0 leading-none">
            <span className="font-headline-sm text-headline-sm tracking-tight text-on-surface truncate">
              Vantage CRM
            </span>
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase tracking-wider mt-space-2xs">
              Sales Cloud • Ops
            </span>
          </div>
        </div>

        {/* Navigation Sections */}
        <div className="flex-1 overflow-y-auto px-space-sm py-space-md">
          {navSections.map((section) => (
            <div key={section.title} className="mb-space-md">
              <div className="px-space-sm py-space-xs font-label-xs-mono text-label-xs-mono uppercase text-secondary tracking-wider">
                {section.title}
              </div>
              <nav className="mt-space-2xs space-y-space-2xs">
                {section.items.map((item) => {
                  const isActive = item.path === '/' 
                    ? location.pathname === '/' 
                    : location.pathname.startsWith(item.path);

                  return (
                    <NavLink
                      key={item.name}
                      to={item.path}
                      className={`flex items-center gap-space-sm px-space-sm py-space-xs rounded-lg font-label-md text-label-md transition-colors ${
                        isActive
                          ? 'bg-primary-container text-on-primary font-semibold shadow-xs'
                          : 'text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface'
                      }`}
                    >
                      <span className="material-symbols-outlined text-[18px]">
                        {item.icon}
                      </span>
                      <span>{item.name}</span>
                    </NavLink>
                  );
                })}
              </nav>
            </div>
          ))}
        </div>
      </div>

      {/* Footer Navigation */}
      <div className="p-space-sm border-t border-outline-variant/30 bg-surface-container-low">
        <nav className="space-y-space-2xs">
          {footerItems.map((item) => {
            const isActive = location.pathname.startsWith(item.path);
            return (
              <NavLink
                key={item.name}
                to={item.path}
                className={`flex items-center gap-space-sm px-space-sm py-space-xs rounded-lg font-label-md text-label-md transition-colors ${
                  isActive
                    ? 'bg-primary-container text-on-primary font-semibold shadow-xs'
                    : 'text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface'
                }`}
              >
                <span className="material-symbols-outlined text-[18px]">
                  {item.icon}
                </span>
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;
