import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
// import {createContext, useContext, useEffect, useMemo, useState} from "react";

// const AuthContext = createContext();

// const AuthProvider = ({children}) => {
//   const [token, setToken_] = useState(localStorage.getItem("token"));

//   const setToken = (newToken) => {
//     setToken_(newToken);
//   }

//   useEffect(() => {
//       if (token) {
//         axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
//         localStorage.setItem("token", token);
//       } else {
//         delete axios.defaults.headers.common["Authorization"];
//         localStorage.removeItem("token");
//       }
//   }, [token]);

//   const contextValue = useMemo(() => (
//       {
//         token, 
//         setToken
//       }), 
//       [token]
//   );

//   return (
//     <AuthContext.Provider value={contextValue}>
//       {children}
//     </AuthContext.Provider>
//   );
// }

// export const useAuth = () => {
//   return useContext(AuthContext);
// };

// export default AuthProvider;

// ---------

interface AuthContextType {
    isAuthenticated: boolean;
    login: (token: string) => void;
    logout: () => void;
}

interface AuthProviderProps {
    children: ReactNode;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider= ({ children }: AuthProviderProps) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('jwt');
        if (token) {
            setIsAuthenticated(true); // Check token validity if needed
        }
    }, []);

    const login = (token: string) => {
        localStorage.setItem('jwt', token);
        setIsAuthenticated(true);
    };

    const logout = () => {
        localStorage.removeItem('jwt');
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('AuthProvider cannot be undefined');
    }
    return context;
};