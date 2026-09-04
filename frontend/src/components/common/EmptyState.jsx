import React from 'react';

export const EmptyState = ({ title = 'No records found', description = 'Try adjusting your filters or search query.', icon = 'inbox' }) => {
  return (
    <div className="w-full py-16 px-space-lg flex flex-col items-center justify-center text-center bg-surface-container-lowest rounded-xl border border-outline-variant/30">
      <div className="w-12 h-12 rounded-xl bg-surface-container flex items-center justify-center text-secondary mb-space-sm">
        <span className="material-symbols-outlined text-[24px]">{icon}</span>
      </div>
      <h3 className="font-headline-sm text-headline-sm text-on-surface mb-1">
        {title}
      </h3>
      <p className="font-body-sm text-body-sm text-secondary max-w-md">
        {description}
      </p>
    </div>
  );
};

export default EmptyState;
