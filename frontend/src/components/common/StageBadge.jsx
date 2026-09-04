import React from 'react';

export const StageBadge = ({ stage }) => {
  const normalized = (stage || '').toLowerCase();

  if (normalized === 'won') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold bg-tertiary/10 text-tertiary-container border border-tertiary-container/30">
        <span className="w-1.5 h-1.5 rounded-full bg-tertiary-container"></span>
        <span>Won</span>
      </span>
    );
  }

  if (normalized === 'engaging') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-medium bg-primary-fixed/40 text-primary-container border border-primary-container/20">
        <span className="w-1.5 h-1.5 rounded-full bg-primary-container animate-pulse"></span>
        <span>Engaging</span>
      </span>
    );
  }

  if (normalized === 'prospecting') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono text-secondary bg-surface-container-high border border-outline-variant/40">
        <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
        <span>Prospecting</span>
      </span>
    );
  }

  if (normalized === 'lost') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono text-on-error-container bg-error-container/60 border border-error/30">
        <span className="w-1.5 h-1.5 rounded-full bg-error"></span>
        <span>Lost</span>
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono text-secondary bg-surface-container">
      <span>{stage || '—'}</span>
    </span>
  );
};

export default StageBadge;
