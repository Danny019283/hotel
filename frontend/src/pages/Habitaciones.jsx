import { useEffect, useState } from "react";
import {
  createHabitacion,
  deleteHabitacion,
  getHabitaciones,
  updateEstadoHabitacion,
  updateHabitacion,
} from "../api/habitaciones.api";
import { getApiError } from "../api/axiosConfig";
import { getTiposHabitacion } from "../api/tiposHabitacion.api";
import DataTable from "../components/DataTable";
import { Alert, LoadingState } from "../components/Feedback";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import { getSession, isAdminRole } from "../utils/auth";
import { formatCurrency } from "../utils/formatters";

const initialForm = {
  room_number: "",
  room_type_id: "",
  available: true,
};

function Habitaciones() {
  const user = getSession();
  const canManage = isAdminRole(user.role);
  const [rooms, setRooms] = useState([]);
  const [roomTypes, setRoomTypes] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState({ type: "", message: "" });

  const loadRooms = async () => {
    try {
      setLoading(true);
      const [roomData, roomTypeData] = await Promise.all([getHabitaciones(), getTiposHabitacion()]);
      setRooms(roomData);
      setRoomTypes(roomTypeData);
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRooms();
  }, []);

  const openCreate = () => {
    setEditing(null);
    setForm(initialForm);
    setModalOpen(true);
  };

  const openEdit = (room) => {
    setEditing(room.room_number);
    setForm({
      ...room,
      room_number: String(room.room_number),
      room_type_id: String(room.room_type_id),
    });
    setModalOpen(true);
  };

  const submit = async (event) => {
    event.preventDefault();
    setFeedback({ type: "", message: "" });
    if (Number(form.room_type_id) <= 0 || Number(form.room_number) <= 0) {
      setFeedback({ type: "error", message: "Completa los campos y selecciona un tipo de habitacion valido." });
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updateHabitacion(editing, {
          room_type_id: Number(form.room_type_id),
        });
      } else {
        await createHabitacion({
          room_number: Number(form.room_number),
          room_type_id: Number(form.room_type_id),
          available: true,
        });
      }
      setModalOpen(false);
      setFeedback({ type: "success", message: editing ? "Habitacion actualizada." : "Habitacion creada." });
      await loadRooms();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setSaving(false);
    }
  };

  const toggleStatus = async (room) => {
    try {
      await updateEstadoHabitacion(room.room_number, !room.available);
      setFeedback({ type: "success", message: "Estado actualizado correctamente." });
      await loadRooms();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    }
  };

  const remove = async (room) => {
    if (!window.confirm(`Eliminar la habitacion ${room.room_number}?`)) return;
    try {
      await deleteHabitacion(room.room_number);
      setFeedback({ type: "success", message: "Habitacion eliminada correctamente." });
      await loadRooms();
    } catch (error) {
      setFeedback({ type: "error", message: error.message || getApiError(error) });
    }
  };

  const columns = [
    { key: "room_number", label: "Numero" },
    { key: "room_type_name", label: "Tipo" },
    { key: "capacity", label: "Capacidad" },
    { key: "base_price", label: "Precio / noche", render: (room) => formatCurrency(room.base_price) },
    {
      key: "room_type_active",
      label: "Tipo activo",
      render: (room) => (
        <span className={`badge ${room.room_type_active ? "badge-success" : "badge-muted"}`}>
          {room.room_type_active ? "Activo" : "Inactivo"}
        </span>
      ),
    },
    {
      key: "available",
      label: "Habitacion",
      render: (room) => (
        <span className={`badge ${room.available ? "badge-success" : "badge-muted"}`}>
          {room.available ? "Disponible" : "No disponible"}
        </span>
      ),
    },
    {
      key: "actions",
      label: "Acciones",
      render: (room) =>
        canManage ? (
          <div className="table-actions">
            <button className="button button-small button-secondary" onClick={() => openEdit(room)}>Editar</button>
            <button className="button button-small button-ghost" onClick={() => toggleStatus(room)}>
              {room.available ? "Bloquear" : "Habilitar"}
            </button>
            <button className="button button-small button-danger" onClick={() => remove(room)}>
              Eliminar
            </button>
          </div>
        ) : (
          <span className="muted">Solo lectura</span>
        ),
    },
  ];

  return (
    <>
      <PageHeader
        eyebrow="Inventario"
        title="Habitaciones"
        description="Administra habitaciones enlazadas a tipos, tarifas y capacidades del hotel."
        action={canManage && <button className="button button-primary" onClick={openCreate}>+ Nueva habitacion</button>}
      />
      <Alert type={feedback.type}>{feedback.message}</Alert>
      <div className="scope-note">
        Los cambios se guardan en SQL Server. Una habitacion relacionada con reservas puede no ser eliminable.
      </div>
      <article className="panel">
        {loading ? <LoadingState /> : <DataTable columns={columns} rows={rooms} rowKey="room_number" />}
      </article>

      {modalOpen && (
        <Modal title={editing ? `Editar habitacion ${editing}` : "Nueva habitacion"} onClose={() => setModalOpen(false)}>
          <form onSubmit={submit} className="form-grid">
            <label>
              Numero de habitacion
              <input
                type="number"
                min="1"
                disabled={Boolean(editing)}
                value={form.room_number}
                onChange={(event) => setForm({ ...form, room_number: event.target.value })}
                required
              />
            </label>
            <label>
              Tipo
              <select
                value={form.room_type_id}
                onChange={(event) => setForm({ ...form, room_type_id: event.target.value })}
                required
              >
                <option value="">Seleccione un tipo</option>
                {roomTypes
                  .filter((type) => type.active || String(type.room_type_id) === form.room_type_id)
                  .map((type) => (
                  <option key={type.room_type_id} value={type.room_type_id}>
                    {type.name} - Capacidad {type.capacity} - {formatCurrency(type.base_price)}
                  </option>
                  ))}
              </select>
            </label>
            {!editing && (
              <p className="form-hint form-full">
                Las habitaciones nuevas usan la tarifa y capacidad del tipo seleccionado.
              </p>
            )}
            <div className="form-actions form-full">
              <button type="button" className="button button-ghost" onClick={() => setModalOpen(false)}>Cancelar</button>
              <button className="button button-primary" disabled={saving}>{saving ? "Guardando..." : "Guardar"}</button>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}

export default Habitaciones;
