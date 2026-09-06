import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('admin@crm.local');
  const [password, setPassword] = useState('AdminPass123!');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await login(email, password);
      if (result.success) {
        navigate('/');
      } else {
        setError(result.message);
      }
    } catch {
      setError('An unexpected error occurred during login.');
    } finally {
      setLoading(false);
    }
  };

  const setRoleDemo = (demoEmail, demoPass) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center px-space-base py-space-xl select-none">
      <div className="w-full max-w-md bg-surface-container-lowest rounded-2xl border border-outline-variant/40 shadow-lg p-space-xl">
        {/* Header */}
        <div className="flex flex-col items-center text-center mb-space-xl">
          <div className="w-12 h-12 rounded-xl bg-primary-container text-on-primary flex items-center justify-center font-bold text-xl shadow-xs mb-space-sm">
            <span className="material-symbols-outlined text-[26px]">insights</span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight">
            Vantage
          </h1>
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase tracking-wider mt-1">
            Enterprise Revenue Operations Platform
          </span>
        </div>

        {error && (
          <div className="mb-space-base p-space-sm bg-error-container/40 border border-error/30 text-on-error-container rounded-lg font-body-sm text-body-sm flex items-center gap-2">
            <span className="material-symbols-outlined text-[18px]">error</span>
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-space-md">
          <div>
            <label className="block font-label-xs-mono text-label-xs-mono uppercase text-secondary mb-1">
              Email Address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full h-10 px-space-sm bg-surface-container-low border border-outline-variant/60 rounded-lg font-body-sm text-body-sm text-on-surface focus:outline-none focus:border-primary-container"
              placeholder="Enter email..."
            />
          </div>

          <div>
            <label className="block font-label-xs-mono text-label-xs-mono uppercase text-secondary mb-1">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full h-10 px-space-sm bg-surface-container-low border border-outline-variant/60 rounded-lg font-body-sm text-body-sm text-on-surface focus:outline-none focus:border-primary-container"
              placeholder="Enter password..."
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full h-10 bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md rounded-lg flex items-center justify-center gap-space-xs transition-colors shadow-xs mt-space-base"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-on-primary border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <>
                <span className="material-symbols-outlined text-[18px]">login</span>
                <span>Sign In to Vantage CRM</span>
              </>
            )}
          </button>
        </form>

        {/* Preset Role Credentials */}
        <div className="mt-space-lg pt-space-md border-t border-outline-variant/20">
          <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block text-center mb-2">
            Pre-Seeded Demo Roles
          </span>
          <div className="grid grid-cols-3 gap-1.5 text-center">
            <button
              type="button"
              onClick={() => setRoleDemo('admin@crm.local', 'AdminPass123!')}
              className="p-1.5 rounded bg-surface-container-low hover:bg-surface-container border border-outline-variant/40 font-label-xs-mono text-label-xs-mono text-on-surface transition-colors"
            >
              Admin
            </button>
            <button
              type="button"
              onClick={() => setRoleDemo('manager@crm.local', 'ManagerPass123!')}
              className="p-1.5 rounded bg-surface-container-low hover:bg-surface-container border border-outline-variant/40 font-label-xs-mono text-label-xs-mono text-on-surface transition-colors"
            >
              Manager
            </button>
            <button
              type="button"
              onClick={() => setRoleDemo('agent@crm.local', 'AgentPass123!')}
              className="p-1.5 rounded bg-surface-container-low hover:bg-surface-container border border-outline-variant/40 font-label-xs-mono text-label-xs-mono text-on-surface transition-colors"
            >
              Agent
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
