import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "@/context/AuthProvider";
import LoadingSpinner from "@pages/LoadingSpinner";

interface ProtectedRouteProps {
  component: React.ComponentType;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  component: Component,
}) => {
  const { loading, authState } = useContext(AuthContext);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!authState.token) {
    return <Navigate to="/login" />;
  }

  return <Component />;
};

export default ProtectedRoute;
