import { useEffect, useState } from "react";
import { getApiError } from "../api/axiosConfig";
import {
  createPago,
  deletePago,
  getMetodosPago,
  getPagos,
  getResumenPago,
  updatePago,
} from "../api/pagos.api";
import { getReservas } from "../api/reservas.api";
import DataTable from "../components/DataTable";
import { Alert, LoadingState } from "../components/Feedback";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import StatCard from "../components/StatCard";
import { getSession, isAdminRole } from "../utils/auth";
import { formatCurrency } from "../utils/formatters";

function Pagos() {
  const canManage = isAdminRole(getSession()?.role);
  const [payments, setPayments] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [methods, setMethods] = useState([]);
  const [form, setForm] = useState({ booking_id: "", payment_method_id: "" });
  const [editing, setEditing] = useState(null);
  const [summary, setSummary] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState({ type: "", message: "" });

  const loadData = async () => {
    try {
      setLoading(true);
      const [paymentData, bookingData, methodData] = await Promise.all([
        getPagos(),
        getReservas(),
        getMetodosPago(),
      ]);
      setPayments(paymentData);
      setBookings(bookingData);
      setMethods(methodData.filter((method) => method.active));
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const openCreate = () => {
    setEditing(null);
    setForm({
      booking_id: "",
      payment_method_id: String(methods[0]?.payment_method_id || ""),
    });
    setModalOpen(true);
  };

  const openEdit = (payment) => {
    setEditing(payment.bill_id);
    setForm({
      booking_id: String(payment.booking_id),
      payment_method_id: String(payment.payment_method_id),
    });
    setModalOpen(true);
  };

  const submit = async (event) => {
    event.preventDefault();
    if (Number(form.booking_id) <= 0 || Number(form.payment_method_id) <= 0) {
      setFeedback({ type: "error", message: "Selecciona una reserva y un metodo de pago." });
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updatePago(editing, form.payment_method_id);
      } else {
        await createPago({
          booking_id: Number(form.booking_id),
          payment_method_id: Number(form.payment_method_id),
        });
      }
      setModalOpen(false);
      setFeedback({
        type: "success",
        message: editing ? "Metodo de pago actualizado." : "Factura generada correctamente.",
      });
      await loadData();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setSaving(false);
    }
  };

  const remove = async (payment) => {
    if (!window.confirm(`Eliminar la factura #${payment.bill_id}?`)) return;
    try {
      await deletePago(payment.bill_id);
      setFeedback({ type: "success", message: "Factura eliminada correctamente." });
      await loadData();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    }
  };

  const showSummary = async (payment) => {
    try {
      setSummary(await getResumenPago(payment.bill_id));
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    }
  };

  const methodName = (id) =>
    methods.find((method) => method.payment_method_id === id)?.name || `Metodo ${id}`;
  const billedBookingIds = new Set(payments.map((payment) => payment.booking_id));
  const unbilledBookings = bookings.filter(
    (booking) => !billedBookingIds.has(booking.booking_id),
  );
  const total = payments.reduce((sum, payment) => sum + Number(payment.total), 0);

  const columns = [
    { key: "bill_id", label: "Factura", render: (payment) => <strong>#{payment.bill_id}</strong> },
    { key: "booking_id", label: "Reserva", render: (payment) => `#${payment.booking_id}` },
    {
      key: "payment_method_id",
      label: "Metodo",
      render: (payment) => methodName(payment.payment_method_id),
    },
    { key: "total", label: "Total calculado", render: (payment) => <strong>{formatCurrency(payment.total)}</strong> },
    {
      key: "actions",
      label: "Acciones",
      render: (payment) => (
        <div className="table-actions">
          <button className="button button-small button-ghost" onClick={() => showSummary(payment)}>
            Detalle
          </button>
          {canManage && (
            <>
              <button className="button button-small button-secondary" onClick={() => openEdit(payment)}>
                Cambiar metodo
              </button>
              <button className="button button-small button-danger" onClick={() => remove(payment)}>
                Eliminar
              </button>
            </>
          )}
        </div>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        eyebrow="Facturacion"
        title="Pagos y facturas"
        description="Genera facturas desde reservas y consulta los ingresos almacenados."
        action={<button className="button button-primary" onClick={openCreate}>+ Generar factura</button>}
      />
      <Alert type={feedback.type}>{feedback.message}</Alert>
      <div className="scope-note">
        El total se calcula en el backend según habitaciones y noches. No se ingresa manualmente.
      </div>
      <section className="stats-grid stats-compact">
        <StatCard title="Facturas" value={payments.length} subtitle="Registros persistidos" icon="F" />
        <StatCard title="Ingresos totales" value={formatCurrency(total)} subtitle="Suma de facturas" icon="$" tone="gold" />
        <StatCard title="Sin facturar" value={unbilledBookings.length} subtitle="Reservas pendientes" icon="P" tone="slate" />
      </section>
      <article className="panel">
        {loading ? <LoadingState /> : <DataTable columns={columns} rows={payments} rowKey="bill_id" />}
      </article>

      {modalOpen && (
        <Modal title={editing ? `Cambiar metodo de factura #${editing}` : "Generar factura"} onClose={() => setModalOpen(false)}>
          <form onSubmit={submit} className="form-grid">
            <label>
              Reserva
              <select
                value={form.booking_id}
                onChange={(event) => setForm({ ...form, booking_id: event.target.value })}
                disabled={Boolean(editing)}
                required
              >
                <option value="">Seleccionar reserva</option>
                {(editing ? bookings.filter((booking) => booking.booking_id === Number(form.booking_id)) : unbilledBookings)
                  .map((booking) => (
                    <option key={booking.booking_id} value={booking.booking_id}>
                      #{booking.booking_id} - Cliente {booking.client_id}
                    </option>
                  ))}
              </select>
            </label>
            <label>
              Metodo de pago
              <select
                value={form.payment_method_id}
                onChange={(event) => setForm({ ...form, payment_method_id: event.target.value })}
                required
              >
                <option value="">Seleccionar metodo</option>
                {methods.map((method) => (
                  <option key={method.payment_method_id} value={method.payment_method_id}>
                    {method.name}
                  </option>
                ))}
              </select>
            </label>
            <div className="form-actions form-full">
              <button type="button" className="button button-ghost" onClick={() => setModalOpen(false)}>Cancelar</button>
              <button className="button button-primary" disabled={saving}>{saving ? "Guardando..." : "Confirmar"}</button>
            </div>
          </form>
        </Modal>
      )}

      {summary && (
        <Modal title={`Factura #${summary.bill_id}`} onClose={() => setSummary(null)}>
          <div className="invoice">
            <div><span>Reserva</span><strong>#{summary.booking_id}</strong></div>
            <div><span>Cliente</span><strong>{summary.client_id}</strong></div>
            <div><span>Habitaciones</span><strong>{summary.room_numbers.join(", ")}</strong></div>
            <div><span>Metodo de pago</span><strong>{methodName(summary.payment_method_id)}</strong></div>
            <div className="invoice-total"><span>Total</span><strong>{formatCurrency(summary.total)}</strong></div>
          </div>
        </Modal>
      )}
    </>
  );
}

export default Pagos;
