# Frontend de HotelManager CR

Interfaz React + Vite conectada exclusivamente al backend FastAPI del proyecto.

## Requisitos

- Node.js 18 o superior.
- Backend activo en `http://localhost:8000`.

## Ejecucion

```bash
cd frontend
npm install
npm run dev
```

La URL del backend se configura en `.env`:

```env
VITE_API_URL=http://localhost:8000
```

## Autenticacion

El inicio de sesion usa `POST /api/v1/auth/login`. El backend entrega un token
Bearer firmado y el frontend conserva el token, el usuario y el rol en
`localStorage`.

Credenciales iniciales configuradas para desarrollo:

```text
Usuario: admin
Contrasena: admin123
```

Los roles disponibles son:

- `ADMIN`: administra catalogos, usuarios, habitaciones y facturas.
- `EMPLOYEE`: consulta datos y gestiona clientes y reservas.

## Datos reales

El frontend no utiliza registros simulados. Si el backend no esta disponible,
las pantallas muestran un error de conexion y conservan una interfaz estable.
Habitaciones, clientes, reservas, facturas, metodos de pago y usuarios se
obtienen de la base de datos mediante Axios.

## Verificacion

```bash
npm run lint
npm run build
```
