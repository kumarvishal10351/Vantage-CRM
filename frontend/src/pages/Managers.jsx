import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { managersApi } from '../api/client';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';

export const Managers = () => {
  const navigate = useNavigate();
  const [managers, setManagers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await managersApi.list();
      setManagers(res.data || []);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch sales managers directory.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Sales Organization</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Managers</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Sales Management Leadership
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              Regional sales leadership hierarchy, team sizes, and cumulative revenue performance.
            </p>
          </div>
        </div>
      </div>

      {/* Managers Grid */}
      {loading ? (
        <LoadingState message="Loading sales leadership team..." />
      ) : error ? (
        <ErrorState message={error} onRetry={loadData} />
      ) : managers.length === 0 ? (
        <EmptyState title="No managers found" icon="supervisor_account" />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-space-lg">
          {managers.map((mgr) => (
            <div
              key={mgr.manager}
              onClick={() => navigate(`/managers/${encodeURIComponent(mgr.manager)}`)}
              className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs hover:border-primary-container/40 transition-all cursor-pointer flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-space-sm">
                    <div className="w-10 h-10 rounded-full bg-primary-container text-on-primary flex items-center justify-center font-bold text-sm shadow-xs">
                      {mgr.manager.substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                      <h3 className="font-headline-sm text-headline-sm text-on-surface">{mgr.manager}</h3>
                      <span className="text-xs text-secondary">{mgr.regional_office}</span>
                    </div>
                  </div>
                  <span className="px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold bg-surface-container text-on-surface">
                    {mgr.total_agents} Reps
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-space-sm mt-space-lg pt-space-sm border-t border-outline-variant/20">
                  <div>
                    <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">Won Revenue</span>
                    <span className="font-headline-sm text-headline-sm font-bold text-on-surface tnum">
                      ${Math.round(mgr.won_revenue || 0).toLocaleString()}
                    </span>
                  </div>
                  <div>
                    <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">Win Rate</span>
                    <span className="font-headline-sm text-headline-sm font-bold text-tertiary-container tnum">
                      {mgr.win_rate !== undefined ? `${mgr.win_rate.toFixed(1)}%` : '—'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-space-md pt-space-xs border-t border-outline-variant/20 flex items-center justify-between text-xs text-primary-container font-semibold">
                <span>View Leadership Rollup</span>
                <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Managers;
