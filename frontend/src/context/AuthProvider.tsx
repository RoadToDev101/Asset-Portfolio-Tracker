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
}

export const AuthContext = createContext<AuthContextProps>({
  authState: { token: null, user_id: null },
  performLogin: () => {},
  performLogout: () => {},
  updateAccessToken: () => {},
});

const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>({
    token: null,
    user_id: null,
  });
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const checkSession = async () => {
      // If we are logging out and the token is already null, do nothing
      if (isLoggingOut || !authState.token) {
        return;
      }

      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/v1/auth/refresh`,
          { withCredentials: true }
        );
        if (response.data.access_token) {
          setAuthState({
            token: response.data.access_token,
            user_id: response.data.user_id.toString(),
          });
        }
      } catch (error) {
        navigate("/");
      }
    };

    checkSession();
  }, [navigate, isLoggingOut, authState.token]);

  const performLogin = (token: string | null, user_id: string | null) => {
    setAuthState({ token, user_id });
    navigate("/dashboard");
  };

  const performLogout = () => {
    setIsLoggingOut(true);
    setAuthState({ token: null, user_id: null });
    navigate("/");
  };

  const updateAccessToken = (newToken: string) => {
    setAuthState((prevState) => ({
      ...prevState,
      token: newToken,
    }));
  };

  return (
    <AuthContext.Provider
      value={{ authState, performLogin, performLogout, updateAccessToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
