import axios from "axios";
import React, { createContext, useState, ReactNode, useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface AuthState {
  token: string | null;
  user_id: string | null;
}

interface AuthContextProps {
  authState: AuthState;
  performLogin: (token: string | null, user_id: string | null) => void;
  performLogout: () => void;
  updateAccessToken: (newToken: string) => void;
  loading: boolean;
}

export const AuthContext = createContext<AuthContextProps>({
  authState: { token: null, user_id: null },
  performLogin: () => {},
  performLogout: () => {},
  updateAccessToken: () => {},
  loading: true,
});

const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>({
    token: localStorage.getItem("token"),
    user_id: null,
  });
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    const checkSession = async () => {
      // If we're logging out, or the token is already null and never logging out, don't do anything
      if (isLoggingOut || (!authState.token && !isLoggingOut)) {
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/v1/auth/refresh`,
          { withCredentials: true }
        );
        if (response.data.access_token) {
          setAuthState((prevState) => ({
            ...prevState,
            token: response.data.access_token,
          }));
          localStorage.setItem("token", response.data.access_token);
        }
      } catch (error) {
        navigate("/");
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, [navigate, isLoggingOut, authState.token]);

  const performLogin = (token: string | null, user_id: string | null) => {
    setAuthState({ token, user_id });
    if (token) {
      localStorage.setItem("token", token);
    }
    navigate("/dashboard");
  };

  const performLogout = () => {
    setIsLoggingOut(true);
    setAuthState({ token: null, user_id: null });
    localStorage.removeItem("token");
    navigate("/");
  };

  const updateAccessToken = (newToken: string) => {
    setAuthState((prevState) => ({
      ...prevState,
      token: newToken,
    }));
    localStorage.setItem("token", newToken);
  };

  return (
    <AuthContext.Provider
      value={{
        authState,
        performLogin,
        performLogout,
        updateAccessToken,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
