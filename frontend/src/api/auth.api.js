import api from "./axiosConfig";

const BASE = "/api/v1/auth";

export const login = (credentials) =>
  api.post(`${BASE}/login`, credentials).then((response) => response.data);

export const registerUser = (user) =>
  api.post(`${BASE}/register`, user).then((response) => response.data);

export const changePassword = (payload) =>
  api.put(`${BASE}/password`, payload).then((response) => response.data);
