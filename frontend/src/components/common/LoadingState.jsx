import React from 'react';

export const LoadingState = ({ message = 'Loading CRM data from engine...' }) => {
  return (
    <div className="w-full py-16 flex flex-col items-center justify-center text-center">
      <div className="w-8 h-8 rounded-full border-2 border-primary-container border-t-transparent animate-spin mb-space-sm"></div>
      <span className="font-label-sm text-label-sm text-secondary tracking-wide uppercase">
        {message}
      </span>
    </div>
  );
};

export default LoadingState;
