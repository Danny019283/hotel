import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
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
import { formatCurrency } from "../utils/formatters";
import {
  buildBookingsByRoomType,
  buildMonthlyBookings,
  buildMonthlyRevenue,
  buildRoomStatus,
} from "../utils/reports";

const PIE_COLORS = ["#c8a96b", "#18324d"];

function Reportes() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getDatosReportes().then(setData).catch((requestError) => setError(getApiError(requestError)));
  }, []);

  const reports = useMemo(() => {
    if (!data) return null;
    return {
      bookings: buildMonthlyBookings(data.reservas),
      roomTypes: buildBookingsByRoomType(data.reservas, data.habitaciones),
      revenue: buildMonthlyRevenue(data.pagos, data.reservas),
      roomStatus: buildRoomStatus(data.habitaciones),
    };
  }, [data]);

  if (!data && !error) return <LoadingState />;

  return (
    <>
      <PageHeader
        eyebrow="Analitica"
        title="Reportes"
        description="Indicadores calculados directamente desde habitaciones, reservas y facturas."
      />
      <Alert>{error}</Alert>
      {reports && (
        <section className="reports-grid">
          <article className="panel chart-panel">
            <div className="panel-heading">
              <div><p className="eyebrow">Tendencia</p><h3>Reservas por mes</h3></div>
            </div>
            {reports.bookings.length ? (
              <ResponsiveContainer width="100%" height={310}>
                <LineChart data={reports.bookings}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e9ef" />
                  <XAxis dataKey="mes" tickLine={false} axisLine={false} />
                  <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
                  <Tooltip />
                  <Line type="monotone" dataKey="reservas" stroke="#c8a96b" strokeWidth={3} dot={{ fill: "#c8a96b" }} />
                </LineChart>
              </ResponsiveContainer>
            ) : <div className="chart-empty">No hay reservas para graficar.</div>}
          </article>

          <article className="panel chart-panel">
            <div className="panel-heading">
              <div><p className="eyebrow">Preferencias</p><h3>Reservas por tipo</h3></div>
            </div>
            {reports.roomTypes.length ? (
              <ResponsiveContainer width="100%" height={310}>
                <BarChart data={reports.roomTypes} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e5e9ef" />
                  <XAxis type="number" allowDecimals={false} tickLine={false} axisLine={false} />
                  <YAxis type="category" dataKey="tipo" width={90} tickLine={false} axisLine={false} />
                  <Tooltip />
                  <Bar dataKey="reservas" fill="#18324d" radius={[0, 7, 7, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : <div className="chart-empty">No hay tipos reservados para graficar.</div>}
          </article>

          <article className="panel chart-panel">
            <div className="panel-heading">
              <div><p className="eyebrow">Disponibilidad</p><h3>Estado de habitaciones</h3></div>
            </div>
            {data.habitaciones.length ? (
              <>
                <ResponsiveContainer width="100%" height={270}>
                  <PieChart>
                    <Pie
                      data={reports.roomStatus}
                      dataKey="value"
                      nameKey="name"
                      innerRadius={60}
                      outerRadius={95}
                      paddingAngle={4}
                    >
                      {reports.roomStatus.map((item, index) => (
                        <Cell key={item.name} fill={PIE_COLORS[index]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                <div className="legend-row">
                  {reports.roomStatus.map((item, index) => (
                    <span key={item.name}>
                      <i style={{ background: PIE_COLORS[index] }} /> {item.name}: {item.value}
                    </span>
                  ))}
                </div>
              </>
            ) : <div className="chart-empty">No hay habitaciones para graficar.</div>}
          </article>

          <article className="panel chart-panel report-wide">
            <div className="panel-heading">
              <div><p className="eyebrow">Rendimiento</p><h3>Ingresos por mes de reserva</h3></div>
            </div>
            {reports.revenue.length ? (
              <ResponsiveContainer width="100%" height={330}>
                <BarChart data={reports.revenue}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e9ef" />
                  <XAxis dataKey="mes" tickLine={false} axisLine={false} />
                  <YAxis tickFormatter={(value) => `${Math.round(value / 1000)}k`} tickLine={false} axisLine={false} />
                  <Tooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  <Bar name="Ingresos" dataKey="ingresos" fill="#c8a96b" radius={[7, 7, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : <div className="chart-empty">No hay facturas para graficar ingresos.</div>}
          </article>
        </section>
      )}
    </>
  );
}

export default Reportes;
