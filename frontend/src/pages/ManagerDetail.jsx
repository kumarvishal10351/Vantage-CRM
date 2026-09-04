import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { managersApi, agentsApi } from '../api/client';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

export const ManagerDetail = () => {
  const { name } = useParams();
  const navigate = useNavigate();
  const [manager, setManager] = useState(null);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [mgrRes, agentsRes] = await Promise.all([
          managersApi.getByName(name),
          agentsApi.list(),
        ]);
        setManager(mgrRes.data);
        const teamAgents = (agentsRes.data || []).filter(
          (a) => (a.manager || '').toLowerCase() === (mgrRes.data.manager || name).toLowerCase()
        );
        setAgents(teamAgents);
      } catch (err) {
        console.error(err);
        setError('Failed to fetch sales manager profile.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [name]);

  if (loading) return <LoadingState message="Loading leadership hierarchy..." />;
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <button onClick={() => navigate('/managers')} className="hover:text-on-surface">
            Managers
          </button>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">{manager?.manager}</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div className="flex items-center gap-space-md">
            <div className="w-12 h-12 rounded-xl bg-primary-container text-on-primary flex items-center justify-center font-bold text-xl shadow-xs">
              {manager?.manager?.substring(0, 2).toUpperCase() || 'MG'}
            </div>
            <div>
              <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
                {manager?.manager}
              </h1>
              <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                Regional Director • Regional Office: <strong className="text-on-surface">{manager?.regional_office}</strong>
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/managers')}
            className="h-8 px-space-md bg-surface-container-lowest hover:bg-surface-container text-on-surface font-label-md text-label-md rounded border border-outline-variant/60 flex items-center gap-space-xs transition-colors shadow-xs self-start md:self-auto"
          >
            <span className="material-symbols-outlined text-[16px]">arrow_back</span>
            <span>Back to Managers</span>
          </button>
        </div>
      </div>

      {/* Team Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-space-md mb-space-xl">
        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Team Won Revenue</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum mt-1">
            ${Math.round(manager?.won_revenue || 0).toLocaleString()}
          </div>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Team Win Rate</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-tertiary-container tnum mt-1">
            {manager?.win_rate !== undefined ? `${manager.win_rate.toFixed(1)}%` : '—'}
          </div>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Total Opportunities</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum mt-1">
            {manager?.total_opportunities?.toLocaleString()}
          </div>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Direct Reports</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-primary-container tnum mt-1">
            {agents.length} Reps
          </div>
        </div>
      </div>

      {/* Direct Reports Table */}
      <div className="bg-surface-container-lowest rounded-xl border border-outline-variant/30 shadow-xs overflow-hidden">
        <div className="h-12 px-space-base border-b border-outline-variant/20 flex items-center justify-between bg-surface-container-low/30">
          <h2 className="font-headline-sm text-headline-sm text-on-surface">
            Direct Report Sales Representatives ({agents.length})
          </h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left font-body-sm text-body-sm border-collapse">
            <thead>
              <tr className="border-b border-outline-variant/30 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider">
                <th className="py-2.5 px-3">Sales Agent</th>
                <th className="py-2.5 px-3 text-right">Total Deals</th>
                <th className="py-2.5 px-3 text-right">Won Deals</th>
                <th className="py-2.5 px-3 text-right">Win Rate</th>
                <th className="py-2.5 px-3 text-right">Won Revenue</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/20">
              {agents.map((ag) => (
                <tr
                  key={ag.sales_agent}
                  onClick={() => navigate(`/agents/${encodeURIComponent(ag.sales_agent)}`)}
                  className="hover:bg-surface-container-low/60 transition-colors cursor-pointer"
                >
                  <td className="py-2.5 px-3 font-semibold text-on-surface flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-primary-container/10 text-primary-container flex items-center justify-center font-bold text-xs">
                      {ag.sales_agent.substring(0, 2).toUpperCase()}
                    </div>
                    <span>{ag.sales_agent}</span>
                  </td>
                  <td className="py-2.5 px-3 text-right tnum">{ag.total_opportunities}</td>
                  <td className="py-2.5 px-3 text-right tnum">{ag.won_opportunities}</td>
                  <td className="py-2.5 px-3 text-right tnum font-semibold text-tertiary-container">
                    {ag.win_rate !== undefined ? `${ag.win_rate.toFixed(1)}%` : '—'}
                  </td>
                  <td className="py-2.5 px-3 text-right font-bold text-on-surface tnum">
                    ${Math.round(ag.won_revenue || 0).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ManagerDetail;
