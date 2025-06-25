import axios from "axios";

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api/v1",
  withCredentials: true,
});

instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        // Attempt to refresh the token
        const response = await instance.post(
          "/auth/refresh",
          {},
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        // Update the Authorization header with the new token
        instance.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${response.data.token}`;
        return instance(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default instance;