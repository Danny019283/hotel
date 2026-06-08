import api from "./axiosConfig";

const BASE = "/api/v1/bills";

export const getPagos = () =>
  api.get(BASE).then((response) => response.data);

export const createPago = (pago) =>
  api.post(BASE, pago).then((response) => response.data);

export const getPago = (id) =>
  api.get(`${BASE}/${id}`).then((response) => response.data);

export const getPagoPorReserva = (bookingId) =>
  api.get(`${BASE}/booking/${bookingId}`).then((response) => response.data);

export const getResumenPago = (id) =>
  api.get(`${BASE}/${id}/summary`).then((response) => response.data);

export const updatePago = (id, paymentMethodId) =>
  api
    .patch(`${BASE}/${id}/payment-method`, {
      payment_method_id: Number(paymentMethodId),
    })
    .then((response) => response.data);

export const deletePago = (id) => api.delete(`${BASE}/${id}`);

export const getMetodosPago = () =>
  api.get("/api/v1/payment-methods").then((response) => response.data);
