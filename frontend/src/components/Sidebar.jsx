import { NavLink } from "react-router-dom";
import { isAdminRole } from "../utils/auth";

const links = [
  { to: "/dashboard", icon: "⌂", label: "Dashboard" },
  { to: "/habitaciones", icon: "▦", label: "Habitaciones" },
  { to: "/reservas", icon: "▤", label: "Reservas" },
  { to: "/clientes", icon: "◎", label: "Clientes" },
  { to: "/pagos", icon: "$", label: "Pagos" },
  { to: "/reportes", icon: "◫", label: "Reportes" },
  { to: "/usuarios", icon: "♙", label: "Usuarios", adminOnly: true },
];

function Sidebar({ user, open, onClose }) {
  return (
    <>
      <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-mark">HM</div>
          <div>
            <strong>HotelManager CR</strong>
            <span>Gestion Hotelera</span>
          </div>
        </div>
        <nav>
          {links
            .filter((link) => !link.adminOnly || isAdminRole(user.role))
            .map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                onClick={onClose}
                className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
              >
                <span>{link.icon}</span>
                {link.label}
              </NavLink>
            ))}
        </nav>
        <div className="sidebar-footer">
          <span className="status-dot" />
          API configurada
          <small>{import.meta.env.VITE_API_URL || "http://localhost:8000"}</small>
        </div>
      </aside>
      {open && <button className="sidebar-overlay" onClick={onClose} aria-label="Cerrar menu" />}
    </>
  );
}

export default Sidebar;
