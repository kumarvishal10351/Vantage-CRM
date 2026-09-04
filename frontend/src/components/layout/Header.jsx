import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const Header = ({ onSearch }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchSubmit = (e) => {
    if (e.key === 'Enter' && searchTerm.trim()) {
      navigate(`/opportunities?search=${encodeURIComponent(searchTerm.trim())}`);
      if (onSearch) onSearch(searchTerm.trim());
    }
  };

  return (
    <header className="fixed top-0 left-64 right-0 h-14 bg-surface-container-lowest/95 backdrop-blur-md border-b border-outline-variant/30 z-40 flex items-center justify-between px-space-lg select-none">
      <div className="flex items-center gap-space-lg flex-1 max-w-2xl">
        <div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm">
          <span className="font-semibold text-on-surface uppercase tracking-wider">Enterprise</span>
          <span className="text-outline">/</span>
          <span className="truncate text-secondary">Revenue Operations</span>
        </div>
        <div className="relative flex-1 max-w-md">
          <span className="material-symbols-outlined absolute left-space-sm top-1/2 -translate-y-1/2 text-[18px] text-secondary">
            search
          </span>
          <input
            className="w-full h-8 pl-8 pr-14 bg-surface-container-low border border-outline-variant/60 rounded-lg font-body-sm text-body-sm text-on-surface placeholder:text-secondary focus:outline-none focus:border-primary-container"
            placeholder="Search 8,800 opportunities, 85 accounts, products..."
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={handleSearchSubmit}
          />
          <kbd className="absolute right-space-xs top-1/2 -translate-y-1/2 border border-outline-variant/80 bg-surface-container-lowest px-1.5 py-0.5 rounded font-label-xs-mono text-label-xs-mono text-secondary shadow-xs">
            ⌘K
          </kbd>
        </div>
      </div>

      <div className="flex items-center gap-space-md">
        <div className="hidden xl:flex items-center gap-space-xs px-space-sm py-space-2xs bg-surface-container-low rounded border border-outline-variant/30 font-label-xs-mono text-label-xs-mono text-secondary">
          <span className="w-1.5 h-1.5 rounded-full bg-tertiary-container animate-pulse"></span>
          <span>Live Pipeline • 3 Regions Active</span>
        </div>

        <button
          onClick={() => navigate('/opportunities')}
          className="h-8 px-space-md bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md rounded flex items-center gap-space-xs transition-colors shadow-xs"
        >
          <span className="material-symbols-outlined text-[18px]">add</span>
          <span>New Opportunity</span>
        </button>

        <button className="relative p-space-xs text-on-surface-variant hover:text-on-surface rounded-lg hover:bg-surface-container-high transition-colors">
          <span className="material-symbols-outlined text-[20px]">notifications</span>
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-error ring-2 ring-surface-container-lowest"></span>
        </button>

        <div className="h-6 w-px bg-outline-variant/40"></div>

        <div className="flex items-center gap-space-sm">
          <div className="w-8 h-8 rounded-full bg-surface-container-high text-primary font-bold text-xs flex items-center justify-center ring-1 ring-outline-variant/50">
            {user?.username ? user.username.substring(0, 2).toUpperCase() : 'SJ'}
          </div>
          <div className="hidden md:flex flex-col leading-none min-w-0 text-left">
            <span className="font-label-md text-label-md font-semibold text-on-surface truncate">
              {user?.full_name || 'Sarah Jenkins'}
            </span>
            <span className="font-label-xs-mono text-label-xs-mono text-secondary truncate mt-space-2xs max-w-[170px]">
              {user?.role || 'VP Sales Operations'}
            </span>
          </div>
          <button
            onClick={logout}
            className="p-1 rounded text-secondary hover:text-error hover:bg-surface-container transition-colors ml-1"
            title="Sign out"
          >
            <span className="material-symbols-outlined text-[18px]">logout</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
