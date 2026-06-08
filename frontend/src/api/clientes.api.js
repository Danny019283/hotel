import api from "./axiosConfig";

const BASE = "/api/v1/clients";

export const getClientes = () =>
  api.get(BASE).then((response) => response.data);

export const getCliente = (id) =>
  api.get(`${BASE}/${id}`).then((response) => response.data);

export const createCliente = (cliente) =>
  api.post(BASE, cliente).then((response) => response.data);

export const updateCliente = (id, cliente) =>
  api.put(`${BASE}/${id}`, cliente).then((response) => response.data);

export const deleteCliente = (id) => api.delete(`${BASE}/${id}`);
