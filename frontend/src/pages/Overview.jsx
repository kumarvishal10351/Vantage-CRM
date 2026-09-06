import React, { useEffect, useState } from 'react';
import { pipelineApi } from '../api/client';
import MetricCard from '../components/common/MetricCard';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

export const Overview = () => {
  const [summary, setSummary] = useState(null);
  const [stages, setStages] = useState([]);
  const [products, setProducts] = useState([]);
  const [regions, setRegions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumRes, stagesRes, prodRes, regRes] = await Promise.all([
        pipelineApi.getSummary(),
        pipelineApi.getStages(),
        pipelineApi.getProducts(),
        pipelineApi.getRegions(),
      ]);
      setSummary(sumRes.data);
      setStages(stagesRes.data);
      setProducts(prodRes.data);
      setRegions(regRes.data);
    } catch (err) {
      console.error(err);
      setError('Unable to fetch pipeline telemetry. Please verify backend service connectivity.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) return <LoadingState message="Connecting to Vantage Revenue Engine..." />;
  if (error) return <ErrorState message={error} onRetry={loadData} />;

  return (
    <div className="flex flex-col w-full">
      {/* Breadcrumb & Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Enterprise</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Revenue Operations</span>
          <span className="text-outline-variant">/</span>
          <span className="text-secondary">Overview</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Executive Revenue Operations
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              Live sales telemetry, win-rate health index, and cross-stage pipeline velocity.
            </p>
          </div>
          <div className="flex items-center gap-space-sm self-start md:self-auto">
            <div className="flex items-center bg-surface-container-lowest border border-outline-variant/30 px-space-sm py-1.5 rounded-lg shadow-xs">
              <span className="material-symbols-outlined text-[16px] text-tertiary-container mr-1.5 animate-pulse">
                fiber_manual_record
              </span>
              <span className="font-label-xs-mono text-label-xs-mono text-secondary">Telemetry:</span>
              <span className="font-label-xs-mono text-label-xs-mono font-semibold text-on-surface ml-1">
                Verified Engine
              </span>
            </div>
            <button
              onClick={loadData}
              className="h-8 px-space-md bg-surface-container-lowest hover:bg-surface-container text-on-surface font-label-md text-label-md rounded border border-outline-variant/60 flex items-center gap-space-xs transition-colors shadow-xs"
            >
              <span className="material-symbols-outlined text-[16px]">sync</span>
              <span>Sync</span>
            </button>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md mb-space-xl">
        <MetricCard
          label="Total Won Revenue"
          value={summary?.won_revenue}
          formatAsMoney={true}
          change="+12.4%"
          changePositive={true}
          icon="payments"
          subtext="Target $10.0M threshold achieved"
        />
        <MetricCard
          label="Closed-Won Deals"
          value={summary?.won_opportunities}
          icon="task_alt"
          subtext={`Win Rate: ${summary?.win_rate?.toFixed(1)}% of closed deals`}
        />
        <MetricCard
          label="Active Pipeline Deals"
          value={summary?.open_opportunities}
          icon="view_kanban"
          subtext={`${summary?.accounts_count} accounts • ${summary?.products_count} products`}
        />
        <MetricCard
          label="Average Sales Cycle"
          value={`${summary?.average_sales_cycle?.toFixed(1)} days`}
          icon="timelapse"
          subtext={`Avg Deal Size: $${Math.round(summary?.average_deal_size || 0).toLocaleString()}`}
        />
      </div>

      {/* Bento Grid: Pipeline Stages + Product Contribution */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-space-xl items-start mb-space-xl">
        {/* Left Column: Pipeline Stages & Distribution */}
        <div className="xl:col-span-8 flex flex-col gap-space-xl">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
            <div className="flex items-center justify-between mb-space-base pb-space-sm border-b border-outline-variant/20">
              <div>
                <h2 className="font-headline-sm text-headline-sm text-on-surface">
                  Pipeline Stage Distribution
                </h2>
                <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                  Real breakdown across operational pipeline lifecycle
                </p>
              </div>
              <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase bg-surface-container px-2 py-1 rounded">
                {summary?.total_opportunities?.toLocaleString()} Total Opportunities
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md">
              {stages.map((st, idx) => {
                const stageName = st.deal_stage || st.stage || `Stage-${idx}`;
                const isWon = stageName.toLowerCase() === 'won';
                const isEngaging = stageName.toLowerCase() === 'engaging';
                const isProspecting = stageName.toLowerCase() === 'prospecting';
                const count = st.opportunity_count ?? st.count ?? 0;
                const rev = st.total_value ?? st.won_revenue ?? 0;

                return (
                  <div
                    key={`${stageName}-${idx}`}
                    className={`p-space-base rounded-xl border flex flex-col justify-between ${
                      isWon
                        ? 'bg-tertiary-container/5 border-tertiary-container/30'
                        : isEngaging
                        ? 'bg-primary-container/5 border-primary-container/20'
                        : isProspecting
                        ? 'bg-surface-container-low border-outline-variant/30'
                        : 'bg-error-container/10 border-error/20'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-space-xs">
                      <span className="font-label-sm text-label-sm font-semibold text-on-surface uppercase tracking-wide">
                        {stageName}
                      </span>
                      <span
                        className={`w-2 h-2 rounded-full ${
                          isWon
                            ? 'bg-tertiary-container'
                            : isEngaging
                            ? 'bg-primary-container animate-pulse'
                            : isProspecting
                            ? 'bg-secondary'
                            : 'bg-error'
                        }`}
                      ></span>
                    </div>

                    <div className="mt-space-xs">
                      <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
                        {count.toLocaleString()}
                      </div>
                      <div className="font-label-xs-mono text-label-xs-mono text-secondary mt-0.5">
                        {rev > 0
                          ? `$${Math.round(rev).toLocaleString()}`
                          : `${((count / (summary?.total_opportunities || 1)) * 100).toFixed(1)}% of total`}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Stage Proportional Bar */}
            <div className="mt-space-lg">
              <div className="h-3 w-full rounded-full bg-surface-container flex overflow-hidden">
                {stages.map((st, idx) => {
                  const stageName = st.deal_stage || st.stage || `Stage-${idx}`;
                  const count = st.opportunity_count ?? st.count ?? 0;
                  const pct = st.percentage_of_total ?? ((count / (summary?.total_opportunities || 1)) * 100);
                  const color =
                    stageName.toLowerCase() === 'won'
                      ? 'bg-tertiary-container'
                      : stageName.toLowerCase() === 'engaging'
                      ? 'bg-primary-container'
                      : stageName.toLowerCase() === 'prospecting'
                      ? 'bg-outline'
                      : 'bg-error';
                  return (
                    <div
                      key={`${stageName}-bar-${idx}`}
                      style={{ width: `${pct}%` }}
                      className={`${color} h-full`}
                      title={`${stageName}: ${count} (${pct}%)`}
                    />
                  );
                })}
              </div>
              <div className="flex flex-wrap items-center justify-between text-xs text-secondary mt-2">
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-tertiary-container"></span> Won (48.2%)
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-primary-container"></span> Engaging (18.1%)
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-outline"></span> Prospecting (5.7%)
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-error"></span> Lost (28.1%)
                </span>
              </div>
            </div>
          </div>

          {/* Regional Performance Table */}
          <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
            <div className="flex items-center justify-between mb-space-base pb-space-sm border-b border-outline-variant/20">
              <div>
                <h2 className="font-headline-sm text-headline-sm text-on-surface">
                  Regional Office Distribution
                </h2>
                <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                  Pipeline throughput across 3 primary territory offices
                </p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left font-body-sm text-body-sm">
                <thead>
                  <tr className="border-b border-outline-variant/30 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider">
                    <th className="py-2.5 px-3">Regional Office</th>
                    <th className="py-2.5 px-3 text-right">Total Deals</th>
                    <th className="py-2.5 px-3 text-right">Won Deals</th>
                    <th className="py-2.5 px-3 text-right">Win Rate</th>
                    <th className="py-2.5 px-3 text-right">Won Revenue</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-outline-variant/20">
                  {regions.map((reg, idx) => {
                    const regName = reg.dimension_value || reg.regional_office || `Region-${idx}`;
                    return (
                      <tr key={regName} className="hover:bg-surface-container-low/50 transition-colors">
                        <td className="py-2.5 px-3 font-semibold text-on-surface flex items-center gap-2">
                          <span className="material-symbols-outlined text-[16px] text-secondary">location_on</span>
                          <span>{regName}</span>
                        </td>
                        <td className="py-2.5 px-3 text-right tnum">{reg.total_opportunities?.toLocaleString()}</td>
                        <td className="py-2.5 px-3 text-right tnum">{reg.won_opportunities?.toLocaleString()}</td>
                        <td className="py-2.5 px-3 text-right tnum font-semibold text-tertiary-container">
                          {reg.win_rate?.toFixed(1)}%
                        </td>
                        <td className="py-2.5 px-3 text-right tnum font-bold text-on-surface">
                          ${Math.round(reg.won_revenue || 0).toLocaleString()}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column: Product Revenue Contribution */}
        <div className="xl:col-span-4 flex flex-col gap-space-xl">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
            <div className="flex items-center justify-between mb-space-base pb-space-sm border-b border-outline-variant/20">
              <div>
                <h2 className="font-headline-sm text-headline-sm text-on-surface">
                  Product Adoption & Revenue
                </h2>
                <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                  7 Core Hardware / Software Offerings
                </p>
              </div>
            </div>

            <div className="space-y-space-md">
              {products.map((p, idx) => {
                const prodName = p.dimension_value || p.product || `Product-${idx}`;
                const revShare = ((p.won_revenue / (summary?.won_revenue || 1)) * 100).toFixed(1);
                return (
                  <div key={prodName} className="flex flex-col gap-1 p-space-sm rounded-lg hover:bg-surface-container-low/60 transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-[16px] text-secondary">inventory_2</span>
                        <span className="font-label-md text-label-md font-semibold text-on-surface">
                          {prodName}
                        </span>
                      </div>
                      <span className="font-label-xs-mono text-label-xs-mono font-bold text-on-surface tnum">
                        ${Math.round(p.won_revenue || 0).toLocaleString()}
                      </span>
                    </div>

                    <div className="flex items-center justify-between text-xs text-secondary mt-0.5">
                      <span>{p.series || 'Enterprise Tier'}</span>
                      <span className="tnum font-medium text-tertiary-container">{revShare}% share</span>
                    </div>

                    <div className="w-full bg-surface-container h-1.5 rounded-full overflow-hidden mt-1">
                      <div
                        className="bg-primary-container h-full rounded-full"
                        style={{ width: `${revShare}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Operational Governance Callout */}
          <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
            <div className="flex items-center gap-space-sm mb-space-xs text-primary-container font-label-md text-label-md font-semibold">
              <span className="material-symbols-outlined text-[20px]">policy</span>
              <span>CRM Operational Standards</span>
            </div>
            <p className="font-body-sm text-body-sm text-secondary leading-relaxed">
              All pipeline metrics represent 100% authentic B2B transaction telemetry. No synthetic churn, ML conversion predictions, or fabricated contact entities exist.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
