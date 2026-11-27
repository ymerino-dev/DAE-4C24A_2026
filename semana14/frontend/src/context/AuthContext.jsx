import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from 'react';

import { TOKEN_STORAGE_KEY } from '../services/api';
import { login as loginRequest } from '../services/authService';

const USER_STORAGE_KEY = 'user';

const AuthContext = createContext(null);

const getStoredToken = () => localStorage.getItem(TOKEN_STORAGE_KEY);

const getStoredUser = () => {
  try {
    return JSON.parse(localStorage.getItem(USER_STORAGE_KEY));
  } catch {
    return null;
  }
};

export function AuthProvider({ children }) {
  const [token, setToken] = useState(getStoredToken);
  const [user, setUser] = useState(getStoredUser);

  const login = useCallback(async (username, password) => {
    const session = await loginRequest(username, password);

    localStorage.setItem(TOKEN_STORAGE_KEY, session.token);
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(session.user));
    setToken(session.token);
    setUser(session.user);

    return session.user;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
    setToken(null);
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({
      token,
      user,
      isAuthenticated: Boolean(token),
      login,
      logout,
    }),
    [token, user, login, logout],
  );

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}

// oxlint-disable-next-line react/only-export-components
export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider.');
  }

  return context;
}
