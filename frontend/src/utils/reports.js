const monthFormatter = new Intl.DateTimeFormat("es-CR", {
  month: "short",
  year: "2-digit",
  timeZone: "UTC",
});

export const buildMonthlyBookings = (bookings) => {
  const grouped = bookings.reduce((accumulator, booking) => {
    const date = new Date(`${booking.check_in}T00:00:00Z`);
    const key = `${date.getUTCFullYear()}-${String(date.getUTCMonth() + 1).padStart(2, "0")}`;
    accumulator[key] = (accumulator[key] || 0) + 1;
    return accumulator;
  }, {});

  return Object.entries(grouped)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, reservas]) => ({
      mes: monthFormatter.format(new Date(`${key}-01T00:00:00Z`)),
      reservas,
    }));
};

export const buildRoomStatus = (bookings, rooms, today = new Date().toISOString().slice(0, 10)) => {
  const occupiedRooms = new Set();

  bookings.forEach((booking) => {
    if (booking.check_in <= today && booking.check_out > today) {
      booking.room_numbers.forEach((roomNumber) => occupiedRooms.add(roomNumber));
    }
  });

  return [
    { name: "Disponibles hoy", value: rooms.length - occupiedRooms.size },
    { name: "Ocupadas hoy", value: occupiedRooms.size },
  ];
};

export const buildBookingsByRoomType = (bookings, rooms) => {
  const roomTypes = new Map(rooms.map((room) => [room.room_number, room.room_type_name]));
  const grouped = {};

  bookings.forEach((booking) => {
    booking.room_numbers.forEach((number) => {
      const type = roomTypes.get(number) || "Sin tipo";
      grouped[type] = (grouped[type] || 0) + 1;
    });
  });

  return Object.entries(grouped).map(([tipo, reservas]) => ({ tipo, reservas }));
};

export const buildMonthlyRevenue = (payments, bookings) => {
  const bookingDates = new Map(
    bookings.map((booking) => [booking.booking_id, booking.check_in]),
  );
  const grouped = {};

  payments.forEach((payment) => {
    const dateValue = payment.date || bookingDates.get(payment.booking_id);
    if (!dateValue) return;
    const date = new Date(`${dateValue}T00:00:00Z`);
    const key = `${date.getUTCFullYear()}-${String(date.getUTCMonth() + 1).padStart(2, "0")}`;
    grouped[key] = (grouped[key] || 0) + Number(payment.total);
  });

  return Object.entries(grouped)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, ingresos]) => ({
      mes: monthFormatter.format(new Date(`${key}-01T00:00:00Z`)),
      ingresos,
    }));
};
