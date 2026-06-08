const SESSION_KEY = "hotel_user";

export const getSession = () => {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY));
  } catch {
    return null;
  }
};

export const saveSession = (user) => {
  const { access_token, ...session } = user;
  localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  if (access_token) localStorage.setItem("hotel_token", access_token);
  localStorage.removeItem("hotel_demo_mode");
};

export const clearSession = () => {
  localStorage.removeItem(SESSION_KEY);
  localStorage.removeItem("hotel_token");
  localStorage.removeItem("hotel_demo_mode");
};

export const isAdminRole = (role) => String(role).toUpperCase() === "ADMIN";

export const isAdmin = () => isAdminRole(getSession()?.role);
