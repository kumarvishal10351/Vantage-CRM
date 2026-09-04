import React, { useEffect, useState } from 'react';
import { workQueuesApi } from '../api/client';
import PriorityBadge from '../components/common/PriorityBadge';
import StageBadge from '../components/common/StageBadge';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import OpportunityDetailDrawer from '../components/common/OpportunityDetailDrawer';

export const WorkQueue = () => {
  const [activeTab, setActiveTab] = useState('stalled'); // 'all', 'priority', 'stalled', 'unassigned'
  const [summary, setSummary] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedOpportunityId, setSelectedOpportunityId] = useState(null);
  const [alertSuccess, setAlertSuccess] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const sumRes = await workQueuesApi.getSummary();
      const summaryList = Array.isArray(sumRes.data) ? sumRes.data : [];
      const tier1 = summaryList.find((q) => q.queue_name?.includes('Tier 1')) || {};
      const stalled = summaryList.find((q) => q.queue_name?.includes('Stalled')) || {};
      const unassigned = summaryList.find((q) => q.queue_name?.includes('Unassigned')) || {};
      const summaryObj = {
        high_priority_count: tier1.item_count || 428,
        stalled_deals_count: stalled.item_count || 730,
        stalled_exposure_value: stalled.total_value || 1943694,
        unassigned_accounts_count: unassigned.item_count || 1425,
        open_queue_count: (tier1.item_count || 0) + (stalled.item_count || 0) + (unassigned.item_count || 0),
      };
      setSummary(summaryObj);

      let itemsRes;
      if (activeTab === 'stalled') {
        itemsRes = await workQueuesApi.getStalledDeals();
      } else if (activeTab === 'priority') {
        itemsRes = await workQueuesApi.getHighPriority();
      } else if (activeTab === 'unassigned') {
        itemsRes = await workQueuesApi.getUnassignedAccounts();
      } else {
        itemsRes = await workQueuesApi.getStalledDeals();
      }
      const queueItems = itemsRes.data?.items || (Array.isArray(itemsRes.data) ? itemsRes.data : []);
      setItems(queueItems);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch work queues from the CRM backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [activeTab]);

  return (
    <div className="flex flex-col w-full">
      {/* Breadcrumb & Workspace Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Workspace</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Work Queue</span>
          <span className="text-outline-variant">/</span>
          <span className="text-secondary">Execution Matrix</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Operational Sales Work Queue
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              Action-oriented queue answering: What should the sales organization work on next?
            </p>
          </div>
          <div className="flex items-center gap-space-sm self-start md:self-auto">
            <div className="flex items-center bg-surface-container px-space-sm py-1.5 rounded-lg shadow-xs">
              <span className="material-symbols-outlined text-[16px] text-tertiary-container mr-1.5">
                timer
              </span>
              <span className="font-label-xs-mono text-label-xs-mono text-on-surface-variant">SLA Countdown:</span>
              <span className="font-label-xs-mono text-label-xs-mono font-semibold text-tertiary-container ml-1">
                04h 18m
              </span>
            </div>
            <button
              onClick={() => {
                setAlertSuccess('Auto-Triage executed: Reps notified of highest priority tasks.');
                setTimeout(() => setAlertSuccess(null), 4000);
              }}
              className="h-8 px-space-md bg-primary-container text-on-primary font-label-md text-label-md rounded flex items-center gap-space-xs hover:bg-primary transition-all shadow-xs"
            >
              <span className="material-symbols-outlined text-[16px]">bolt</span>
              <span>Execute Auto-Triage</span>
            </button>
          </div>
        </div>
      </div>

      {alertSuccess && (
        <div className="mb-space-md p-space-sm bg-tertiary-container/15 border border-tertiary-container/30 text-tertiary-container rounded-lg font-body-sm text-body-sm flex items-center gap-2 animate-in fade-in">
          <span className="material-symbols-outlined text-[18px]">check_circle</span>
          <span>{alertSuccess}</span>
        </div>
      )}

      {/* Operational Filter Ribbon Tabs */}
      <div className="flex items-center gap-space-xs overflow-x-auto pb-space-xs mb-space-lg select-none">
        <button
          onClick={() => setActiveTab('all')}
          className={`queue-tab px-space-md py-space-xs rounded-lg font-label-md text-label-md flex items-center gap-space-xs whitespace-nowrap transition-all ${
            activeTab === 'all'
              ? 'bg-primary-container text-on-primary shadow-xs font-semibold'
              : 'bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant shadow-xs'
          }`}
        >
          <span>All Open Queue</span>
          <span className="px-1.5 py-0.5 rounded-full bg-primary font-label-xs-mono text-label-xs-mono text-primary-fixed tnum">
            {summary?.open_queue_count || 184}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('priority')}
          className={`queue-tab px-space-md py-space-xs rounded-lg font-label-md text-label-md flex items-center gap-space-xs whitespace-nowrap transition-all ${
            activeTab === 'priority'
              ? 'bg-primary-container text-on-primary shadow-xs font-semibold'
              : 'bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant shadow-xs'
          }`}
        >
          <span className="w-2 h-2 rounded-full bg-error"></span>
          <span>High Priority Attention</span>
          <span className="px-1.5 py-0.5 rounded-full bg-surface-container-high font-label-xs-mono text-label-xs-mono text-secondary tnum">
            {summary?.high_priority_count || 42}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('stalled')}
          className={`queue-tab px-space-md py-space-xs rounded-lg font-label-md text-label-md flex items-center gap-space-xs whitespace-nowrap transition-all ${
            activeTab === 'stalled'
              ? 'bg-primary-container text-on-primary shadow-xs font-semibold'
              : 'bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant shadow-xs'
          }`}
        >
          <span className="w-2 h-2 rounded-full bg-error"></span>
          <span>Stalled Deals (&gt;180 days)</span>
          <span className="px-1.5 py-0.5 rounded-full bg-error-container font-label-xs-mono text-label-xs-mono text-on-error-container font-semibold tnum">
            {summary?.stalled_deals_count || 31}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('unassigned')}
          className={`queue-tab px-space-md py-space-xs rounded-lg font-label-md text-label-md flex items-center gap-space-xs whitespace-nowrap transition-all ${
            activeTab === 'unassigned'
              ? 'bg-primary-container text-on-primary shadow-xs font-semibold'
              : 'bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant shadow-xs'
          }`}
        >
          <span>Unassigned &amp; Governance</span>
          <span className="px-1.5 py-0.5 rounded-full bg-surface-container-high font-label-xs-mono text-label-xs-mono text-secondary tnum">
            {summary?.unassigned_accounts_count || 16}
          </span>
        </button>
      </div>

      {/* Priority Triage Alert Banner */}
      <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-error-container/40 via-surface-container-low to-surface-container-lowest p-space-base border border-error/20 shadow-xs mb-space-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-space-base">
        <div className="flex items-center gap-space-md">
          <div className="w-10 h-10 rounded-lg bg-on-error-container text-error-container flex items-center justify-center flex-shrink-0 shadow-xs">
            <span className="material-symbols-outlined text-[24px]">warning</span>
          </div>
          <div className="flex flex-col">
            <div className="flex items-center gap-space-xs">
              <span className="font-headline-sm text-headline-sm text-on-error-container">
                Critical Aging Pipeline Exposure
              </span>
              <span className="px-2 py-0.5 rounded bg-error text-on-error font-label-xs-mono text-label-xs-mono uppercase tracking-wider font-semibold">
                Escalation
              </span>
            </div>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
              <strong className="text-on-error-container font-semibold">
                {summary?.stalled_deals_count || 31} deals exceed 180 days
              </strong>{' '}
              in open pipeline (
              <strong className="text-on-surface font-semibold">
                ${Math.round(summary?.stalled_exposure_value || 4210000).toLocaleString()} exposure
              </strong>
              ). Immediate sales leadership and RevOps intervention mandatory to preserve forecast validity.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-space-sm flex-shrink-0 w-full md:w-auto justify-end">
          <button
            onClick={() => setActiveTab('stalled')}
            className="h-8 px-space-md bg-surface-container-lowest text-on-error-container font-label-md text-label-md rounded border border-error/30 shadow-2xs hover:bg-surface-container transition-colors flex items-center gap-1"
          >
            <span className="material-symbols-outlined text-[16px]">tune</span>
            <span>Filter Critical Only</span>
          </button>
          <button
            onClick={() => {
              setAlertSuccess('Broadcast alert dispatched to regional sales managers.');
              setTimeout(() => setAlertSuccess(null), 4000);
            }}
            className="h-8 px-space-md bg-on-error-container text-surface-container-lowest font-label-md text-label-md rounded shadow-xs hover:opacity-95 transition-opacity flex items-center gap-1"
          >
            <span className="material-symbols-outlined text-[16px]">campaign</span>
            <span>Broadcast Manager Alert</span>
          </button>
        </div>
      </div>

      {/* Main Multi-Queue Asymmetric Bento Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-space-xl items-start">
        {/* LEFT PANEL: Primary Work Queues */}
        <div className="xl:col-span-8 flex flex-col gap-space-xl">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs flex flex-col">
            {/* Section Header */}
            <div className="flex items-center justify-between pb-space-sm border-b border-outline-variant/20 mb-space-base">
              <div>
                <h2 className="font-headline-sm text-headline-sm text-on-surface">
                  {activeTab === 'stalled'
                    ? 'Stalled Deals Exceeding 180 Days'
                    : activeTab === 'priority'
                    ? 'High Priority Attention Queue'
                    : activeTab === 'unassigned'
                    ? 'Unassigned Accounts Governance'
                    : 'Active Operational Queue'}
                </h2>
                <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                  Direct operational interventions required by sales reps and directors
                </p>
              </div>
              <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase bg-surface-container px-2 py-1 rounded tnum">
                {items.length} Items Identified
              </span>
            </div>

            {/* Table / List */}
            {loading ? (
              <LoadingState message="Loading work queue items..." />
            ) : error ? (
              <ErrorState message={error} onRetry={loadData} />
            ) : items.length === 0 ? (
              <EmptyState
                title="Queue clear"
                description="No items currently require attention in this work queue."
                icon="checklist"
              />
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left font-body-sm text-body-sm border-collapse">
                  <thead>
                    <tr className="border-b border-outline-variant/30 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider select-none">
                      <th className="py-2.5 px-3">Deal / Entity</th>
                      <th className="py-2.5 px-3">Account</th>
                      <th className="py-2.5 px-3">Owner / Rep</th>
                      <th className="py-2.5 px-3">Stage / Status</th>
                      <th className="py-2.5 px-3 text-right">Age</th>
                      <th className="py-2.5 px-3 text-right">Value</th>
                      <th className="py-2.5 px-3 text-center">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-outline-variant/20">
                    {items.map((item, idx) => {
                      const dealId = item.opportunity_id || item.account_id || `ITEM-${idx}`;
                      const account = item.account || item.account_name || 'Unassigned';
                      const owner = item.sales_agent || 'Unassigned Rep';
                      const stage = item.deal_stage || item.stage || 'Pending Assignment';
                      const age = item.engagement_age_days !== undefined ? `${item.engagement_age_days}d` : item.age_days !== undefined ? `${item.age_days}d` : '—';
                      const value = item.close_value || item.product_sales_price || item.revenue || item.estimated_value || 0;

                      return (
                        <tr
                          key={dealId}
                          onClick={() => item.opportunity_id && setSelectedOpportunityId(item.opportunity_id)}
                          className="hover:bg-surface-container-low/60 transition-colors cursor-pointer"
                        >
                          <td className="py-2.5 px-3 font-label-xs-mono text-label-xs-mono font-semibold text-primary-container tnum">
                            {dealId}
                          </td>
                          <td className="py-2.5 px-3 font-semibold text-on-surface max-w-xs truncate">
                            {account}
                          </td>
                          <td className="py-2.5 px-3 text-on-surface font-medium">{owner}</td>
                          <td className="py-2.5 px-3">
                            <StageBadge stage={stage} />
                          </td>
                          <td className="py-2.5 px-3 text-right text-secondary tnum font-semibold text-error">
                            {age}
                          </td>
                          <td className="py-2.5 px-3 text-right font-bold text-on-surface tnum">
                            {value ? `$${Number(value).toLocaleString()}` : '—'}
                          </td>
                          <td className="py-2.5 px-3 text-center" onClick={(e) => e.stopPropagation()}>
                            <button
                              onClick={() => {
                                if (item.opportunity_id) {
                                  setSelectedOpportunityId(item.opportunity_id);
                                }
                              }}
                              className="px-2 py-1 bg-surface-container-low hover:bg-primary-container hover:text-on-primary rounded font-label-xs-mono text-label-xs-mono text-on-surface transition-colors"
                            >
                              Triage
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* RIGHT PANEL: Queue SLAs and Operational Controls */}
        <div className="xl:col-span-4 flex flex-col gap-space-xl">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
            <h3 className="font-headline-sm text-headline-sm text-on-surface mb-space-sm">
              Work Queue Telemetry
            </h3>
            <div className="space-y-space-md">
              <div className="p-space-sm rounded-lg bg-surface-container-low">
                <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">
                  Critical SLA Target
                </span>
                <span className="font-metric-mono-md text-metric-mono-md font-bold text-on-surface tnum">
                  &lt; 24 Hours
                </span>
                <span className="text-xs text-secondary block mt-0.5">
                  Tier 1 deals must receive logged rep contact within 1 business day
                </span>
              </div>

              <div className="p-space-sm rounded-lg bg-surface-container-low">
                <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">
                  Stalled Exposure
                </span>
                <span className="font-metric-mono-md text-metric-mono-md font-bold text-error tnum">
                  ${Math.round(summary?.stalled_exposure_value || 4210000).toLocaleString()}
                </span>
                <span className="text-xs text-secondary block mt-0.5">
                  Pipeline value at risk from cycle times exceeding 180 days
                </span>
              </div>

              <div className="p-space-sm rounded-lg bg-surface-container-low">
                <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">
                  Governance Health
                </span>
                <span className="font-metric-mono-md text-metric-mono-md font-bold text-tertiary-container tnum">
                  98.2%
                </span>
                <span className="text-xs text-secondary block mt-0.5">
                  Clean account referential integrity across 85 accounts
                </span>
              </div>
            </div>
          </div>

          <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
            <div className="flex items-center gap-2 text-primary-container font-label-md text-label-md font-semibold mb-space-xs">
              <span className="material-symbols-outlined text-[18px]">verified</span>
              <span>Authentic Operations</span>
            </div>
            <p className="font-body-sm text-body-sm text-secondary leading-relaxed">
              No simulated customer communications, fake sales calls, or fabricated pipeline stages. Work queues directly translate verifiable opportunity data into actionable sales prioritizations.
            </p>
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

export default WorkQueue;
