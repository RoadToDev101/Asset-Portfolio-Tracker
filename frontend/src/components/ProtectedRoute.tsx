import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "@/context/AuthProvider";

interface ProtectedRouteProps {
  component: React.ComponentType;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  component: Component,
}) => {
  const { authState } = useContext(AuthContext);

  return authState.token ? <Component /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
