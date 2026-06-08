import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { login } from "../api/auth.api";
import { getApiError } from "../api/axiosConfig";
import { Alert } from "../components/Feedback";
import { getSession, saveSession } from "../utils/auth";

function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (getSession()) return <Navigate to="/dashboard" replace />;

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (form.username.trim().length < 3 || form.password.length < 8) {
      setError("Ingresa un usuario valido y una contrasena de al menos 8 caracteres.");
      return;
    }

    try {
      setLoading(true);
      const data = await login({
        username: form.username.trim(),
        password: form.password,
      });
      saveSession(data);
      navigate("/dashboard", { replace: true });
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-page">
      <section className="login-visual">
        <div className="login-overlay">
          <div className="brand brand-login">
            <div className="brand-mark">HM</div>
            <div>
              <strong>HotelManager CR</strong>
              <span>Gestion Hotelera</span>
            </div>
          </div>
          <div className="login-quote">
            <p className="eyebrow">Hospitalidad con precision</p>
            <h1>Una operacion impecable empieza aqui.</h1>
            <p>
              Habitaciones, reservas, huespedes y facturacion en un solo espacio de trabajo.
            </p>
          </div>
          <div className="login-features">
            <span>Control operativo</span>
            <span>Reportes en vivo</span>
            <span>Acceso por roles</span>
          </div>
        </div>
      </section>

      <section className="login-panel">
        <div className="login-form-wrap">
          <p className="eyebrow">Bienvenido de nuevo</p>
          <h2>Iniciar sesion</h2>
          <p className="muted">Ingresa al panel administrativo del hotel.</p>

          <div className="demo-access-card">
            <span>Acceso inicial del entorno local</span>
            <strong>admin / admin123</strong>
            <small>Credenciales reales creadas por el backend al iniciar.</small>
          </div>

          <Alert>{error}</Alert>

          <form onSubmit={handleSubmit} className="form-stack">
            <label>
              Usuario
              <input
                autoFocus
                autoComplete="username"
                placeholder="Ej. admin01"
                value={form.username}
                onChange={(event) => setForm({ ...form, username: event.target.value })}
              />
            </label>
            <label>
              Contrasena
              <input
                type="password"
                autoComplete="current-password"
                placeholder="Minimo 8 caracteres"
                value={form.password}
                onChange={(event) => setForm({ ...form, password: event.target.value })}
              />
            </label>
            <button className="button button-primary button-block" disabled={loading}>
              {loading ? "Verificando..." : "Ingresar al sistema"}
            </button>
          </form>
          <p className="login-note">
            La sesion utiliza un token firmado emitido por el backend.
          </p>
        </div>
      </section>
    </main>
  );
}

export default Login;
