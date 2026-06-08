import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 12000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("hotel_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && window.location.pathname !== "/login") {
      localStorage.removeItem("hotel_user");
      localStorage.removeItem("hotel_token");
      window.location.assign("/login");
    }
    return Promise.reject(error);
  },
);

export const getApiError = (error) => {
  if (!error.response) {
    return "No se pudo conectar con el servidor. Verifica que el backend este activo.";
  }

  const data = error.response.data;
  if (typeof data?.message === "string") return data.message;
  if (typeof data?.detail === "string") return data.detail;
  if (Array.isArray(data?.detail)) {
    return data.detail.map((item) => item.msg).join(". ");
  }
  return "La solicitud no pudo completarse.";
};

export default api;
