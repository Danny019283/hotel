import api from "./axiosConfig";

const BASE = "/api/v1/room-types";

export const getTiposHabitacion = () =>
  api.get(BASE).then((response) => response.data);

export const getTipoHabitacion = (id) =>
  api.get(`${BASE}/${id}`).then((response) => response.data);

export const createTipoHabitacion = (roomType) =>
  api.post(BASE, roomType).then((response) => response.data);

export const updateTipoHabitacion = (id, roomType) =>
  api.put(`${BASE}/${id}`, roomType).then((response) => response.data);

export const updateEstadoTipoHabitacion = (id, active) =>
  api.patch(`${BASE}/${id}/status`, { active }).then((response) => response.data);

export const deleteTipoHabitacion = (id) =>
  api.delete(`${BASE}/${id}`);
