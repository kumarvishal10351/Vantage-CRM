import React, { useEffect, useState } from 'react';
import { pipelineApi } from '../api/client';
import StageBadge from '../components/common/StageBadge';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

export const Pipeline = () => {
  const [stages, setStages] = useState([]);
  const [products, setProducts] = useState([]);
  const [sectors, setSectors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [stgRes, prodRes, secRes] = await Promise.all([
        pipelineApi.getStages(),
        pipelineApi.getProducts(),
        pipelineApi.getSectors(),
      ]);
      setStages(stgRes.data || []);
      setProducts(prodRes.data || []);
      setSectors(secRes.data || []);
    } catch (err) {
      console.error(err);
      setError('Failed to load pipeline analysis from backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) return <LoadingState message="Calculating stage progression metrics..." />;
  if (error) return <ErrorState message={error} onRetry={loadData} />;

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Workspace</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Pipeline</span>
          <span className="text-outline-variant">/</span>
          <span className="text-secondary">Stage Architecture</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Pipeline Stage Analysis
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              Direct telemetry across the 4 verified CRM stages: Prospecting, Engaging, Won, and Lost.
            </p>
          </div>
        </div>
      </div>

      {/* Stage Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md mb-space-xl">
        {stages.map((st, idx) => {
          const stageName = st.deal_stage || st.stage || `Stage-${idx}`;
          const isClosed = stageName.toLowerCase() === 'won' || stageName.toLowerCase() === 'lost';
          const count = st.opportunity_count ?? st.count ?? 0;
          const rev = st.total_value ?? st.won_revenue ?? 0;

          return (
            <div
              key={stageName}
              className="bg-surface-container-lowest rounded-xl p-space-base border border-outline-variant/30 shadow-xs flex flex-col justify-between"
            >
              <div className="flex items-center justify-between">
                <StageBadge stage={stageName} />
                <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">
                  {isClosed ? 'Closed' : 'Open'}
                </span>
              </div>
              <div className="mt-space-md">
                <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
                  {count.toLocaleString()}
                </div>
                <div className="font-label-sm text-label-sm text-secondary mt-1">
                  {rev > 0 ? (
                    <span className="text-tertiary-container font-semibold">
                      ${Math.round(rev).toLocaleString()} Realized
                    </span>
                  ) : (
                    <span>Pipeline Volume</span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Sectors & Products Breakdown */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-space-xl">
        {/* Industry Sector Breakdown */}
        <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
          <h2 className="font-headline-sm text-headline-sm text-on-surface mb-space-xs">
            Pipeline by Industry Sector
          </h2>
          <p className="font-body-sm text-body-sm text-secondary mb-space-base">
            Distribution across enterprise verticals
          </p>

          <div className="overflow-x-auto">
            <table className="w-full text-left font-body-sm text-body-sm">
              <thead>
                <tr className="border-b border-outline-variant/30 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider">
                  <th className="py-2 px-3">Industry Sector</th>
                  <th className="py-2 px-3 text-right">Opportunities</th>
                  <th className="py-2 px-3 text-right">Won Deals</th>
                  <th className="py-2 px-3 text-right">Win Rate</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant/20">
                {sectors.map((sec, idx) => {
                  const secName = sec.dimension_value || sec.sector || `Sector-${idx}`;
                  return (
                    <tr key={secName} className="hover:bg-surface-container-low/50">
                      <td className="py-2 px-3 font-medium text-on-surface capitalize">{secName}</td>
                      <td className="py-2 px-3 text-right tnum">{sec.total_opportunities?.toLocaleString()}</td>
                      <td className="py-2 px-3 text-right tnum">{sec.won_opportunities?.toLocaleString()}</td>
                      <td className="py-2 px-3 text-right tnum font-semibold text-tertiary-container">
                        {sec.win_rate?.toFixed(1)}%
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Product Conversion Rates */}
        <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
          <h2 className="font-headline-sm text-headline-sm text-on-surface mb-space-xs">
            Product Line Performance
          </h2>
          <p className="font-body-sm text-body-sm text-secondary mb-space-base">
            Deal volume and win rate across 7 products
          </p>

          <div className="space-y-space-sm">
            {products.map((prod, idx) => {
              const prodName = prod.dimension_value || prod.product || `Product-${idx}`;
              return (
                <div key={prodName} className="p-space-sm rounded-lg bg-surface-container-low/40 flex items-center justify-between">
                  <div>
                    <span className="font-label-md text-label-md font-semibold text-on-surface block">
                      {prodName}
                    </span>
                    <span className="font-label-xs-mono text-label-xs-mono text-secondary">
                      {prod.won_opportunities} won of {prod.total_opportunities} deals
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="font-label-xs-mono text-label-xs-mono font-bold text-tertiary-container tnum block">
                      {prod.win_rate?.toFixed(1)}% Win Rate
                    </span>
                    <span className="font-label-xs-mono text-label-xs-mono text-on-surface tnum">
                      ${Math.round(prod.won_revenue || 0).toLocaleString()}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Pipeline;
