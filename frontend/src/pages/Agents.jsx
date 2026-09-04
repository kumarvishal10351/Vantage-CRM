import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { agentsApi } from '../api/client';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';

export const Agents = () => {
  const navigate = useNavigate();
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await agentsApi.list();
      setAgents(res.data || []);
    } catch (err) {
      console.error(err);
      setError('Failed to load sales agents roster.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const filteredAgents = agents.filter((a) =>
    (a.sales_agent || '').toLowerCase().includes(search.toLowerCase()) ||
    (a.manager || '').toLowerCase().includes(search.toLowerCase()) ||
    (a.regional_office || '').toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Sales Organization</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Sales Agents</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Sales Agents Performance Roster
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              35 sales team representatives (30 active pipeline producers) across 3 regional territories.
            </p>
          </div>
          <div className="relative max-w-xs w-full">
            <span className="material-symbols-outlined absolute left-space-sm top-1/2 -translate-y-1/2 text-[18px] text-secondary">
              search
            </span>
            <input
              type="text"
              className="w-full h-9 pl-9 pr-space-md bg-surface-container-low border border-outline-variant/60 rounded-lg font-body-sm text-body-sm text-on-surface placeholder:text-secondary focus:outline-none focus:border-primary-container"
              placeholder="Search agent, manager, region..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Agents Table */}
      <div className="bg-surface-container-lowest rounded-xl border border-outline-variant/30 shadow-xs overflow-hidden">
        {loading ? (
          <LoadingState message="Loading sales representatives..." />
        ) : error ? (
          <ErrorState message={error} onRetry={loadData} />
        ) : filteredAgents.length === 0 ? (
          <EmptyState title="No agents found" description="No agents match your search term." icon="support_agent" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-body-sm text-body-sm border-collapse">
              <thead>
                <tr className="border-b border-outline-variant/30 bg-surface-container-low/40 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider select-none">
                  <th className="py-2.5 px-3">Sales Agent</th>
                  <th className="py-2.5 px-3">Reporting Manager</th>
                  <th className="py-2.5 px-3">Regional Office</th>
                  <th className="py-2.5 px-3 text-right">Total Deals</th>
                  <th className="py-2.5 px-3 text-right">Won Deals</th>
                  <th className="py-2.5 px-3 text-right">Open Deals</th>
                  <th className="py-2.5 px-3 text-right">Win Rate</th>
                  <th className="py-2.5 px-3 text-right">Won Revenue</th>
                  <th className="py-2.5 px-3 text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant/20">
                {filteredAgents.map((agent) => (
                  <tr
                    key={agent.sales_agent}
                    onClick={() => navigate(`/agents/${encodeURIComponent(agent.sales_agent)}`)}
                    className="hover:bg-surface-container-low/60 transition-colors cursor-pointer"
                  >
                    <td className="py-2.5 px-3 font-semibold text-on-surface flex items-center gap-2">
                      <div className="w-7 h-7 rounded-full bg-primary-container/10 text-primary-container flex items-center justify-center font-bold text-xs">
                        {agent.sales_agent.substring(0, 2).toUpperCase()}
                      </div>
                      <span>{agent.sales_agent}</span>
                    </td>
                    <td className="py-2.5 px-3 text-secondary">{agent.manager}</td>
                    <td className="py-2.5 px-3 text-secondary">{agent.regional_office}</td>
                    <td className="py-2.5 px-3 text-right tnum">{agent.total_opportunities?.toLocaleString()}</td>
                    <td className="py-2.5 px-3 text-right tnum">{agent.won_opportunities?.toLocaleString()}</td>
                    <td className="py-2.5 px-3 text-right tnum font-semibold text-primary-container">
                      {agent.open_opportunities?.toLocaleString() || 0}
                    </td>
                    <td className="py-2.5 px-3 text-right tnum font-semibold text-tertiary-container">
                      {agent.win_rate !== undefined ? `${agent.win_rate.toFixed(1)}%` : '—'}
                    </td>
                    <td className="py-2.5 px-3 text-right font-bold text-on-surface tnum">
                      ${Math.round(agent.won_revenue || 0).toLocaleString()}
                    </td>
                    <td className="py-2.5 px-3 text-center" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => navigate(`/agents/${encodeURIComponent(agent.sales_agent)}`)}
                        className="p-1 rounded text-secondary hover:text-primary-container transition-colors"
                        title="View Rep Profile"
                      >
                        <span className="material-symbols-outlined text-[18px]">visibility</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Agents;
