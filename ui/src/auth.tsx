import axios from "axios";
import { navigate } from "wouter/use-browser-location";
import { createContext, useContext, useEffect, useMemo, useState } from "react";

export const axiosInstance = axios.create();

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
},
(error) => {
  console.error(error);
});

// automatically re-direct to login if a 401 (error) response is received
axiosInstance.interceptors.response.use((response) => {
  return response;
}, (error) => {
  console.error(error.message);
  if (error.response.status === 401) {
    navigate('/login', { replace: true});
  }
});

const AuthContext = createContext<{ token: string | null; setToken: (newToken: string) => void }>({ token: null, setToken: () => { } });

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken_] = useState(localStorage.getItem("token"));

  const setToken = (newToken: string | null) => {
    setToken_(newToken);
  };

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
    return () => {
      // Cleanup function
    };
  }, [token]);

  const contextValue = useMemo(
    () => ({
      token,
      setToken,
    }),
    [token]
  );

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => {
    return useContext(AuthContext);
};
