import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { productsApi } from '../api/client';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

export const Products = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await productsApi.list();
      setProducts(res.data || []);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch product catalog.');
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
          <span className="text-primary-container font-semibold">Products</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Product Portfolio & Price Tiers
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              7 active product offerings across GTX hardware series, MG solutions, and Mobile enterprise lines.
            </p>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      {loading ? (
        <LoadingState message="Loading product catalog..." />
      ) : error ? (
        <ErrorState message={error} onRetry={loadData} />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-space-lg">
          {products.map((p) => (
            <div
              key={p.product}
              onClick={() => navigate(`/products/${encodeURIComponent(p.product)}`)}
              className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs hover:border-primary-container/40 transition-all cursor-pointer flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-space-sm">
                    <div className="w-10 h-10 rounded-xl bg-surface-container text-primary flex items-center justify-center">
                      <span className="material-symbols-outlined text-[22px]">inventory_2</span>
                    </div>
                    <div>
                      <h3 className="font-headline-sm text-headline-sm text-on-surface">{p.product}</h3>
                      <span className="text-xs text-secondary">{p.series || 'Enterprise Series'}</span>
                    </div>
                  </div>
                  <span className="px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold bg-primary-fixed/40 text-primary-container tnum">
                    ${p.sales_price ? Number(p.sales_price).toLocaleString() : '—'}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-space-sm mt-space-lg pt-space-sm border-t border-outline-variant/20">
                  <div>
                    <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">Won Revenue</span>
                    <span className="font-headline-sm text-headline-sm font-bold text-on-surface tnum">
                      ${Math.round(p.won_revenue || 0).toLocaleString()}
                    </span>
                  </div>
                  <div>
                    <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">Win Rate</span>
                    <span className="font-headline-sm text-headline-sm font-bold text-tertiary-container tnum">
                      {p.win_rate !== undefined ? `${p.win_rate.toFixed(1)}%` : '—'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-space-md pt-space-xs border-t border-outline-variant/20 flex items-center justify-between text-xs text-primary-container font-semibold">
                <span>View Product Pipeline</span>
                <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Products;
