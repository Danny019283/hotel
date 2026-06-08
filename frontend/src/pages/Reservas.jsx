import { useEffect, useState } from "react";
import { getApiError } from "../api/axiosConfig";
import { getClientes } from "../api/clientes.api";
import { getHabitaciones } from "../api/habitaciones.api";
import {
  createReserva,
  deleteReserva,
  getFechasOcupadasPorHabitacion,
  getReservas,
  updateFechasReserva,
} from "../api/reservas.api";
import DataTable from "../components/DataTable";
import { Alert, LoadingState } from "../components/Feedback";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import { formatCurrency, formatDate, todayISO } from "../utils/formatters";

const initialForm = {
  client_id: "",
  room_numbers: [],
  check_in: "",
  check_out: "",
};

const rangesOverlap = (checkIn, checkOut, range) =>
  Boolean(checkIn && checkOut) && checkIn < range.check_out && checkOut > range.check_in;

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
  const [occupiedRanges, setOccupiedRanges] = useState({});

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

  useEffect(() => {
    if (!modalOpen || editing || form.room_numbers.length === 0) {
      setOccupiedRanges({});
      return;
    }

    const loadOccupiedRanges = async () => {
      try {
        const entries = await Promise.all(
          form.room_numbers.map(async (roomNumber) => [roomNumber, await getFechasOcupadasPorHabitacion(roomNumber)]),
        );
        setOccupiedRanges(Object.fromEntries(entries));
      } catch (error) {
        setFeedback({ type: "error", message: getApiError(error) });
      }
    };

    loadOccupiedRanges();
  }, [modalOpen, editing, form.room_numbers]);

  const selectedOverlaps = Object.values(occupiedRanges)
    .flat()
    .some((range) => rangesOverlap(form.check_in, form.check_out, range));

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
    if (!editing && selectedOverlaps) {
      setFeedback({ type: "error", message: "Una o mas habitaciones seleccionadas ya estan ocupadas en ese rango." });
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

  const toggleRoomSelection = (roomNumber) => {
    const selected = form.room_numbers.includes(roomNumber)
      ? form.room_numbers.filter((value) => value !== roomNumber)
      : [...form.room_numbers, roomNumber];
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
          {booking.can_edit_dates && (
            <button className="button button-small button-secondary" onClick={() => openEdit(booking)}>
              Editar fechas
            </button>
          )}
          {booking.can_delete && (
            <button className="button button-small button-danger" onClick={() => remove(booking)}>
              Eliminar
            </button>
          )}
          {!booking.can_edit_dates && !booking.can_delete && <span className="muted">Sin acciones</span>}
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
              <div className={`room-picker ${editing ? "room-picker-disabled" : ""}`}>
                {rooms.map((room) => {
                  const selected = form.room_numbers.includes(room.room_number);
                  return (
                    <button
                      key={room.room_number}
                      type="button"
                      className={`room-chip ${selected ? "room-chip-selected" : ""}`}
                      onClick={() => toggleRoomSelection(room.room_number)}
                      disabled={Boolean(editing)}
                    >
                      <strong>#{room.room_number}</strong>
                      <span>{room.room_type_name}</span>
                      <small>Capacidad {room.capacity} · {formatCurrency(room.base_price)}</small>
                    </button>
                  );
                })}
              </div>
              {!editing && <small>Selecciona una o varias habitaciones para la misma estancia.</small>}
            </label>
            <label>
              Fecha de entrada
              <input
                type="date"
                min={editing ? undefined : todayISO()}
                className={!editing && selectedOverlaps ? "input-error" : ""}
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
                className={!editing && selectedOverlaps ? "input-error" : ""}
                value={form.check_out}
                onChange={(event) => setForm({ ...form, check_out: event.target.value })}
                required
              />
            </label>
            {!editing && form.room_numbers.length > 0 && (
              <div className="form-full occupancy-panel">
                <div className="occupancy-header">
                  <strong>Fechas ocupadas</strong>
                </div>
                <div className="occupancy-grid">
                  {form.room_numbers.map((roomNumber) => {
                    const ranges = occupiedRanges[roomNumber] || [];
                    return (
                      <div key={roomNumber} className="occupancy-card">
                        <h4>Habitacion #{roomNumber}</h4>
                        {ranges.length === 0 ? (
                          <p className="occupancy-empty">Sin reservas registradas.</p>
                        ) : (
                          <div className="occupancy-ranges">
                            {ranges.map((range) => (
                              <span
                                key={`${roomNumber}-${range.booking_id}-${range.check_in}`}
                                className={`occupancy-range ${rangesOverlap(form.check_in, form.check_out, range) ? "occupancy-range-conflict" : ""}`}
                              >
                                {formatDate(range.check_in)} a {formatDate(range.check_out)}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
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
