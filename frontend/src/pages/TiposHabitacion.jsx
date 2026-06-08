import { useEffect, useState } from "react";
import { getApiError } from "../api/axiosConfig";
import {
  createTipoHabitacion,
  deleteTipoHabitacion,
  getTiposHabitacion,
  updateEstadoTipoHabitacion,
  updateTipoHabitacion,
} from "../api/tiposHabitacion.api";
import DataTable from "../components/DataTable";
import { Alert, LoadingState } from "../components/Feedback";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import { formatCurrency } from "../utils/formatters";

const initialForm = {
  name: "",
  description: "",
  capacity: "",
  base_price: "",
  active: true,
};

function TiposHabitacion() {
  const [roomTypes, setRoomTypes] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState({ type: "", message: "" });

  const loadRoomTypes = async () => {
    try {
      setLoading(true);
      setRoomTypes(await getTiposHabitacion());
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRoomTypes();
  }, []);

  const openCreate = () => {
    setEditing(null);
    setForm(initialForm);
    setModalOpen(true);
  };

  const openEdit = (roomType) => {
    setEditing(roomType.room_type_id);
    setForm({
      name: roomType.name,
      description: roomType.description,
      capacity: String(roomType.capacity),
      base_price: String(roomType.base_price),
      active: roomType.active,
    });
    setModalOpen(true);
  };

  const submit = async (event) => {
    event.preventDefault();
    if (!form.name.trim() || !form.description.trim() || Number(form.capacity) <= 0 || Number(form.base_price) <= 0) {
      setFeedback({ type: "error", message: "Completa todos los campos con valores validos." });
      return;
    }

    try {
      setSaving(true);
      const payload = {
        name: form.name.trim(),
        description: form.description.trim(),
        capacity: Number(form.capacity),
        base_price: Number(form.base_price),
      };

      if (editing) {
        await updateTipoHabitacion(editing, payload);
      } else {
        await createTipoHabitacion({ ...payload, active: true });
      }
      setModalOpen(false);
      setFeedback({ type: "success", message: editing ? "Tipo actualizado." : "Tipo creado." });
      await loadRoomTypes();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setSaving(false);
    }
  };

  const toggleStatus = async (roomType) => {
    try {
      await updateEstadoTipoHabitacion(roomType.room_type_id, !roomType.active);
      setFeedback({ type: "success", message: "Estado actualizado correctamente." });
      await loadRoomTypes();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    }
  };

  const remove = async (roomType) => {
    if (!window.confirm(`Eliminar el tipo ${roomType.name}?`)) return;
    try {
      await deleteTipoHabitacion(roomType.room_type_id);
      setFeedback({ type: "success", message: "Tipo eliminado correctamente." });
      await loadRoomTypes();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    }
  };

  const columns = [
    { key: "name", label: "Nombre", render: (roomType) => <strong>{roomType.name}</strong> },
    { key: "description", label: "Descripcion" },
    { key: "capacity", label: "Capacidad" },
    { key: "base_price", label: "Precio base", render: (roomType) => formatCurrency(roomType.base_price) },
    {
      key: "active",
      label: "Estado",
      render: (roomType) => (
        <span className={`badge ${roomType.active ? "badge-success" : "badge-muted"}`}>
          {roomType.active ? "Activo" : "Inactivo"}
        </span>
      ),
    },
    {
      key: "actions",
      label: "Acciones",
      render: (roomType) => (
        <div className="table-actions">
          <button className="button button-small button-secondary" onClick={() => openEdit(roomType)}>Editar</button>
          <button className="button button-small button-ghost" onClick={() => toggleStatus(roomType)}>
            {roomType.active ? "Desactivar" : "Activar"}
          </button>
          {roomType.can_delete && (
            <button className="button button-small button-danger" onClick={() => remove(roomType)}>Eliminar</button>
          )}
        </div>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        eyebrow="Catalogo"
        title="Tipos de habitacion"
        description="Administra capacidades y tarifas base que usan las habitaciones y reservas."
        action={<button className="button button-primary" onClick={openCreate}>+ Nuevo tipo</button>}
      />
      <Alert type={feedback.type}>{feedback.message}</Alert>
      <article className="panel">
        {loading ? <LoadingState /> : <DataTable columns={columns} rows={roomTypes} rowKey="room_type_id" />}
      </article>

      {modalOpen && (
        <Modal title={editing ? "Editar tipo" : "Nuevo tipo"} onClose={() => setModalOpen(false)}>
          <form onSubmit={submit} className="form-grid">
            <label>
              Nombre
              <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
            </label>
            <label>
              Capacidad
              <input
                type="number"
                min="1"
                value={form.capacity}
                onChange={(event) => setForm({ ...form, capacity: event.target.value })}
                required
              />
            </label>
            <label className="form-full">
              Descripcion
              <input value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} required />
            </label>
            <label className="form-full">
              Precio base
              <input
                type="number"
                min="0.01"
                step="0.01"
                value={form.base_price}
                onChange={(event) => setForm({ ...form, base_price: event.target.value })}
                required
              />
            </label>
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

export default TiposHabitacion;
