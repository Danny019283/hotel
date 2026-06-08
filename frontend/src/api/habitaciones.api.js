import api from "./axiosConfig";

const BASE = "/api/v1/rooms";

export const getHabitaciones = () =>
  api.get(BASE).then((response) => response.data);

export const getHabitacion = (numero) =>
  api.get(`${BASE}/${numero}`).then((response) => response.data);

export const createHabitacion = (habitacion) =>
  api.post(BASE, habitacion).then((response) => response.data);

export const updateHabitacion = (numero, habitacion) =>
  api.put(`${BASE}/${numero}`, habitacion).then((response) => response.data);

export const deleteHabitacion = (numero) => api.delete(`${BASE}/${numero}`);
