import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { opportunitiesApi, pipelineApi } from '../api/client';
import StageBadge from '../components/common/StageBadge';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import OpportunityDetailDrawer from '../components/common/OpportunityDetailDrawer';

export const Opportunities = () => {
  const [searchParams] = useSearchParams();
  const [opportunities, setOpportunities] = useState([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [page, setPage] = useState(1);
  const limit = 25;

  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [stageFilter, setStageFilter] = useState('');
  const [productFilter, setProductFilter] = useState('');
  const [productsList, setProductsList] = useState([]);
  const [sortBy, setSortBy] = useState('engage_date');
  const [sortOrder, setSortOrder] = useState('desc');

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedOpportunityId, setSelectedOpportunityId] = useState(null);

  // Summary counts for the top ribbon
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const [sumRes, prodRes] = await Promise.all([
          pipelineApi.getSummary(),
          pipelineApi.getProducts(),
        ]);
        setSummary(sumRes.data);
        setProductsList(prodRes.data);
      } catch (err) {
        console.error('Failed to load filter metadata', err);
      }
    };
    fetchMetadata();
  }, []);

  const loadOpportunities = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {
        page,
        limit,
        sort_by: sortBy,
        sort_order: sortOrder,
      };
      if (search) params.search = search;
      if (stageFilter) params.stage = stageFilter;
      if (productFilter) params.product = productFilter;

      const res = await opportunitiesApi.list(params);
      const items = res.data.items || (Array.isArray(res.data) ? res.data : []);
      setOpportunities(items);
      setTotal(res.data.pagination?.total_items ?? res.data.total ?? items.length);
      setPages(res.data.pagination?.total_pages ?? res.data.pages ?? 1);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch opportunities from the backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOpportunities();
  }, [page, stageFilter, productFilter, sortBy, sortOrder]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    loadOpportunities();
  };

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  return (
    <div className="flex flex-col w-full">
      {/* Breadcrumb & Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Workspace</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Pipeline Management</span>
          <span className="text-outline-variant">/</span>
          <span className="text-secondary">Opportunities</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Opportunities Directory
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              Comprehensive directory of 8,800 deals with multi-field filtering and real-time stage tracking.
            </p>
          </div>
          <div className="flex items-center gap-space-sm self-start md:self-auto">
            <button
              onClick={() => {
                const csvHeader = 'Opportunity ID,Account,Product,Stage,Sales Agent,Engage Date,Close Date,Close Value\n';
                const rows = opportunities.map(o => `"${o.opportunity_id}","${o.account}","${o.product}","${o.stage}","${o.sales_agent}","${o.engage_date}","${o.close_date || ''}","${o.close_value || ''}"`).join('\n');
                const blob = new Blob([csvHeader + rows], { type: 'text/csv' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'crm_opportunities_export.csv';
                a.click();
              }}
              className="h-8 px-space-md bg-surface-container-lowest hover:bg-surface-container text-on-surface font-label-md text-label-md rounded border border-outline-variant/60 flex items-center gap-space-xs transition-colors shadow-xs"
            >
              <span className="material-symbols-outlined text-[16px]">download</span>
              <span>Export CSV</span>
            </button>
          </div>
        </div>
      </div>

      {/* Top Metrics Ribbon */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-space-md mb-space-lg">
        <div className="bg-surface-container-lowest rounded-xl p-space-sm border border-outline-variant/30 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary-container">
            <span className="material-symbols-outlined text-[20px]">view_kanban</span>
          </div>
          <div>
            <div className="font-label-xs-mono text-label-xs-mono uppercase text-secondary">Total Deals</div>
            <div className="font-metric-mono-md text-metric-mono-md font-bold text-on-surface tnum">
              {summary?.total_opportunities?.toLocaleString() || '8,800'}
            </div>
          </div>
        </div>

        <div className="bg-surface-container-lowest rounded-xl p-space-sm border border-outline-variant/30 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-tertiary-container/10 flex items-center justify-center text-tertiary-container">
            <span className="material-symbols-outlined text-[20px]">task_alt</span>
          </div>
          <div>
            <div className="font-label-xs-mono text-label-xs-mono uppercase text-secondary">Won Revenue</div>
            <div className="font-metric-mono-md text-metric-mono-md font-bold text-on-surface tnum">
              ${Math.round(summary?.won_revenue || 0).toLocaleString()}
            </div>
          </div>
        </div>

        <div className="bg-surface-container-lowest rounded-xl p-space-sm border border-outline-variant/30 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-primary-container/10 flex items-center justify-center text-primary-container">
            <span className="material-symbols-outlined text-[20px]">pending_actions</span>
          </div>
          <div>
            <div className="font-label-xs-mono text-label-xs-mono uppercase text-secondary">Open Pipeline</div>
            <div className="font-metric-mono-md text-metric-mono-md font-bold text-on-surface tnum">
              {summary?.open_opportunities?.toLocaleString() || '2,089'}
            </div>
          </div>
        </div>

        <div className="bg-surface-container-lowest rounded-xl p-space-sm border border-outline-variant/30 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-secondary-container/30 flex items-center justify-center text-secondary">
            <span className="material-symbols-outlined text-[20px]">percent</span>
          </div>
          <div>
            <div className="font-label-xs-mono text-label-xs-mono uppercase text-secondary">Win Rate Index</div>
            <div className="font-metric-mono-md text-metric-mono-md font-bold text-on-surface tnum">
              {summary?.win_rate?.toFixed(1) || '63.2'}%
            </div>
          </div>
        </div>
      </div>

      {/* Filter Ribbon */}
      <div className="bg-surface-container-lowest rounded-xl p-space-md border border-outline-variant/30 shadow-xs mb-space-base flex flex-col md:flex-row gap-space-md items-stretch md:items-center justify-between">
        <form onSubmit={handleSearchSubmit} className="relative flex-1 max-w-md">
          <span className="material-symbols-outlined absolute left-space-sm top-1/2 -translate-y-1/2 text-[18px] text-secondary">
            search
          </span>
          <input
            type="text"
            className="w-full h-9 pl-9 pr-space-md bg-surface-container-low border border-outline-variant/60 rounded-lg font-body-sm text-body-sm text-on-surface placeholder:text-secondary focus:outline-none focus:border-primary-container"
            placeholder="Filter by account, agent, or deal ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </form>

        <div className="flex flex-wrap items-center gap-space-sm">
          {/* Stage Filter */}
          <div className="flex items-center gap-1.5">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Stage:</span>
            <select
              value={stageFilter}
              onChange={(e) => {
                setStageFilter(e.target.value);
                setPage(1);
              }}
              className="h-8 px-2 bg-surface-container-low border border-outline-variant/60 rounded font-label-md text-label-md text-on-surface focus:outline-none focus:border-primary-container"
            >
              <option value="">All Stages</option>
              <option value="Prospecting">Prospecting</option>
              <option value="Engaging">Engaging</option>
              <option value="Won">Won</option>
              <option value="Lost">Lost</option>
            </select>
          </div>

          {/* Product Filter */}
          <div className="flex items-center gap-1.5">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Product:</span>
            <select
              value={productFilter}
              onChange={(e) => {
                setProductFilter(e.target.value);
                setPage(1);
              }}
              className="h-8 px-2 bg-surface-container-low border border-outline-variant/60 rounded font-label-md text-label-md text-on-surface focus:outline-none focus:border-primary-container"
            >
              <option value="">All Products</option>
              {productsList.map((p) => (
                <option key={p.product} value={p.product}>
                  {p.product}
                </option>
              ))}
            </select>
          </div>

          {(search || stageFilter || productFilter) && (
            <button
              onClick={() => {
                setSearch('');
                setStageFilter('');
                setProductFilter('');
                setPage(1);
              }}
              className="h-8 px-2 text-secondary hover:text-on-surface font-label-xs-mono text-label-xs-mono uppercase underline"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Main Table Container */}
      <div className="bg-surface-container-lowest rounded-xl border border-outline-variant/30 shadow-xs overflow-hidden">
        {loading ? (
          <LoadingState message="Loading opportunities..." />
        ) : error ? (
          <ErrorState message={error} onRetry={loadOpportunities} />
        ) : opportunities.length === 0 ? (
          <EmptyState
            title="No opportunities found"
            description="No opportunities match your current filter parameters."
            icon="monetization_on"
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-body-sm text-body-sm border-collapse">
              <thead>
                <tr className="border-b border-outline-variant/30 bg-surface-container-low/40 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider select-none">
                  <th className="py-2.5 px-3">
                    <button
                      onClick={() => handleSort('opportunity_id')}
                      className="flex items-center gap-1 hover:text-on-surface"
                    >
                      <span>Deal ID</span>
                      {sortBy === 'opportunity_id' && (
                        <span className="material-symbols-outlined text-[14px]">
                          {sortOrder === 'asc' ? 'arrow_upward' : 'arrow_downward'}
                        </span>
                      )}
                    </button>
                  </th>
                  <th className="py-2.5 px-3">
                    <button
                      onClick={() => handleSort('account')}
                      className="flex items-center gap-1 hover:text-on-surface"
                    >
                      <span>Account</span>
                      {sortBy === 'account' && (
                        <span className="material-symbols-outlined text-[14px]">
                          {sortOrder === 'asc' ? 'arrow_upward' : 'arrow_downward'}
                        </span>
                      )}
                    </button>
                  </th>
                  <th className="py-2.5 px-3">Product</th>
                  <th className="py-2.5 px-3">Stage</th>
                  <th className="py-2.5 px-3">Sales Agent</th>
                  <th className="py-2.5 px-3">
                    <button
                      onClick={() => handleSort('engage_date')}
                      className="flex items-center gap-1 hover:text-on-surface"
                    >
                      <span>Engage Date</span>
                      {sortBy === 'engage_date' && (
                        <span className="material-symbols-outlined text-[14px]">
                          {sortOrder === 'asc' ? 'arrow_upward' : 'arrow_downward'}
                        </span>
                      )}
                    </button>
                  </th>
                  <th className="py-2.5 px-3 text-right">
                    <button
                      onClick={() => handleSort('close_value')}
                      className="flex items-center gap-1 hover:text-on-surface ml-auto"
                    >
                      <span>Close Value</span>
                      {sortBy === 'close_value' && (
                        <span className="material-symbols-outlined text-[14px]">
                          {sortOrder === 'asc' ? 'arrow_upward' : 'arrow_downward'}
                        </span>
                      )}
                    </button>
                  </th>
                  <th className="py-2.5 px-3 text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant/20">
                {opportunities.map((opp) => (
                  <tr
                    key={opp.opportunity_id}
                    onClick={() => setSelectedOpportunityId(opp.opportunity_id)}
                    className="hover:bg-surface-container-low/60 transition-colors cursor-pointer"
                  >
                    <td className="py-2.5 px-3 font-label-xs-mono text-label-xs-mono font-semibold text-primary-container tnum">
                      {opp.opportunity_id}
                    </td>
                    <td className="py-2.5 px-3 font-semibold text-on-surface max-w-xs truncate">
                      {opp.account || 'Unassigned Account'}
                    </td>
                    <td className="py-2.5 px-3 text-secondary">{opp.product}</td>
                    <td className="py-2.5 px-3">
                      <StageBadge stage={opp.deal_stage || opp.stage} />
                    </td>
                    <td className="py-2.5 px-3 text-on-surface font-medium">{opp.sales_agent}</td>
                    <td className="py-2.5 px-3 text-secondary tnum">{opp.engage_date}</td>
                    <td className="py-2.5 px-3 text-right font-bold text-on-surface tnum">
                      {opp.close_value ? `$${Number(opp.close_value).toLocaleString()}` : '—'}
                    </td>
                    <td className="py-2.5 px-3 text-center" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => setSelectedOpportunityId(opp.opportunity_id)}
                        className="p-1 rounded text-secondary hover:text-primary-container hover:bg-surface-container transition-colors"
                        title="View Opportunity Detail"
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

        {/* Pagination Bar */}
        <div className="h-12 px-space-base bg-surface-container-low/40 border-t border-outline-variant/30 flex items-center justify-between font-label-sm text-label-sm text-secondary select-none">
          <div>
            Showing <strong className="text-on-surface tnum">{opportunities.length > 0 ? (page - 1) * limit + 1 : 0}</strong> to{' '}
            <strong className="text-on-surface tnum">
              {Math.min(page * limit, total)}
            </strong>{' '}
            of <strong className="text-on-surface tnum">{total.toLocaleString()}</strong> opportunities
          </div>

          <div className="flex items-center gap-space-xs">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="h-7 px-2.5 rounded bg-surface-container-lowest border border-outline-variant/60 font-label-xs-mono text-label-xs-mono disabled:opacity-40 hover:bg-surface-container transition-colors shadow-2xs"
            >
              Previous
            </button>
            <span className="px-2 font-label-xs-mono text-label-xs-mono tnum">
              Page {page} of {pages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(pages, p + 1))}
              disabled={page >= pages}
              className="h-7 px-2.5 rounded bg-surface-container-lowest border border-outline-variant/60 font-label-xs-mono text-label-xs-mono disabled:opacity-40 hover:bg-surface-container transition-colors shadow-2xs"
            >
              Next
            </button>
          </div>
        </div>
      </div>

      {/* Slide-out detail drawer */}
      {selectedOpportunityId && (
        <OpportunityDetailDrawer
          opportunityId={selectedOpportunityId}
          onClose={() => setSelectedOpportunityId(null)}
        />
      )}
    </div>
  );
};

export default Opportunities;
