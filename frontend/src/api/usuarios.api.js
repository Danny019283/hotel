import { changePassword as changePasswordApi, registerUser as registerUserApi } from "./auth.api";
import api from "./axiosConfig";

const BASE = "/api/v1/auth/users";

export const getUsuarios = () =>
  api.get(BASE).then((response) => response.data);

export const registerUser = registerUserApi;

export const updateUsuario = (username, changes) =>
  api.patch(`${BASE}/${username}/role`, changes).then((response) => response.data);

export const deleteUsuario = (username) =>
  api.delete(`${BASE}/${username}`);

export const changePassword = changePasswordApi;
