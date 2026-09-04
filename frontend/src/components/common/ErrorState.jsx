import React from 'react';

export const ErrorState = ({ message = 'Failed to load data from the CRM backend.', onRetry }) => {
  return (
    <div className="w-full py-12 px-space-lg flex flex-col items-center justify-center text-center bg-error-container/20 rounded-xl border border-error/30">
      <div className="w-10 h-10 rounded-lg bg-error-container text-on-error-container flex items-center justify-center mb-space-sm">
        <span className="material-symbols-outlined text-[22px]">error</span>
      </div>
      <h3 className="font-headline-sm text-headline-sm text-on-error-container mb-1">
        API Connection Notice
      </h3>
      <p className="font-body-sm text-body-sm text-secondary max-w-md mb-space-md">
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="h-8 px-space-md bg-surface-container-lowest hover:bg-surface-container text-on-surface font-label-md text-label-md rounded border border-outline-variant/60 shadow-xs flex items-center gap-1 transition-colors"
        >
          <span className="material-symbols-outlined text-[16px]">refresh</span>
          <span>Retry Request</span>
        </button>
      )}
    </div>
  );
};

export default ErrorState;
