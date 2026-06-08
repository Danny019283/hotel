import { getClientes } from "./clientes.api";
import { getHabitaciones } from "./habitaciones.api";
import { getPagos } from "./pagos.api";
import { getReservas } from "./reservas.api";

export const getDatosReportes = async () => {
  const [habitaciones, reservas, clientes, pagos] = await Promise.all([
    getHabitaciones(),
    getReservas(),
    getClientes(),
    getPagos(),
  ]);

  return { habitaciones, reservas, clientes, pagos };
};
