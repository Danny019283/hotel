import { useEffect, useState } from "react";
import { getApiError } from "../api/axiosConfig";
import {
  deleteUsuario,
  getUsuarios,
  registerUser,
  updateUsuario,
} from "../api/usuarios.api";
import DataTable from "../components/DataTable";
import { Alert, LoadingState } from "../components/Feedback";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import { getSession } from "../utils/auth";

const initialForm = {
  username: "",
  password: "",
  role: "EMPLOYEE",
};

function Usuarios() {
  const session = getSession();
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState({ type: "", message: "" });

  const loadUsers = async () => {
    try {
      setLoading(true);
      setUsers(await getUsuarios());
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const openCreate = () => {
    setEditing(null);
    setForm(initialForm);
    setModalOpen(true);
  };

  const openEdit = (user) => {
    setEditing(user.username);
    setForm({ username: user.username, password: "", role: user.role });
    setModalOpen(true);
  };

  const submit = async (event) => {
    event.preventDefault();
    if (form.username.trim().length < 3 || (!editing && form.password.length < 8)) {
      setFeedback({
        type: "error",
        message: "El usuario debe tener al menos 3 caracteres y la contrasena al menos 8.",
      });
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updateUsuario(editing, { role: form.role });
      } else {
        await registerUser({
          username: form.username.trim(),
          password: form.password,
          role: form.role,
        });
      }
      setModalOpen(false);
      setFeedback({ type: "success", message: editing ? "Rol actualizado." : "Usuario registrado." });
      await loadUsers();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    } finally {
      setSaving(false);
    }
  };

  const remove = async (user) => {
    if (user.username === session.username) {
      setFeedback({ type: "error", message: "No puedes eliminar tu propia sesion." });
      return;
    }
    if (!window.confirm(`Eliminar al usuario ${user.username}?`)) return;
    try {
      await deleteUsuario(user.username);
      setFeedback({ type: "success", message: "Usuario eliminado." });
      await loadUsers();
    } catch (error) {
      setFeedback({ type: "error", message: getApiError(error) });
    }
  };

  const columns = [
    { key: "username", label: "Nombre de usuario", render: (user) => <strong>{user.username}</strong> },
    {
      key: "role",
      label: "Rol",
      render: (user) => (
        <span className={`badge ${user.role === "ADMIN" ? "badge-gold" : "badge-muted"}`}>
          {user.role === "ADMIN" ? "Administrador" : "Empleado"}
        </span>
      ),
    },
    {
      key: "actions",
      label: "Acciones",
      render: (user) => (
        <div className="table-actions">
          <button className="button button-small button-secondary" onClick={() => openEdit(user)}>
            Editar rol
          </button>
          <button className="button button-small button-danger" onClick={() => remove(user)}>
            Eliminar
          </button>
        </div>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        eyebrow="Administracion"
        title="Usuarios"
        description="Gestiona cuentas y roles persistidos en la base de datos."
        action={<button className="button button-primary" onClick={openCreate}>+ Nuevo usuario</button>}
      />
      <Alert type={feedback.type}>{feedback.message}</Alert>
      <div className="scope-note">
        Solo administradores pueden acceder. El backend impide eliminar al ultimo administrador.
      </div>
      <article className="panel">
        {loading ? <LoadingState /> : <DataTable columns={columns} rows={users} rowKey="username" />}
      </article>

      {modalOpen && (
        <Modal title={editing ? `Editar rol de ${editing}` : "Nuevo usuario"} onClose={() => setModalOpen(false)}>
          <form onSubmit={submit} className="form-grid">
            <label>
              Nombre de usuario
              <input
                value={form.username}
                onChange={(event) => setForm({ ...form, username: event.target.value })}
                disabled={Boolean(editing)}
                minLength="3"
                required
              />
            </label>
            {!editing && (
              <label>
                Contrasena
                <input
                  type="password"
                  value={form.password}
                  onChange={(event) => setForm({ ...form, password: event.target.value })}
                  minLength="8"
                  required
                />
              </label>
            )}
            <label className="form-full">
              Rol
              <select value={form.role} onChange={(event) => setForm({ ...form, role: event.target.value })}>
                <option value="EMPLOYEE">Empleado</option>
                <option value="ADMIN">Administrador</option>
              </select>
            </label>
            <div className="form-actions form-full">
              <button type="button" className="button button-ghost" onClick={() => setModalOpen(false)}>Cancelar</button>
              <button className="button button-primary" disabled={saving}>{saving ? "Guardando..." : "Guardar usuario"}</button>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}

export default Usuarios;
