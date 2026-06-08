import api from "./axiosConfig";

const BASE = "/api/v1/bookings";

export const getReservas = () =>
  api.get(BASE).then((response) => response.data);

export const getReserva = (id) =>
  api.get(`${BASE}/${id}`).then((response) => response.data);

export const createReserva = (reserva) =>
  api.post(BASE, reserva).then((response) => response.data);

export const updateFechasReserva = (id, fechas) =>
  api.put(`${BASE}/${id}/dates`, fechas).then((response) => response.data);

export const deleteReserva = (id) => api.delete(`${BASE}/${id}`);

export const getHistorialCliente = (clientId) =>
  api
    .get(`${BASE}/client/${clientId}/history`)
    .then((response) => response.data);

export const getFechasOcupadasPorHabitacion = (roomNumber) =>
  api
    .get(`${BASE}/rooms/${roomNumber}/occupied-ranges`)
    .then((response) => response.data);
