import React, { useEffect, useState } from 'react';
import { prioritiesApi } from '../api/client';
import PriorityBadge from '../components/common/PriorityBadge';
import StageBadge from '../components/common/StageBadge';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import OpportunityDetailDrawer from '../components/common/OpportunityDetailDrawer';

export const Priorities = () => {
  const [priorities, setPriorities] = useState([]);
  const [summary, setSummary] = useState(null);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [page, setPage] = useState(1);
  const limit = 25;

  const [tierFilter, setTierFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedOpportunityId, setSelectedOpportunityId] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumRes, listRes] = await Promise.all([
        prioritiesApi.getSummary(),
        prioritiesApi.list({
          page,
          limit,
          tier: tierFilter || undefined,
        }),
      ]);
      setSummary(sumRes.data);
      const items = listRes.data.items || (Array.isArray(listRes.data) ? listRes.data : []);
      setPriorities(items);
      setTotal(listRes.data.pagination?.total_items ?? listRes.data.total ?? items.length);
      setPages(listRes.data.pagination?.total_pages ?? listRes.data.pages ?? 1);
    } catch (err) {
      console.error(err);
      setError('Unable to load operational prioritization matrix.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [page, tierFilter]);

  return (
    <div className="flex flex-col w-full">
      {/* Breadcrumb & Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Workspace</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Strategic Prioritization</span>
          <span className="text-outline-variant">/</span>
          <span className="text-secondary">Priority Matrix</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Opportunity Prioritization Engine
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              Operational scoring model allocating sales focus across 2,089 active opportunities.
            </p>
          </div>
          <div className="flex items-center gap-space-sm self-start md:self-auto">
            <div className="flex items-center bg-surface-container-lowest border border-outline-variant/30 px-space-sm py-1.5 rounded-lg shadow-xs">
              <span className="material-symbols-outlined text-[16px] text-primary-container mr-1.5">
                verified
              </span>
              <span className="font-label-xs-mono text-label-xs-mono text-secondary">Framework:</span>
              <span className="font-label-xs-mono text-label-xs-mono font-semibold text-on-surface ml-1">
                Deterministic 100-pt Matrix
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Priority Tiers Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-space-md mb-space-xl">
        {/* Tier 1 Card */}
        <div
          onClick={() => {
            setTierFilter(tierFilter === 'Tier 1' ? '' : 'Tier 1');
            setPage(1);
          }}
          className={`p-space-base rounded-xl border cursor-pointer transition-all ${
            tierFilter === 'Tier 1'
              ? 'ring-2 ring-error bg-error-container/10 border-error/40'
              : 'bg-surface-container-lowest border-outline-variant/30 hover:border-error/30'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold bg-error-container text-on-error-container">
              <span className="w-2 h-2 rounded-full bg-error"></span>
              Tier 1 — High Priority
            </span>
            <span className="font-label-xs-mono text-label-xs-mono text-secondary">Score 70–100</span>
          </div>
          <div className="mt-space-sm">
            <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
              {summary?.tier_1_count || 428}
            </div>
            <div className="font-label-sm text-label-sm text-secondary mt-1">
              Immediate executive alignment & active deal intervention
            </div>
          </div>
        </div>

        {/* Tier 2 Card */}
        <div
          onClick={() => {
            setTierFilter(tierFilter === 'Tier 2' ? '' : 'Tier 2');
            setPage(1);
          }}
          className={`p-space-base rounded-xl border cursor-pointer transition-all ${
            tierFilter === 'Tier 2'
              ? 'ring-2 ring-primary-container bg-primary-container/10 border-primary-container/40'
              : 'bg-surface-container-lowest border-outline-variant/30 hover:border-primary-container/30'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold bg-secondary-container text-on-secondary-fixed-variant">
              <span className="w-2 h-2 rounded-full bg-primary-container"></span>
              Tier 2 — Medium Priority
            </span>
            <span className="font-label-xs-mono text-label-xs-mono text-secondary">Score 45–69</span>
          </div>
          <div className="mt-space-sm">
            <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
              {summary?.tier_2_count || 1033}
            </div>
            <div className="font-label-sm text-label-sm text-secondary mt-1">
              Standard sales rep cadence & stage progression
            </div>
          </div>
        </div>

        {/* Tier 3 Card */}
        <div
          onClick={() => {
            setTierFilter(tierFilter === 'Tier 3' ? '' : 'Tier 3');
            setPage(1);
          }}
          className={`p-space-base rounded-xl border cursor-pointer transition-all ${
            tierFilter === 'Tier 3'
              ? 'ring-2 ring-outline bg-surface-container-high border-outline'
              : 'bg-surface-container-lowest border-outline-variant/30 hover:border-outline/40'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold bg-surface-container-high text-secondary">
              <span className="w-2 h-2 rounded-full bg-outline"></span>
              Tier 3 — Lower Priority
            </span>
            <span className="font-label-xs-mono text-label-xs-mono text-secondary">Score 0–44</span>
          </div>
          <div className="mt-space-sm">
            <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
              {summary?.tier_3_count || 628}
            </div>
            <div className="font-label-sm text-label-sm text-secondary mt-1">
              Automated cadence & secondary qualification
            </div>
          </div>
        </div>
      </div>

      {/* Model Definition Callout */}
      <div className="bg-surface-container-lowest rounded-xl p-space-base border border-outline-variant/30 shadow-xs mb-space-xl">
        <div className="flex items-center gap-2 text-primary-container font-headline-sm text-headline-sm mb-space-xs">
          <span className="material-symbols-outlined text-[20px]">architecture</span>
          <span>Deterministic Scoring Architecture (0–100 Points)</span>
        </div>
        <p className="font-body-sm text-body-sm text-secondary leading-relaxed mb-space-md">
          This system evaluates <strong>only open pipeline deals</strong> (2,089 opportunities) using pre-outcome operational variables. It is an operational prioritization score, <strong>not a win probability prediction</strong>.
        </p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-space-sm">
          <div className="p-space-sm rounded-lg bg-surface-container-low border border-outline-variant/20">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">Stage Progress</span>
            <span className="font-headline-sm text-headline-sm font-bold text-on-surface tnum">40 Pts Max</span>
            <span className="text-xs text-secondary block mt-0.5">Engaging (40) vs Prospecting (20)</span>
          </div>
          <div className="p-space-sm rounded-lg bg-surface-container-low border border-outline-variant/20">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">Product Tier</span>
            <span className="font-headline-sm text-headline-sm font-bold text-on-surface tnum">25 Pts Max</span>
            <span className="text-xs text-secondary block mt-0.5">Enterprise (25), Mid (15), Basic (10)</span>
          </div>
          <div className="p-space-sm rounded-lg bg-surface-container-low border border-outline-variant/20">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">Account Scale</span>
            <span className="font-headline-sm text-headline-sm font-bold text-on-surface tnum">20 Pts Max</span>
            <span className="text-xs text-secondary block mt-0.5">Large enterprise accounts & subsidiaries</span>
          </div>
          <div className="p-space-sm rounded-lg bg-surface-container-low border border-outline-variant/20">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">Recency / Velocity</span>
            <span className="font-headline-sm text-headline-sm font-bold text-on-surface tnum">15 Pts Max</span>
            <span className="text-xs text-secondary block mt-0.5">Decaying scale penalizing deal stall</span>
          </div>
        </div>
      </div>

      {/* Filter / Actions */}
      <div className="flex items-center justify-between mb-space-base">
        <div className="flex items-center gap-space-sm">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase tracking-wider">
            Filtered Queue:
          </span>
          <span className="font-semibold text-on-surface">
            {tierFilter ? `${tierFilter} Opportunities` : 'All Open Prioritized Opportunities'}
          </span>
          {tierFilter && (
            <button
              onClick={() => {
                setTierFilter('');
                setPage(1);
              }}
              className="text-xs text-secondary hover:text-on-surface underline ml-2"
            >
              Clear filter
            </button>
          )}
        </div>
        <span className="font-label-xs-mono text-label-xs-mono text-secondary tnum">
          Showing {priorities.length} of {total} records
        </span>
      </div>

      {/* Ranked Table */}
      <div className="bg-surface-container-lowest rounded-xl border border-outline-variant/30 shadow-xs overflow-hidden">
        {loading ? (
          <LoadingState message="Ranking open pipeline by operational score..." />
        ) : error ? (
          <ErrorState message={error} onRetry={loadData} />
        ) : priorities.length === 0 ? (
          <EmptyState
            title="No prioritized opportunities"
            description="No deals found matching the selected priority filter."
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-body-sm text-body-sm border-collapse">
              <thead>
                <tr className="border-b border-outline-variant/30 bg-surface-container-low/40 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider select-none">
                  <th className="py-2.5 px-3">Deal ID</th>
                  <th className="py-2.5 px-3">Account</th>
                  <th className="py-2.5 px-3">Product</th>
                  <th className="py-2.5 px-3">Stage</th>
                  <th className="py-2.5 px-3">Sales Agent</th>
                  <th className="py-2.5 px-3 text-right">Age</th>
                  <th className="py-2.5 px-3 text-center">Score</th>
                  <th className="py-2.5 px-3">Priority Tier</th>
                  <th className="py-2.5 px-3 text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant/20">
                {priorities.map((item) => (
                  <tr
                    key={item.opportunity_id}
                    onClick={() => setSelectedOpportunityId(item.opportunity_id)}
                    className="hover:bg-surface-container-low/60 transition-colors cursor-pointer"
                  >
                    <td className="py-2.5 px-3 font-label-xs-mono text-label-xs-mono font-semibold text-primary-container tnum">
                      {item.opportunity_id}
                    </td>
                    <td className="py-2.5 px-3 font-semibold text-on-surface max-w-xs truncate">
                      {item.account || 'Unassigned Account'}
                    </td>
                    <td className="py-2.5 px-3 text-secondary">{item.product}</td>
                    <td className="py-2.5 px-3">
                      <StageBadge stage={item.deal_stage || item.stage} />
                    </td>
                    <td className="py-2.5 px-3 text-on-surface font-medium">{item.sales_agent}</td>
                    <td className="py-2.5 px-3 text-right text-secondary tnum">
                      {item.engagement_age_days !== undefined ? `${item.engagement_age_days}d` : item.age_days !== undefined ? `${item.age_days}d` : '—'}
                    </td>
                    <td className="py-2.5 px-3 text-center font-metric-mono-md text-metric-mono-md font-bold text-on-surface tnum">
                      {item.crm_priority_score ?? item.priority_score ?? '—'}
                    </td>
                    <td className="py-2.5 px-3">
                      <PriorityBadge tier={item.priority_tier} score={item.crm_priority_score ?? item.priority_score} />
                    </td>
                    <td className="py-2.5 px-3 text-center" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => setSelectedOpportunityId(item.opportunity_id)}
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
            Showing <strong className="text-on-surface tnum">{priorities.length > 0 ? (page - 1) * limit + 1 : 0}</strong> to{' '}
            <strong className="text-on-surface tnum">
              {Math.min(page * limit, total)}
            </strong>{' '}
            of <strong className="text-on-surface tnum">{total.toLocaleString()}</strong> prioritized opportunities
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

export default Priorities;
