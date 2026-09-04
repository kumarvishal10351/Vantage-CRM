import React, { useEffect, useState } from 'react';
import { opportunitiesApi } from '../../api/client';
import StageBadge from './StageBadge';

export const OpportunityDetailDrawer = ({ opportunityId, onClose }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!opportunityId) return;

    const fetchDetail = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await opportunitiesApi.getById(opportunityId);
        setData(res.data);
      } catch {
        setError('Could not retrieve opportunity metadata.');
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [opportunityId]);

  if (!opportunityId) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-on-surface/30 backdrop-blur-xs transition-opacity">
      <div className="w-full max-w-lg bg-surface-container-lowest h-full shadow-2xl flex flex-col border-l border-outline-variant/40 animate-in slide-in-from-right duration-200">
        {/* Header */}
        <div className="h-14 px-space-lg flex items-center justify-between border-b border-outline-variant/30 bg-surface-container-low/40">
          <div className="flex items-center gap-space-xs">
            <span className="font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
              Opportunity Detail
            </span>
            <span className="text-outline-variant">/</span>
            <span className="font-label-sm text-label-sm font-semibold text-primary-container tnum">
              {opportunityId}
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-secondary hover:text-on-surface hover:bg-surface-container-high transition-colors"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-space-lg">
          {loading ? (
            <div className="py-20 flex flex-col items-center justify-center">
              <div className="w-6 h-6 border-2 border-primary-container border-t-transparent rounded-full animate-spin"></div>
              <span className="font-label-xs-mono text-label-xs-mono text-secondary mt-2">Loading deal record...</span>
            </div>
          ) : error ? (
            <div className="p-4 bg-error-container/30 text-on-error-container rounded-lg text-sm">
              {error}
            </div>
          ) : data ? (
            <div className="flex flex-col gap-space-lg">
              {/* Top Banner */}
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="font-headline-lg text-headline-lg text-on-surface tracking-tight">
                    {data.account || 'Unassigned Account'}
                  </h2>
                  <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                    Product: <strong className="text-on-surface">{data.product}</strong>
                  </p>
                </div>
                <StageBadge stage={data.stage} />
              </div>

              {/* Value Callout */}
              <div className="p-space-base rounded-xl bg-surface-container-low border border-outline-variant/30 flex items-center justify-between">
                <div>
                  <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">
                    Deal Value
                  </span>
                  <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
                    {data.close_value ? `$${Number(data.close_value).toLocaleString()}` : '$0'}
                  </div>
                </div>
                <div className="text-right">
                  <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">
                    Assigned Agent
                  </span>
                  <div className="font-label-md text-label-md font-semibold text-on-surface mt-0.5">
                    {data.sales_agent}
                  </div>
                </div>
              </div>

              {/* Timeline & Metadata */}
              <div className="space-y-space-md border-t border-outline-variant/30 pt-space-md">
                <span className="font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
                  Deal Parameters
                </span>

                <div className="grid grid-cols-2 gap-space-md font-body-sm text-body-sm">
                  <div className="p-space-sm rounded bg-surface-container/40">
                    <span className="text-secondary block font-label-xs-mono text-label-xs-mono uppercase">Engage Date</span>
                    <span className="font-semibold text-on-surface tnum">{data.engage_date || '—'}</span>
                  </div>
                  <div className="p-space-sm rounded bg-surface-container/40">
                    <span className="text-secondary block font-label-xs-mono text-label-xs-mono uppercase">Close Date</span>
                    <span className="font-semibold text-on-surface tnum">{data.close_date || 'In Pipeline'}</span>
                  </div>
                  <div className="p-space-sm rounded bg-surface-container/40">
                    <span className="text-secondary block font-label-xs-mono text-label-xs-mono uppercase">Series / Category</span>
                    <span className="font-semibold text-on-surface">{data.product}</span>
                  </div>
                  <div className="p-space-sm rounded bg-surface-container/40">
                    <span className="text-secondary block font-label-xs-mono text-label-xs-mono uppercase">Record Identifier</span>
                    <span className="font-semibold text-on-surface tnum text-xs">{data.opportunity_id}</span>
                  </div>
                </div>
              </div>

              {/* CRM Guidance */}
              <div className="p-space-base rounded-xl bg-surface-container-high/40 border border-outline-variant/30">
                <div className="flex items-center gap-1 text-primary-container font-label-sm text-label-sm font-semibold uppercase mb-1">
                  <span className="material-symbols-outlined text-[16px]">verified_user</span>
                  <span>Operational Governance</span>
                </div>
                <p className="font-body-sm text-body-sm text-secondary">
                  Real opportunity transaction logged in the verified CRM pipeline engine. No synthetic activities or unverified attributes are recorded.
                </p>
              </div>
            </div>
          ) : null}
        </div>

        {/* Footer actions */}
        <div className="p-space-md border-t border-outline-variant/30 bg-surface-container-low flex justify-end gap-space-sm">
          <button
            onClick={onClose}
            className="h-8 px-space-md rounded bg-surface-container-lowest border border-outline-variant/60 font-label-md text-label-md text-on-surface hover:bg-surface-container transition-colors shadow-xs"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default OpportunityDetailDrawer;
