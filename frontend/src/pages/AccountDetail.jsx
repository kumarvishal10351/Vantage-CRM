import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { accountsApi, opportunitiesApi } from '../api/client';
import StageBadge from '../components/common/StageBadge';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

export const AccountDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [account, setAccount] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [accRes, oppsRes] = await Promise.all([
          accountsApi.getById(id),
          opportunitiesApi.list({ search: id, limit: 50 }),
        ]);
        setAccount(accRes.data);
        // Filter opportunities matching this account exactly
        const matchingOpps = (oppsRes.data.items || []).filter(
          (o) => (o.account || '').toLowerCase() === (accRes.data.account || id).toLowerCase()
        );
        setOpportunities(matchingOpps);
      } catch (err) {
        console.error(err);
        setError('Failed to fetch account profile details.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  if (loading) return <LoadingState message="Loading account hierarchy..." />;
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <button onClick={() => navigate('/accounts')} className="hover:text-on-surface">
            Accounts
          </button>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">{account?.account}</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div className="flex items-center gap-space-md">
            <div className="w-12 h-12 rounded-xl bg-primary-container text-on-primary flex items-center justify-center font-bold text-xl shadow-xs">
              {account?.account?.substring(0, 2).toUpperCase() || 'AC'}
            </div>
            <div>
              <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
                {account?.account}
              </h1>
              <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                {account?.sector || 'Enterprise'} • HQ: {account?.office_location || 'Global'}
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/accounts')}
            className="h-8 px-space-md bg-surface-container-lowest hover:bg-surface-container text-on-surface font-label-md text-label-md rounded border border-outline-variant/60 flex items-center gap-space-xs transition-colors shadow-xs self-start md:self-auto"
          >
            <span className="material-symbols-outlined text-[16px]">arrow_back</span>
            <span>Back to Directory</span>
          </button>
        </div>
      </div>

      {/* Account Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-space-md mb-space-xl">
        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Annual Revenue</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum mt-1">
            {account?.revenue ? `$${Number(account.revenue).toLocaleString()}M` : '—'}
          </div>
          <span className="text-xs text-secondary mt-1 block">Reported corporate revenue</span>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Employees</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum mt-1">
            {account?.employees ? Number(account.employees).toLocaleString() : '—'}
          </div>
          <span className="text-xs text-secondary mt-1 block">Full-time workforce</span>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Year Established</span>
          <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum mt-1">
            {account?.year_established || '—'}
          </div>
          <span className="text-xs text-secondary mt-1 block">Corporate incorporation</span>
        </div>

        <div className="p-space-base rounded-xl bg-surface-container-lowest border border-outline-variant/30 shadow-xs">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Corporate Structure</span>
          <div className="mt-1">
            {account?.subsidiary_of ? (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-medium bg-primary-fixed/40 text-primary-container">
                Subsidiary of {account.subsidiary_of}
              </span>
            ) : (
              <span className="font-label-md text-label-md font-semibold text-on-surface">
                Parent / Independent Corporation
              </span>
            )}
          </div>
          <span className="text-xs text-secondary mt-1 block">Authentic CRM relationship</span>
        </div>
      </div>

      {/* Related Opportunities Table */}
      <div className="bg-surface-container-lowest rounded-xl border border-outline-variant/30 shadow-xs overflow-hidden">
        <div className="h-12 px-space-base border-b border-outline-variant/20 flex items-center justify-between bg-surface-container-low/30">
          <h2 className="font-headline-sm text-headline-sm text-on-surface">
            Account Opportunities ({opportunities.length})
          </h2>
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">
            Logged pipeline activity
          </span>
        </div>

        {opportunities.length === 0 ? (
          <div className="p-space-lg text-center text-secondary text-sm">
            No pipeline deals currently linked to this account.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-body-sm text-body-sm border-collapse">
              <thead>
                <tr className="border-b border-outline-variant/30 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider">
                  <th className="py-2.5 px-3">Deal ID</th>
                  <th className="py-2.5 px-3">Product</th>
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
                    <td className="py-2.5 px-3 text-on-surface font-medium">{opp.product}</td>
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
        )}
      </div>
    </div>
  );
};

export default AccountDetail;
