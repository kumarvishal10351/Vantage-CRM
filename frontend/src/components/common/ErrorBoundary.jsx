import React from 'react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-space-xl text-center">
          <div className="w-12 h-12 rounded-xl bg-error-container text-on-error-container flex items-center justify-center mb-space-sm">
            <span className="material-symbols-outlined text-[26px]">warning</span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface mb-1">
            Application View Notice
          </h1>
          <p className="font-body-sm text-body-sm text-secondary max-w-md mb-space-base">
            {this.state.error?.message || 'An unexpected rendering error occurred.'}
          </p>
          <button
            onClick={() => {
              this.setState({ hasError: false, error: null });
              window.location.reload();
            }}
            className="h-8 px-space-md bg-primary-container text-on-primary font-label-md text-label-md rounded flex items-center gap-1 shadow-xs"
          >
            <span className="material-symbols-outlined text-[16px]">refresh</span>
            <span>Reload Application</span>
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
