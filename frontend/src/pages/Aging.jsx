import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { agingApi } from '../api/client';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

export const Aging = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await agingApi.getSummary();
      setData(res.data);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch opportunity aging telemetry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) return <LoadingState message="Calculating deal lifecycle velocity..." />;
  if (error) return <ErrorState message={error} onRetry={loadData} />;

  const distribution = data?.aging_distribution || [
    { band: '0–30 Days', count: 820, percentage: 39.2, status: 'Healthy' },
    { band: '31–60 Days', count: 640, percentage: 30.6, status: 'Normal' },
    { band: '61–90 Days', count: 320, percentage: 15.3, status: 'Attention' },
    { band: '91–180 Days', count: 278, percentage: 13.3, status: 'Warning' },
    { band: '180+ Days (Stalled)', count: 31, percentage: 1.5, status: 'Critical' },
  ];

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Operations</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Aging Analysis</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Opportunity Aging & Velocity Analysis
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              Cycle time duration distribution, deal staleness monitoring, and pipeline flow metrics.
            </p>
          </div>
          <button
            onClick={() => navigate('/workqueue')}
            className="h-8 px-space-md bg-primary-container text-on-primary font-label-md text-label-md rounded flex items-center gap-space-xs hover:bg-primary transition-all shadow-xs self-start md:self-auto"
          >
            <span className="material-symbols-outlined text-[16px]">checklist</span>
            <span>View Stalled Queue (31)</span>
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-space-md mb-space-xl">
        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">
            Overall Average Sales Cycle
          </span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum mt-1">
            {data?.overall_average_days?.toFixed(1) || '48.0'} Days
          </div>
          <span className="text-xs text-secondary mt-1 block">From initial engage to resolution</span>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">
            Closed-Won Velocity
          </span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-tertiary-container tnum mt-1">
            42.3 Days
          </div>
          <span className="text-xs text-secondary mt-1 block">Average velocity of converted deals</span>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">
            Critical Stalled Deals
          </span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-error tnum mt-1">
            31 Deals
          </div>
          <span className="text-xs text-error mt-1 block">&gt;180 days in open pipeline</span>
        </div>
      </div>

      {/* Aging Distribution Bands */}
      <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs mb-space-xl">
        <div className="flex items-center justify-between mb-space-base pb-space-sm border-b border-outline-variant/20">
          <div>
            <h2 className="font-headline-sm text-headline-sm text-on-surface">
              Pipeline Aging Distribution Bands
            </h2>
            <p className="font-body-sm text-body-sm text-secondary mt-0.5">
              Open deals categorized by days elapsed since engagement
            </p>
          </div>
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase bg-surface-container px-2 py-1 rounded">
            2,089 Open Pipeline Deals
          </span>
        </div>

        <div className="space-y-space-md">
          {distribution.map((band) => {
            const isCritical = band.status === 'Critical';
            const isWarning = band.status === 'Warning';
            const isAttention = band.status === 'Attention';

            const barColor = isCritical
              ? 'bg-error'
              : isWarning
              ? 'bg-amber-500'
              : isAttention
              ? 'bg-primary-container'
              : 'bg-tertiary-container';

            return (
              <div key={band.band} className="p-space-sm rounded-lg bg-surface-container-low/40">
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <span className="font-label-md text-label-md font-semibold text-on-surface">
                      {band.band}
                    </span>
                    <span
                      className={`px-1.5 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold ${
                        isCritical
                          ? 'bg-error-container text-on-error-container'
                          : isWarning
                          ? 'bg-amber-100 text-amber-800'
                          : 'bg-surface-container text-secondary'
                      }`}
                    >
                      {band.status}
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-metric-mono-md text-metric-mono-md font-bold text-on-surface tnum">
                      {band.count?.toLocaleString()} deals
                    </span>
                    <span className="font-label-xs-mono text-label-xs-mono text-secondary tnum w-12 text-right">
                      {band.percentage}%
                    </span>
                  </div>
                </div>

                <div className="w-full bg-surface-container h-2 rounded-full overflow-hidden">
                  <div
                    className={`${barColor} h-full rounded-full transition-all`}
                    style={{ width: `${band.percentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Aging;
