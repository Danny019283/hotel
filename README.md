# HotelManager CR

Sistema web universitario para la administracion de un hotel. Integra:

- Frontend con React y Vite.
- Backend con FastAPI.
- Base de datos SQL Server.
- Autenticacion con token.
- Roles `ADMIN` y `EMPLOYEE`.
- CRUD, reportes y graficos con datos reales.

## Que se debe compartir

Para probar el sistema en otra computadora con Docker Compose se debe entregar:

- La carpeta completa del proyecto.
- `docker-compose.yml`.
- `server/.env.example`.
- Este archivo `README.md`.
- Un script SQL o respaldo de la base, solamente si se necesitan exactamente
  los mismos clientes, habitaciones, reservas y facturas.

No se recomienda publicar `server/.env`, porque contiene contrasenas y claves
privadas. Cada integrante debe crear su propio archivo a partir de
`server/.env.example`.

`frontend/.env` no es obligatorio para Docker Compose en este proyecto, porque
el frontend ya usa `http://localhost:8000` por defecto. Solo hace falta si se
desea cambiar la URL de la API.

## Programas necesarios

Para levantar todo con Docker Compose, cada integrante debe instalar:

1. Docker Desktop.
2. Git.

Node.js, Python, `uv` y Microsoft ODBC Driver 18 for SQL Server solo se
necesitan para ejecutar el frontend o el backend fuera de Docker.

Antes de continuar, Docker Desktop debe estar abierto y funcionando.

## Estructura esperada

La terminal debe estar ubicada en la carpeta que contiene estos elementos:

```text
hotel-main/
|-- docker-compose.yml
|-- README.md
|-- frontend/
`-- server/
```

En este equipo, por ejemplo, la ruta es:

```text
C:\Users\morer\Downloads\hotel-main\hotel-main
```

## Configurar el backend

Desde la raiz del proyecto, crear `server/.env`:

```powershell
Copy-Item server/.env.example server/.env
```

Abrir el archivo y configurar valores como estos:

```env
DB_SERVER=localhost,1433
DB_NAME=hotel
DB_USERNAME=SA
DB_PASSWORD=HotelManagerCR_2026!
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_TRUST_SERVER_CERTIFICATE=yes
DB_ECHO=false
DB_RESET_ON_START=false
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
AUTH_SECRET=una_clave_privada_larga_para_el_equipo
AUTH_TOKEN_TTL_SECONDS=28800
INITIAL_ADMIN_USERNAME=admin
INITIAL_ADMIN_PASSWORD=admin123
```

La contraseña de `DB_PASSWORD` debe ser fuerte y es la misma que Docker usara
para SQL Server.

## Configurar el frontend

Si se desea definir explícitamente la URL del backend, el archivo
`frontend/.env` puede contener:

```env
VITE_API_URL=http://localhost:8000
```

Si no existe `frontend/.env`, el frontend usa `http://localhost:8000`
automáticamente.

## Iniciar el sistema con Docker

Desde la carpeta que contiene `docker-compose.yml`:

```powershell
docker compose --env-file server/.env up --build -d
docker compose --env-file server/.env ps
```

El resultado debe mostrar estos contenedores:

- `hotel-sqlserver` en estado `healthy`.
- `hotel-server` ejecutandose en `http://localhost:8000`.
- `hotel-frontend` ejecutandose en `http://localhost:5173`.

Docker crea automáticamente una base llamada `hotel`. Los datos se guardan en
un volumen persistente, por lo que sobreviven al reinicio del contenedor.

La API queda disponible en:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

El frontend queda disponible en:

- App: `http://localhost:5173`

## Iniciar solo el backend en local

En la primera terminal:

```powershell
cd server
uv sync
uv run python -m uvicorn main:app --reload
```

La API quedara disponible en:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

El backend crea las tablas y los datos iniciales al arrancar.

## Iniciar solo el frontend en local

Abrir una segunda terminal y ejecutar:

```powershell
cd C:\ruta\del\proyecto\hotel-main\frontend
npm install
npm run dev
```

Abrir en el navegador:

```text
http://localhost:5173
```

## Credenciales iniciales

```text
Usuario: admin
Contrasena: admin123
Rol: ADMIN
```

El administrador puede crear usuarios con rol `EMPLOYEE` desde el modulo de
usuarios.

## Datos iniciales

En una base nueva, el backend registra automáticamente:

- El usuario administrador.
- Efectivo.
- Tarjeta.
- Transferencia.

Los clientes, habitaciones, reservas y facturas se crean desde la interfaz.

## Compartir los mismos registros

Compartir solamente el código crea una base nueva y vacía para cada
integrante. Para entregar también los mismos registros existen dos opciones:

1. Ejecutar en cada computadora un script SQL con los datos de prueba.
2. Restaurar un respaldo `.bak` de SQL Server.

Para este proyecto se recomienda un script SQL reproducible, porque también
forma parte de los entregables solicitados para Bases de Datos.

## Detener el sistema

Si el sistema se levantó con Docker Compose, detener todo sin borrar datos:

```powershell
docker compose --env-file server/.env down
```

Si el backend y el frontend se levantaron manualmente, se detienen presionando
`Ctrl + C` en sus terminales.

No ejecutar lo siguiente si se desean conservar los datos:

```powershell
docker compose --env-file server/.env down -v
```

La opcion `-v` elimina el volumen de SQL Server.

## Errores comunes

### No encuentra `server/.env`

La terminal está ubicada una carpeta arriba. Entrar primero a la carpeta que
contiene `docker-compose.yml`:

```powershell
cd .\hotel-main
```

### PowerShell muestra `>>`

PowerShell espera que se termine un comando incompleto. Presionar `Ctrl + C` y
ejecutar cada comando por separado.

### `Failed to spawn: uvicorn`

Ejecutar el backend mediante Python:

```powershell
uv sync
uv run python -m uvicorn main:app --reload
```

### El frontend no conecta con el backend

Comprobar:

- Que el backend siga abierto en otra terminal.
- Que `http://localhost:8000/docs` responda.
- Que `frontend/.env` use `VITE_API_URL=http://localhost:8000`.
- Reiniciar `npm run dev` después de modificar `.env`.
- Si se usa Docker Compose, ejecutar `docker compose --env-file server/.env ps`.

### SQL Server no aparece como `healthy`

Verificar que Docker Desktop esté abierto y consultar:

```powershell
docker compose --env-file server/.env ps
docker logs hotel-sqlserver
```

## Verificacion del proyecto

Frontend:

```powershell
cd frontend
npm run lint
npm run build
```

Backend:

```powershell
cd server
uv run python -m compileall src main.py
```

## Tecnologias

- React 18.
- Vite.
- Axios.
- React Router DOM.
- Recharts.
- FastAPI.
- SQLModel.
- SQL Server 2022.
- PyODBC.
- bcrypt.
- Docker Compose.

## Consideraciones actuales

El modelo existente no almacena capacidad de habitación, estado histórico de
reserva, fecha propia de factura ni estado de pago. La interfaz utiliza
solamente los campos que realmente se guardan en SQL Server.

La disponibilidad de una habitación es global: crear una reserva la marca como
no disponible y eliminar esa reserva vuelve a habilitarla.
