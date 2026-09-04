import React from 'react';

export const HelpDocs = () => {
  return (
    <div className="flex flex-col w-full max-w-4xl">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Documentation</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Help &amp; Documentation</span>
        </div>
        <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
          Vantage CRM Documentation &amp; Standards
        </h1>
        <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
          Operational definitions, priority framework rules, and database schema conventions.
        </p>
      </div>

      <div className="space-y-space-lg">
        {/* Priority Framework */}
        <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
          <div className="flex items-center gap-2 text-primary-container font-headline-sm text-headline-sm mb-space-sm">
            <span className="material-symbols-outlined text-[20px]">flag</span>
            <h2>Operational Opportunity Prioritization Score (0–100 Points)</h2>
          </div>
          <p className="font-body-sm text-body-sm text-secondary leading-relaxed mb-space-base">
            The prioritization engine allocates sales focus exclusively across open pipeline opportunities (2,089 deals). It uses pre-outcome variables to avoid target leakage and is <strong>strictly an operational focus score, not a win probability prediction</strong>.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-space-sm">
            <div className="p-space-sm rounded bg-error-container/20 border border-error/30">
              <strong className="text-on-error-container font-semibold block text-sm">Tier 1 — High Priority</strong>
              <span className="text-xs text-secondary mt-1 block">Score 70–100 (428 deals). Requires immediate executive escalation and active senior rep cadence.</span>
            </div>
            <div className="p-space-sm rounded bg-secondary-container/30 border border-secondary/30">
              <strong className="text-on-secondary-container font-semibold block text-sm">Tier 2 — Medium Priority</strong>
              <span className="text-xs text-secondary mt-1 block">Score 45–69 (1,033 deals). Standard deal cadence progressing through engagement milestones.</span>
            </div>
            <div className="p-space-sm rounded bg-surface-container border border-outline-variant/40">
              <strong className="text-on-surface font-semibold block text-sm">Tier 3 — Lower Priority</strong>
              <span className="text-xs text-secondary mt-1 block">Score 0–44 (628 deals). Secondary focus, nurture automation, or re-qualification.</span>
            </div>
          </div>
        </div>

        {/* Stages Definition */}
        <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
          <div className="flex items-center gap-2 text-primary-container font-headline-sm text-headline-sm mb-space-sm">
            <span className="material-symbols-outlined text-[20px]">view_kanban</span>
            <h2>Sales Pipeline Lifecycle Stages</h2>
          </div>
          <ul className="space-y-space-sm text-body-sm text-secondary">
            <li>
              <strong className="text-on-surface">1. Prospecting:</strong> Initial discovery and business requirements identification (500 active deals).
            </li>
            <li>
              <strong className="text-on-surface">2. Engaging:</strong> Active proposal, demonstration, and contract negotiation (1,589 active deals).
            </li>
            <li>
              <strong className="text-on-surface">3. Won:</strong> Successfully executed contract with realized revenue (4,238 closed deals, $10,005,534 total).
            </li>
            <li>
              <strong className="text-on-surface">4. Lost:</strong> Formally discontinued or disqualified opportunity (2,473 closed deals).
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default HelpDocs;
