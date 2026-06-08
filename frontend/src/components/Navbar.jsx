import { isAdminRole } from "../utils/auth";

function Navbar({ user, onMenu, onLogout }) {
  return (
    <header className="navbar">
      <button className="icon-button mobile-menu" onClick={onMenu} aria-label="Abrir menu">
        ☰
      </button>
      <div>
        <p className="eyebrow">Panel operativo</p>
        <h2>Gestion hotelera</h2>
      </div>
      <div className="user-menu">
        <div className="avatar">{user.username.slice(0, 2).toUpperCase()}</div>
        <div className="user-copy">
          <strong>{user.username}</strong>
          <span>{isAdminRole(user.role) ? "Administrador" : "Empleado"}</span>
        </div>
        <button className="button button-ghost" onClick={onLogout}>
          Salir
        </button>
      </div>
    </header>
  );
}

export default Navbar;
