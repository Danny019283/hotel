import { useEffect, useState } from "react";
import {
  createCliente,
  deleteCliente,
  getClientes,
  updateCliente,
} from "../api/clientes.api";
import { getApiError } from "../api/axiosConfig";
import DataTable from "../components/DataTable";
import { Alert, LoadingState } from "../components/Feedback";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import { getSession, isAdminRole } from "../utils/auth";

const initialForm = { client_id: "", name: "", last_name: "", phone: "", email: "" };
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function Clientes() {
  const isAdmin = isAdminRole(getSession().role);
  const [clients, setClients] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState({ type: "", message: "" });

  const loadClients = async () => {
    try {
      setLoading(true);
      setClients(await getClientes());
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadClients();
  }, []);

  const openCreate = () => {
    setEditing(null);
    setForm(initialForm);
    setModalOpen(true);
  };

  const openEdit = (client) => {
    setEditing(client.client_id);
    setForm({ ...client, phone: String(client.phone) });
    setModalOpen(true);
  };

  const submit = async (event) => {
    event.preventDefault();
    if (
      !form.client_id.trim() ||
      !form.name.trim() ||
      !form.last_name.trim() ||
      !/^\d{8}$/.test(form.phone) ||
      !emailPattern.test(form.email)
    ) {
      setFeedback({ type: "error", message: "Revisa los campos. El telefono debe tener 8 digitos y el correo debe ser valido." });
      return;
    }

    const payload = {
      name: form.name.trim(),
      last_name: form.last_name.trim(),
      phone: Number(form.phone),
      email: form.email.trim(),
    };

    try {
      setSaving(true);
      if (editing) {
        await updateCliente(editing, payload);
      } else {
        await createCliente({ client_id: form.client_id.trim(), ...payload });
      }
      setModalOpen(false);
      setFeedback({ type: "success", message: editing ? "Cliente actualizado." : "Cliente registrado." });
      await loadClients();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setSaving(false);
    }
  };

  const remove = async (client) => {
    if (!window.confirm(`Eliminar al cliente ${client.name} ${client.last_name}?`)) return;
    try {
      await deleteCliente(client.client_id);
      setFeedback({ type: "success", message: "Cliente eliminado." });
      await loadClients();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    }
  };

  const columns = [
    { key: "client_id", label: "Identificacion" },
    { key: "name", label: "Cliente", render: (client) => <strong>{client.name} {client.last_name}</strong> },
    { key: "phone", label: "Telefono" },
    { key: "email", label: "Correo" },
    {
      key: "actions",
      label: "Acciones",
      render: (client) => (
        <div className="table-actions">
          <button className="button button-small button-secondary" onClick={() => openEdit(client)}>Editar</button>
          {isAdmin && <button className="button button-small button-danger" onClick={() => remove(client)}>Eliminar</button>}
        </div>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        eyebrow="Huespedes"
        title="Clientes"
        description="Registro y seguimiento de las personas atendidas por el hotel."
        action={<button className="button button-primary" onClick={openCreate}>+ Nuevo cliente</button>}
      />
      <Alert type={feedback.type}>{feedback.message}</Alert>
      <article className="panel">
        {loading ? <LoadingState /> : <DataTable columns={columns} rows={clients} rowKey="client_id" />}
      </article>

      {modalOpen && (
        <Modal title={editing ? "Editar cliente" : "Nuevo cliente"} onClose={() => setModalOpen(false)}>
          <form onSubmit={submit} className="form-grid">
            <label>
              Identificacion
              <input
                maxLength="10"
                disabled={Boolean(editing)}
                value={form.client_id}
                onChange={(event) => setForm({ ...form, client_id: event.target.value })}
                required
              />
            </label>
            <label>
              Nombre
              <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
            </label>
            <label>
              Apellido
              <input value={form.last_name} onChange={(event) => setForm({ ...form, last_name: event.target.value })} required />
            </label>
            <label>
              Telefono
              <input
                inputMode="numeric"
                maxLength="8"
                placeholder="88887777"
                value={form.phone}
                onChange={(event) => setForm({ ...form, phone: event.target.value.replace(/\D/g, "") })}
                required
              />
            </label>
            <label className="form-full">
              Correo electronico
              <input type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required />
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

export default Clientes;
