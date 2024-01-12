import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "@/context/AuthProvider";
import LoadingSpinner from "./LoadingSpinner";

interface ProtectedRouteProps {
  component: React.ComponentType;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  component: Component,
}) => {
  const { loading } = useContext(AuthContext);
  const token = localStorage.getItem("token");

  // If the authentication state is still loading, return null or a loading spinner
  if (loading) {
    return <LoadingSpinner />;
  }

  // Once loading is complete, render the component if the user is authenticated
  // or redirect to the login page if they're not
  return token ? <Component /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
