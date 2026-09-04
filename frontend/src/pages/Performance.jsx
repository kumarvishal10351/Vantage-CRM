import React, { useEffect, useState } from 'react';
import { pipelineApi } from '../api/client';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

export const Performance = () => {
  const [regions, setRegions] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [regRes, sumRes] = await Promise.all([
          pipelineApi.getRegions(),
          pipelineApi.getSummary(),
        ]);
        setRegions(regRes.data || []);
        setSummary(sumRes.data);
      } catch (err) {
        console.error(err);
        setError('Failed to load sales performance telemetry.');
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <LoadingState message="Aggregating regional scorecards..." />;
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Operations</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Performance</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Regional Sales Performance
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              Territory throughput, team win rate benchmarks, and revenue attainment.
            </p>
          </div>
        </div>
      </div>

      {/* Regional Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-space-lg mb-space-xl">
        {regions.map((reg) => (
          <div
            key={reg.regional_office}
            className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between pb-space-xs border-b border-outline-variant/20">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-[20px] text-primary-container">location_city</span>
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">{reg.regional_office} Office</h3>
                </div>
                <span className="font-label-xs-mono text-label-xs-mono font-bold text-tertiary-container bg-tertiary-container/10 px-2 py-0.5 rounded">
                  {reg.win_rate?.toFixed(1)}% Win Rate
                </span>
              </div>

              <div className="space-y-space-sm mt-space-md">
                <div className="flex justify-between items-center text-body-sm">
                  <span className="text-secondary">Won Revenue:</span>
                  <span className="font-bold text-on-surface tnum">
                    ${Math.round(reg.won_revenue || 0).toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between items-center text-body-sm">
                  <span className="text-secondary">Closed Deals:</span>
                  <span className="font-semibold text-on-surface tnum">
                    {reg.won_opportunities} won / {reg.total_opportunities} total
                  </span>
                </div>
                <div className="flex justify-between items-center text-body-sm">
                  <span className="text-secondary">Average Deal:</span>
                  <span className="text-on-surface tnum">
                    ${reg.won_opportunities ? Math.round(reg.won_revenue / reg.won_opportunities).toLocaleString() : '—'}
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-space-lg pt-space-sm border-t border-outline-variant/20">
              <span className="text-xs text-secondary">Operational Territory Lead: Active</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Performance;
