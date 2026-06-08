import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { getApiError } from "../api/axiosConfig";
import { getDatosReportes } from "../api/reportes.api";
import { Alert, LoadingState } from "../components/Feedback";
import PageHeader from "../components/PageHeader";
import StatCard from "../components/StatCard";
import { formatCurrency, formatDate, todayISO } from "../utils/formatters";
import { buildMonthlyBookings, buildRoomStatus } from "../utils/reports";

const PIE_COLORS = ["#c8a96b", "#18324d"];

function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getDatosReportes().then(setData).catch((requestError) => setError(getApiError(requestError)));
  }, []);

  const metrics = useMemo(() => {
    if (!data) return null;
    const today = todayISO();
    const activeBookings = data.reservas.filter(
      (booking) => booking.check_in <= today && booking.check_out > today,
    );
    const roomStatus = buildRoomStatus(data.reservas, data.habitaciones, today);
    return {
      available: roomStatus[0]?.value || 0,
      occupied: roomStatus[1]?.value || 0,
      activeBookings: activeBookings.length,
      revenue: data.pagos.reduce((sum, payment) => sum + Number(payment.total), 0),
    };
  }, [data]);

  if (!data && !error) return <LoadingState />;

  const monthlyBookings = buildMonthlyBookings(data?.reservas || []);
  const roomStatus = buildRoomStatus(data?.reservas || [], data?.habitaciones || [], todayISO());
  const recentBookings = [...(data?.reservas || [])]
    .sort((a, b) => b.booking_id - a.booking_id)
    .slice(0, 5);

  return (
    <>
      <PageHeader
        eyebrow="Resumen general"
        title="Dashboard"
        description="Vista en tiempo real de la operacion y el rendimiento del hotel."
      />
      <Alert>{error}</Alert>

      {data && (
        <>
          <section className="stats-grid">
            <StatCard title="Habitaciones" value={data.habitaciones.length} subtitle="Inventario total" icon="H" />
            <StatCard title="Disponibles hoy" value={metrics.available} subtitle="Sin reservas activas" icon="D" tone="gold" />
            <StatCard title="Ocupadas hoy" value={metrics.occupied} subtitle="Con estancias en curso" icon="O" tone="slate" />
            <StatCard title="Reservas activas" value={metrics.activeBookings} subtitle="Estancias de hoy" icon="R" tone="blue" />
            <StatCard title="Clientes" value={data.clientes.length} subtitle="Huespedes registrados" icon="C" />
            <StatCard title="Pagos" value={data.pagos.length} subtitle="Facturas encontradas" icon="P" tone="gold" />
            <StatCard title="Ingresos" value={formatCurrency(metrics.revenue)} subtitle="Facturacion acumulada" icon="$" tone="blue" />
          </section>

          <section className="dashboard-grid">
            <article className="panel chart-panel chart-wide">
              <div className="panel-heading">
                <div>
                  <p className="eyebrow">Demanda</p>
                  <h3>Reservas por mes</h3>
                </div>
              </div>
              {monthlyBookings.length ? (
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={monthlyBookings}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e9ef" />
                    <XAxis dataKey="mes" tickLine={false} axisLine={false} />
                    <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
                    <Tooltip />
                    <Bar dataKey="reservas" fill="#c8a96b" radius={[7, 7, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="chart-empty">No hay reservas para graficar.</div>
              )}
            </article>

            <article className="panel chart-panel">
              <div className="panel-heading">
                <div>
                  <p className="eyebrow">Inventario</p>
                  <h3>Estado de habitaciones</h3>
                </div>
              </div>
              {data.habitaciones.length ? (
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie data={roomStatus} dataKey="value" nameKey="name" innerRadius={58} outerRadius={90} paddingAngle={4}>
                      {roomStatus.map((entry, index) => (
                        <Cell key={entry.name} fill={PIE_COLORS[index]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="chart-empty">No hay habitaciones para graficar.</div>
              )}
              <div className="legend-row">
                {roomStatus.map((item, index) => (
                  <span key={item.name}>
                    <i style={{ background: PIE_COLORS[index] }} /> {item.name}: {item.value}
                  </span>
                ))}
              </div>
            </article>
          </section>

          <article className="panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Actividad reciente</p>
                <h3>Ultimas reservas</h3>
              </div>
            </div>
            <div className="reservation-list">
              {recentBookings.length === 0 && <p className="empty-message">No hay registros disponibles.</p>}
              {recentBookings.map((booking) => (
                <div className="reservation-item" key={booking.booking_id}>
                  <div className="reservation-number">#{booking.booking_id}</div>
                  <div>
                    <strong>Cliente {booking.client_id}</strong>
                    <span>Habitacion(es): {booking.room_numbers.join(", ")}</span>
                  </div>
                  <div className="reservation-dates">
                    <strong>{formatDate(booking.check_in)}</strong>
                    <span>hasta {formatDate(booking.check_out)}</span>
                  </div>
                </div>
              ))}
            </div>
          </article>
        </>
      )}
    </>
  );
}

export default Dashboard;
