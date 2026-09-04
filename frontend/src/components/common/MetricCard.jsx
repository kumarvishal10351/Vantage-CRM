import React from 'react';

export const MetricCard = ({ label, value, change, changePositive, icon, subtext, formatAsMoney, formatAsPercent }) => {
  const formattedValue = () => {
    if (value === undefined || value === null) return '—';
    if (formatAsMoney) {
      return `$${Number(value).toLocaleString('en-US', { maximumFractionDigits: 0 })}`;
    }
    if (formatAsPercent) {
      return `${Number(value).toFixed(1)}%`;
    }
    if (typeof value === 'number') {
      return Number(value).toLocaleString('en-US');
    }
    return value;
  };

  return (
    <div className="bg-surface-container-lowest rounded-xl p-space-base border border-outline-variant/30 shadow-xs flex flex-col justify-between select-none">
      <div className="flex items-center justify-between">
        <span className="font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          {label}
        </span>
        {icon && (
          <span className="material-symbols-outlined text-[18px] text-secondary">
            {icon}
          </span>
        )}
      </div>

      <div className="mt-space-sm flex items-baseline gap-space-xs">
        <span className="font-metric-mono-lg text-metric-mono-lg font-bold text-on-surface tnum tracking-tight">
          {formattedValue()}
        </span>
        {change && (
          <span
            className={`px-1.5 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold ${
              changePositive
                ? 'bg-tertiary-container/10 text-tertiary-container'
                : 'bg-error-container/60 text-on-error-container'
            }`}
          >
            {change}
          </span>
        )}
      </div>

      {subtext && (
        <span className="font-label-sm text-label-sm text-secondary mt-space-2xs truncate">
          {subtext}
        </span>
      )}
    </div>
  );
};

export default MetricCard;
