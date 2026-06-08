import { Navigate, Outlet } from "react-router-dom";
import { getSession, isAdminRole } from "../utils/auth";

function ProtectedRoute({ allowedRoles }) {
  const user = getSession();

  if (!user) return <Navigate to="/login" replace />;

  const hasAllowedRole =
    !allowedRoles ||
    allowedRoles.some((role) =>
      role === "ADMIN" ? isAdminRole(user.role) : role === user.role,
    );

  if (!hasAllowedRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;
