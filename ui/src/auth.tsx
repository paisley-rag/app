import axios from "axios";
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
    (error) => console.log(error));

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
