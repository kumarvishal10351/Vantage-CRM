import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { productsApi, opportunitiesApi } from '../api/client';
import StageBadge from '../components/common/StageBadge';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

export const ProductDetail = () => {
  const { name } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [prodRes, oppsRes] = await Promise.all([
          productsApi.getByName(name),
          opportunitiesApi.list({ product: name, limit: 50, sort_by: 'engage_date', sort_order: 'desc' }),
        ]);
        setProduct(prodRes.data);
        setOpportunities(oppsRes.data.items || []);
      } catch (err) {
        console.error(err);
        setError('Failed to fetch product profile details.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [name]);

  if (loading) return <LoadingState message="Loading product data..." />;
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <button onClick={() => navigate('/products')} className="hover:text-on-surface">
            Products
          </button>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">{product?.product}</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div className="flex items-center gap-space-md">
            <div className="w-12 h-12 rounded-xl bg-primary-container text-on-primary flex items-center justify-center font-bold text-xl shadow-xs">
              <span className="material-symbols-outlined text-[24px]">inventory_2</span>
            </div>
            <div>
              <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
                {product?.product}
              </h1>
              <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                Series: <strong className="text-on-surface">{product?.series || 'Standard'}</strong> • Base Price:{' '}
                <strong className="text-on-surface">${product?.sales_price?.toLocaleString()}</strong>
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/products')}
            className="h-8 px-space-md bg-surface-container-lowest hover:bg-surface-container text-on-surface font-label-md text-label-md rounded border border-outline-variant/60 flex items-center gap-space-xs transition-colors shadow-xs self-start md:self-auto"
          >
            <span className="material-symbols-outlined text-[16px]">arrow_back</span>
            <span>Back to Products</span>
          </button>
        </div>
      </div>

      {/* Product Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-space-md mb-space-xl">
        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Won Revenue</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum mt-1">
            ${Math.round(product?.won_revenue || 0).toLocaleString()}
          </div>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Win Rate</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-tertiary-container tnum mt-1">
            {product?.win_rate !== undefined ? `${product.win_rate.toFixed(1)}%` : '—'}
          </div>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Total Opportunities</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum mt-1">
            {product?.total_opportunities?.toLocaleString()}
          </div>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Closed Won Deals</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-primary-container tnum mt-1">
            {product?.won_opportunities?.toLocaleString()}
          </div>
        </div>
      </div>

      {/* Opportunities Table */}
      <div className="bg-surface-container-lowest rounded-xl border border-outline-variant/30 shadow-xs overflow-hidden">
        <div className="h-12 px-space-base border-b border-outline-variant/20 flex items-center justify-between bg-surface-container-low/30">
          <h2 className="font-headline-sm text-headline-sm text-on-surface">
            Product Deals ({opportunities.length})
          </h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left font-body-sm text-body-sm border-collapse">
            <thead>
              <tr className="border-b border-outline-variant/30 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider">
                <th className="py-2.5 px-3">Deal ID</th>
                <th className="py-2.5 px-3">Account</th>
                <th className="py-2.5 px-3">Stage</th>
                <th className="py-2.5 px-3">Sales Agent</th>
                <th className="py-2.5 px-3">Engage Date</th>
                <th className="py-2.5 px-3 text-right">Close Value</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/20">
              {opportunities.map((opp) => (
                <tr key={opp.opportunity_id} className="hover:bg-surface-container-low/60 transition-colors">
                  <td className="py-2.5 px-3 font-label-xs-mono text-label-xs-mono font-semibold text-primary-container tnum">
                    {opp.opportunity_id}
                  </td>
                  <td className="py-2.5 px-3 font-medium text-on-surface">{opp.account}</td>
                  <td className="py-2.5 px-3">
                    <StageBadge stage={opp.stage} />
                  </td>
                  <td className="py-2.5 px-3 text-secondary">{opp.sales_agent}</td>
                  <td className="py-2.5 px-3 text-secondary tnum">{opp.engage_date}</td>
                  <td className="py-2.5 px-3 text-right font-bold text-on-surface tnum">
                    {opp.close_value ? `$${Number(opp.close_value).toLocaleString()}` : '—'}
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

export default ProductDetail;
