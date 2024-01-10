import axios from "axios";
import { useContext } from "react";
import { AuthContext } from "@/context/AuthProvider";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
  withCredentials: true,
});

// Add a response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { updateAccessToken, performLogout } = useContext(AuthContext);
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        // Call your refresh token endpoint
        const refreshTokenResponse = await axiosInstance.get(
          "/v1/auth/refresh"
        );
        const newAccessToken = refreshTokenResponse.data.access_token;

        // Update context with new access token
        updateAccessToken(newAccessToken);

        // Modify the original request with new token and retry
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return axios(originalRequest);
      } catch (refreshError) {
        // Handle refresh token expiration (e.g., redirect to login)
        performLogout();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
