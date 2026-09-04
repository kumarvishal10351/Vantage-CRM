import React from 'react';

export const PriorityBadge = ({ tier, score }) => {
  if (tier === 'Tier 1' || tier === 'Tier 1 - High' || tier === 'High') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-semibold bg-error-container text-on-error-container border border-error/20">
        <span className="w-1.5 h-1.5 rounded-full bg-error"></span>
        <span>Tier 1 High</span>
        {score !== undefined && <span className="opacity-80">({score} pts)</span>}
      </span>
    );
  }

  if (tier === 'Tier 2' || tier === 'Tier 2 - Medium' || tier === 'Medium') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono font-medium bg-secondary-container text-on-secondary-fixed-variant border border-secondary/20">
        <span className="w-1.5 h-1.5 rounded-full bg-primary-container"></span>
        <span>Tier 2 Medium</span>
        {score !== undefined && <span className="opacity-80">({score} pts)</span>}
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-label-xs-mono text-label-xs-mono text-secondary bg-surface-container-high border border-outline-variant/40">
      <span className="w-1.5 h-1.5 rounded-full bg-outline"></span>
      <span>Tier 3 Lower</span>
      {score !== undefined && <span className="opacity-80">({score} pts)</span>}
    </span>
  );
};

export default PriorityBadge;
