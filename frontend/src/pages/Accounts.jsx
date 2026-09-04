import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { accountsApi } from '../api/client';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';

export const Accounts = () => {
  const navigate = useNavigate();
  const [accounts, setAccounts] = useState([]);
  const [summary, setSummary] = useState(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const limit = 25;

  const [search, setSearch] = useState('');
  const [sectorFilter, setSectorFilter] = useState('');
  const [parentOnly, setParentOnly] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumRes, accRes] = await Promise.all([
        accountsApi.getSummary(),
        accountsApi.list({
          page,
          limit,
          search: search || undefined,
          sector: sectorFilter || undefined,
          parent_only: parentOnly ? true : undefined,
        }),
      ]);
      setSummary(sumRes.data);
      setAccounts(accRes.data.items || []);
      setTotal(accRes.data.total || 0);
      setPages(accRes.data.pages || 1);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch accounts from CRM engine.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [page, sectorFilter, parentOnly]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    loadData();
  };

  return (
    <div className="flex flex-col w-full">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Workspace</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Accounts</span>
          <span className="text-outline-variant">/</span>
          <span className="text-secondary">Directory</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
          <div>
            <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
              Enterprise Accounts
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
              85 verified corporate client accounts, subsidiary hierarchies, and corporate revenue data.
            </p>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-space-md mb-space-lg">
        <div className="bg-surface-container-lowest rounded-xl p-space-base border border-outline-variant/30 shadow-xs flex items-center justify-between">
          <div>
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Total Accounts</span>
            <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
              {summary?.total_accounts || 85}
            </div>
            <span className="text-xs text-secondary mt-1 block">Full enterprise directory</span>
          </div>
          <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary-container">
            <span className="material-symbols-outlined text-[22px]">corporate_fare</span>
          </div>
        </div>

        <div className="bg-surface-container-lowest rounded-xl p-space-base border border-outline-variant/30 shadow-xs flex items-center justify-between">
          <div>
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Parent Corporations</span>
            <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
              {summary?.parent_companies_count || 7}
            </div>
            <span className="text-xs text-secondary mt-1 block">Holding 15 active subsidiaries</span>
          </div>
          <div className="w-10 h-10 rounded-lg bg-tertiary-container/10 flex items-center justify-center text-tertiary-container">
            <span className="material-symbols-outlined text-[22px]">account_tree</span>
          </div>
        </div>

        <div className="bg-surface-container-lowest rounded-xl p-space-base border border-outline-variant/30 shadow-xs flex items-center justify-between">
          <div>
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Average Revenue</span>
            <div className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum">
              ${Math.round(summary?.average_revenue || 1280).toLocaleString()}M
            </div>
            <span className="text-xs text-secondary mt-1 block">Enterprise client valuation</span>
          </div>
          <div className="w-10 h-10 rounded-lg bg-primary-container/10 flex items-center justify-center text-primary-container">
            <span className="material-symbols-outlined text-[22px]">trending_up</span>
          </div>
        </div>
      </div>

      {/* Filter Ribbon */}
      <div className="bg-surface-container-lowest rounded-xl p-space-md border border-outline-variant/30 shadow-xs mb-space-base flex flex-col md:flex-row gap-space-md items-stretch md:items-center justify-between">
        <form onSubmit={handleSearch} className="relative flex-1 max-w-md">
          <span className="material-symbols-outlined absolute left-space-sm top-1/2 -translate-y-1/2 text-[18px] text-secondary">
            search
          </span>
          <input
            type="text"
            className="w-full h-9 pl-9 pr-space-md bg-surface-container-low border border-outline-variant/60 rounded-lg font-body-sm text-body-sm text-on-surface placeholder:text-secondary focus:outline-none focus:border-primary-container"
            placeholder="Search accounts or location..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </form>

        <div className="flex items-center gap-space-sm">
          <div className="flex items-center gap-1.5">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase">Sector:</span>
            <select
              value={sectorFilter}
              onChange={(e) => {
                setSectorFilter(e.target.value);
                setPage(1);
              }}
              className="h-8 px-2 bg-surface-container-low border border-outline-variant/60 rounded font-label-md text-label-md text-on-surface focus:outline-none focus:border-primary-container"
            >
              <option value="">All Sectors</option>
              <option value="retail">Retail</option>
              <option value="technology">Technology</option>
              <option value="medical">Medical</option>
              <option value="finance">Finance</option>
              <option value="telecommunications">Telecommunications</option>
              <option value="services">Services</option>
            </select>
          </div>

          <button
            onClick={() => {
              setParentOnly(!parentOnly);
              setPage(1);
            }}
            className={`h-8 px-3 rounded font-label-md text-label-md transition-colors ${
              parentOnly
                ? 'bg-primary-container text-on-primary font-semibold'
                : 'bg-surface-container-low border border-outline-variant/60 text-on-surface hover:bg-surface-container'
            }`}
          >
            Parents Only (7)
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-surface-container-lowest rounded-xl border border-outline-variant/30 shadow-xs overflow-hidden">
        {loading ? (
          <LoadingState message="Loading accounts directory..." />
        ) : error ? (
          <ErrorState message={error} onRetry={loadData} />
        ) : accounts.length === 0 ? (
          <EmptyState title="No accounts found" description="Try clearing your search query." icon="corporate_fare" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-body-sm text-body-sm border-collapse">
              <thead>
                <tr className="border-b border-outline-variant/30 bg-surface-container-low/40 text-secondary font-label-xs-mono text-label-xs-mono uppercase tracking-wider select-none">
                  <th className="py-2.5 px-3">Account Name</th>
                  <th className="py-2.5 px-3">Industry Sector</th>
                  <th className="py-2.5 px-3">Headquarters</th>
                  <th className="py-2.5 px-3 text-right">Revenue ($M)</th>
                  <th className="py-2.5 px-3 text-right">Employees</th>
                  <th className="py-2.5 px-3">Parent Company</th>
                  <th className="py-2.5 px-3 text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant/20">
                {accounts.map((acc) => (
                  <tr
                    key={acc.account_id || acc.account}
                    onClick={() => navigate(`/accounts/${encodeURIComponent(acc.account)}`)}
                    className="hover:bg-surface-container-low/60 transition-colors cursor-pointer"
                  >
                    <td className="py-2.5 px-3 font-semibold text-on-surface flex items-center gap-2">
                      <span className="material-symbols-outlined text-[18px] text-secondary">domain</span>
                      <span>{acc.account}</span>
                    </td>
                    <td className="py-2.5 px-3 text-secondary">{acc.sector || 'General'}</td>
                    <td className="py-2.5 px-3 text-secondary">{acc.office_location || '—'}</td>
                    <td className="py-2.5 px-3 text-right font-bold text-on-surface tnum">
                      {acc.revenue ? `$${Number(acc.revenue).toLocaleString()}` : '—'}
                    </td>
                    <td className="py-2.5 px-3 text-right text-secondary tnum">
                      {acc.employees ? Number(acc.employees).toLocaleString() : '—'}
                    </td>
                    <td className="py-2.5 px-3">
                      {acc.subsidiary_of ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-medium bg-primary-fixed/40 text-primary-container">
                          <span className="material-symbols-outlined text-[12px]">subdirectory_arrow_right</span>
                          <span>{acc.subsidiary_of}</span>
                        </span>
                      ) : (
                        <span className="text-secondary text-xs">—</span>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-center" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => navigate(`/accounts/${encodeURIComponent(acc.account)}`)}
                        className="p-1 rounded text-secondary hover:text-primary-container transition-colors"
                        title="View Account Details"
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

        {/* Pagination */}
        <div className="h-12 px-space-base bg-surface-container-low/40 border-t border-outline-variant/30 flex items-center justify-between font-label-sm text-label-sm text-secondary select-none">
          <div>
            Showing <strong className="text-on-surface tnum">{accounts.length > 0 ? (page - 1) * limit + 1 : 0}</strong> to{' '}
            <strong className="text-on-surface tnum">{Math.min(page * limit, total)}</strong> of{' '}
            <strong className="text-on-surface tnum">{total.toLocaleString()}</strong> accounts
          </div>

          <div className="flex items-center gap-space-xs">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="h-7 px-2.5 rounded bg-surface-container-lowest border border-outline-variant/60 font-label-xs-mono text-label-xs-mono disabled:opacity-40 hover:bg-surface-container transition-colors"
            >
              Previous
            </button>
            <span className="px-2 font-label-xs-mono text-label-xs-mono tnum">
              Page {page} of {pages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(pages, p + 1))}
              disabled={page >= pages}
              className="h-7 px-2.5 rounded bg-surface-container-lowest border border-outline-variant/60 font-label-xs-mono text-label-xs-mono disabled:opacity-40 hover:bg-surface-container transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Accounts;
