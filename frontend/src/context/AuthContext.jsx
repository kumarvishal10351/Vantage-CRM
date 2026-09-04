import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../api/client';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('vantage_auth_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('vantage_auth_token');
      if (storedToken) {
        try {
          const res = await authApi.getMe();
          setUser(res.data);
        } catch {
          // Token expired or invalid
          localStorage.removeItem('vantage_auth_token');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const res = await authApi.login(email, password);
      const authToken = res.data.access_token || res.data.token;
      localStorage.setItem('vantage_auth_token', authToken);
      setToken(authToken);
      // Fetch user profile
      try {
        const meRes = await authApi.getMe();
        setUser(meRes.data);
      } catch {
        setUser(res.data.user || { email, full_name: 'Sarah Jenkins', role: 'VP Sales Operations' });
      }
      return { success: true };
    } catch (err) {
      return {
        success: false,
        message: err.response?.data?.detail || 'Authentication failed. Please verify credentials.',
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('vantage_auth_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
