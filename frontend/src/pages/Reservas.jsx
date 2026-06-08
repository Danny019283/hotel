import { useEffect, useState } from "react";
import { getApiError } from "../api/axiosConfig";
import { getClientes } from "../api/clientes.api";
import { getHabitaciones } from "../api/habitaciones.api";
import {
  createReserva,
  deleteReserva,
  getReservas,
  updateFechasReserva,
} from "../api/reservas.api";
import DataTable from "../components/DataTable";
import { Alert, LoadingState } from "../components/Feedback";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import { formatDate, todayISO } from "../utils/formatters";

const initialForm = {
  client_id: "",
  room_numbers: [],
  check_in: "",
  check_out: "",
};

const getBookingStatus = (booking) => {
  const today = todayISO();
  if (booking.check_out < today) return { label: "Finalizada", className: "badge-muted" };
  if (booking.check_in > today) return { label: "Proxima", className: "badge-gold" };
  return { label: "Activa", className: "badge-success" };
};

function Reservas() {
  const [bookings, setBookings] = useState([]);
  const [clients, setClients] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState({ type: "", message: "" });

  const loadData = async () => {
    try {
      setLoading(true);
      const [bookingData, clientData, roomData] = await Promise.all([
        getReservas(),
        getClientes(),
        getHabitaciones(),
      ]);
      setBookings(bookingData);
      setClients(clientData);
      setRooms(roomData);
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
    setForm(initialForm);
    setModalOpen(true);
  };

  const openEdit = (booking) => {
    setEditing(booking.booking_id);
    setForm({
      client_id: booking.client_id,
      room_numbers: booking.room_numbers,
      check_in: booking.check_in,
      check_out: booking.check_out,
    });
    setModalOpen(true);
  };

  const submit = async (event) => {
    event.preventDefault();
    if (
      !form.check_in ||
      !form.check_out ||
      form.check_out <= form.check_in ||
      (!editing && (!form.client_id || form.room_numbers.length === 0))
    ) {
      setFeedback({ type: "error", message: "Selecciona cliente y habitacion, y usa una salida posterior a la entrada." });
      return;
    }
    if (!editing && form.check_in < todayISO()) {
      setFeedback({ type: "error", message: "La fecha de entrada no puede estar en el pasado." });
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updateFechasReserva(editing, {
          check_in: form.check_in,
          check_out: form.check_out,
        });
      } else {
        await createReserva({
          client_id: form.client_id,
          room_numbers: form.room_numbers.map(Number),
          check_in: form.check_in,
          check_out: form.check_out,
        });
      }
      setModalOpen(false);
      setFeedback({ type: "success", message: editing ? "Fechas actualizadas." : "Reserva creada correctamente." });
      await loadData();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setSaving(false);
    }
  };

  const remove = async (booking) => {
    if (!window.confirm(`Eliminar la reserva #${booking.booking_id}?`)) return;
    try {
      await deleteReserva(booking.booking_id);
      setFeedback({ type: "success", message: "Reserva eliminada correctamente." });
      await loadData();
    } catch (error) {
      setFeedback({ type: "error", message: error.message || getApiError(error) });
    }
  };

  const updateRoomSelection = (event) => {
    const selected = Array.from(event.target.selectedOptions, (option) => Number(option.value));
    setForm({ ...form, room_numbers: selected });
  };

  const clientName = (id) => {
    const client = clients.find((item) => item.client_id === id);
    return client ? `${client.name} ${client.last_name}` : id;
  };

  const columns = [
    { key: "booking_id", label: "Reserva", render: (booking) => <strong>#{booking.booking_id}</strong> },
    { key: "client_id", label: "Cliente", render: (booking) => clientName(booking.client_id) },
    { key: "room_numbers", label: "Habitaciones", render: (booking) => booking.room_numbers.join(", ") },
    { key: "check_in", label: "Entrada", render: (booking) => formatDate(booking.check_in) },
    { key: "check_out", label: "Salida", render: (booking) => formatDate(booking.check_out) },
    {
      key: "status",
      label: "Estado",
      render: (booking) => {
        const status = getBookingStatus(booking);
        return <span className={`badge ${status.className}`}>{status.label}</span>;
      },
    },
    {
      key: "actions",
      label: "Acciones",
      render: (booking) => (
        <div className="table-actions">
          <button className="button button-small button-secondary" onClick={() => openEdit(booking)}>
            Editar fechas
          </button>
          <button className="button button-small button-danger" onClick={() => remove(booking)}>
            Eliminar
          </button>
        </div>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        eyebrow="Operacion"
        title="Reservas"
        description="Gestiona estancias, clientes y asignacion de habitaciones."
        action={<button className="button button-primary" onClick={openCreate}>+ Nueva reserva</button>}
      />
      <Alert type={feedback.type}>{feedback.message}</Alert>
      <div className="scope-note">
        El estado se calcula con las fechas. Las reservas facturadas no pueden eliminarse.
      </div>
      <article className="panel">
        {loading ? <LoadingState /> : <DataTable columns={columns} rows={bookings} rowKey="booking_id" />}
      </article>

      {modalOpen && (
        <Modal title={editing ? `Editar reserva #${editing}` : "Nueva reserva"} onClose={() => setModalOpen(false)}>
          <form onSubmit={submit} className="form-grid">
            <label>
              Cliente
              <select
                disabled={Boolean(editing)}
                value={form.client_id}
                onChange={(event) => setForm({ ...form, client_id: event.target.value })}
                required
              >
                <option value="">Seleccionar cliente</option>
                {clients.map((client) => (
                  <option key={client.client_id} value={client.client_id}>
                    {client.name} {client.last_name} ({client.client_id})
                  </option>
                ))}
              </select>
            </label>
            <label>
              Habitaciones
              <select
                multiple
                className="multi-select"
                disabled={Boolean(editing)}
                value={form.room_numbers.map(String)}
                onChange={updateRoomSelection}
                required
              >
                {rooms
                  .filter((room) => room.available || form.room_numbers.includes(room.room_number))
                  .map((room) => (
                    <option key={room.room_number} value={room.room_number}>
                      #{room.room_number} - {room.room_type}
                    </option>
                  ))}
              </select>
              {!editing && <small>Usa Ctrl para seleccionar varias.</small>}
            </label>
            <label>
              Fecha de entrada
              <input
                type="date"
                min={editing ? undefined : todayISO()}
                value={form.check_in}
                onChange={(event) => setForm({ ...form, check_in: event.target.value })}
                required
              />
            </label>
            <label>
              Fecha de salida
              <input
                type="date"
                min={form.check_in || todayISO()}
                value={form.check_out}
                onChange={(event) => setForm({ ...form, check_out: event.target.value })}
                required
              />
            </label>
            <div className="form-actions form-full">
              <button type="button" className="button button-ghost" onClick={() => setModalOpen(false)}>Cancelar</button>
              <button className="button button-primary" disabled={saving}>{saving ? "Guardando..." : "Guardar reserva"}</button>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}

export default Reservas;
