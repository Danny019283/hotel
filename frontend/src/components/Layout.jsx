import { useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { clearSession, getSession } from "../utils/auth";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function Layout() {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();
  const user = getSession();

  const logout = () => {
    clearSession();
    navigate("/login", { replace: true });
  };

  return (
    <div className="app-shell">
      <Sidebar user={user} open={menuOpen} onClose={() => setMenuOpen(false)} />
      <div className="main-shell">
        <Navbar user={user} onMenu={() => setMenuOpen(true)} onLogout={logout} />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default Layout;
