# Sistema de reservaciones de hotel

Este backend centraliza la gestion de clientes, habitaciones, reservaciones, facturacion y autenticacion de usuarios dentro de un sistema hotelero. La API fue desarrollada con FastAPI y se organiza en capas `api`, `application`, `domain` e `infrastructure`, con una separacion clara entre la exposicion HTTP, la logica del negocio y la persistencia.

Nota: actualmente este README documenta unicamente el backend ubicado en `server/`.

## Características

- El sistema permite administrar clientes a lo largo de su ciclo completo, desde el registro inicial hasta su consulta, actualizacion, eliminacion y listado general.
- La gestion de habitaciones contempla su registro, consulta individual, actualizacion de datos, cambio de estado y visualizacion del inventario disponible.
- La API puede filtrar habitaciones disponibles mediante el parametro `available=true`, lo que facilita su consulta operativa.
- Las reservaciones pueden crearse, consultarse y actualizarse en sus fechas cuando ya existen en el sistema.
- Cada cliente puede consultar su historial de reservaciones, lo que permite dar seguimiento a su actividad.
- La facturacion se genera a partir de reservaciones existentes y puede consultarse tanto por identificador propio como por reservacion asociada.
- El backend tambien expone un resumen de factura con datos vinculados del cliente, las habitaciones y el metodo de pago.
- En el modulo de usuarios se incluye registro, inicio de sesion y cambio de contrasena.
- Los errores de la aplicacion se devuelven mediante un formato JSON uniforme para mantener consistencia en la API.
- Al iniciar, la aplicacion crea automaticamente las tablas registradas en el modelo de datos.

## Tecnologías Utilizadas

- Python 3.13.
- FastAPI.
- Uvicorn.
- SQLModel.
- SQLAlchemy.
- PyODBC.
- Microsoft SQL Server mediante `mssql+pyodbc`.
- bcrypt para hash y validacion de contrasenas.
- `uv` para gestion de dependencias (`pyproject.toml` y `uv.lock`).

## Arquitectura

El proyecto sigue una base inspirada en Clean Architecture y distribuye sus responsabilidades por capas para mantener el codigo mas ordenado y predecible:

- `api`: expone los endpoints HTTP y traduce errores a respuestas HTTP.
- `application`: contiene DTOs y casos de uso que coordinan la logica de negocio.
- `domain`: define entidades, excepciones y reglas de negocio.
- `infrastructure`: implementa persistencia, modelos SQLModel, mapeos y repositorios.

En terminos generales, una solicitud entra por una ruta HTTP, pasa a un caso de uso, se valida con reglas de negocio y finalmente interactua con los repositorios y la base de datos.

## Estructura del Proyecto

```text
backend-proy2-progra4/
|-- server/
|   |-- main.py
|   |-- pyproject.toml
|   |-- uv.lock
|   |-- .env.example
|   `-- src/
|       |-- api/
|       |   `-- routes/
|       |-- application/
|       |   |-- dtos/
|       |   `-- uses_cases/
|       |-- domain/
|       |   |-- bussiness_rules/
|       |   |-- entities/
|       |   `-- exeptions.py
|       `-- infrastructure/
|           |-- database/
|           |-- mappers/
|           |-- models/
|           `-- repositories/
`-- .gitignore
```

- `server/main.py`: concentra el arranque de FastAPI, la configuracion de CORS y el manejo global de errores.
- `server/src/api/routes/`: agrupa las rutas REST por modulo, separando clientes, habitaciones, reservaciones, facturas y autenticacion.
- `server/src/application/dtos/`: define los modelos de entrada y salida con los que se comunica la API.
- `server/src/application/uses_cases/`: coordina la logica de aplicacion y el flujo de cada operacion.
- `server/src/domain/entities/`: representa las entidades principales del dominio hotelero.
- `server/src/domain/bussiness_rules/`: concentra las validaciones y reglas del negocio.
- `server/src/infrastructure/database/`: resuelve la conexion a la base de datos y la creacion de tablas.
- `server/src/infrastructure/models/`: contiene los modelos persistentes construidos con SQLModel.
- `server/src/infrastructure/repositories/`: encapsula el acceso a datos desde la capa de infraestructura.
- `server/src/infrastructure/mappers/`: se encarga de convertir entre entidades de dominio y modelos persistentes.

## Instalación

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd backend-proy2-progra4
```

2. Entrar al directorio del backend:

```bash
cd server
```

3. Instalar dependencias con `uv`:

```bash
uv sync
```

Nota: la URL exacta del repositorio no esta documentada en el proyecto y queda pendiente de agregar.

## Configuración

El backend toma su configuracion principal desde `server/.env`, y el proyecto incluye `server/.env.example` como referencia base para completar los valores necesarios.

Variables requeridas:

- `DB_SERVER`: servidor de base de datos.
- `DB_NAME`: nombre de la base de datos.
- `DB_USERNAME`: usuario de base de datos.
- `DB_PASSWORD`: contrasena de base de datos.

Variables opcionales:

- `DB_DRIVER`: driver ODBC. Valor por defecto: `ODBC Driver 17 for SQL Server`.
- `DB_TRUST_SERVER_CERTIFICATE`: valor por defecto `yes`.
- `DB_ECHO`: habilita logs SQL cuando vale `true`.
- `ALLOWED_ORIGINS`: origenes permitidos por CORS separados por coma. Por defecto: `http://localhost:3000,http://localhost:5173`.

Pasos recomendados:

1. Crear `server/.env` a partir de `server/.env.example`.
2. Configurar una instancia accesible de SQL Server.
3. Verificar que el driver ODBC configurado exista en el entorno donde correra el backend.

Nota: el proyecto no documenta configuraciones diferenciadas por ambiente y eso queda pendiente de documentar.

## Ejecución

Desde `server/`, ejecutar:

```bash
uv run uvicorn main:app --reload
```

Al iniciar, la aplicacion crea las tablas registradas en `SQLModel.metadata`, por lo que la estructura base de persistencia se prepara automaticamente.

## API

Todos los endpoints se publican bajo el prefijo base `/api/v1`, organizados por contexto funcional.

- Clientes: `POST /api/v1/clients`, `GET /api/v1/clients/{client_id}`, `PUT /api/v1/clients/{client_id}`, `DELETE /api/v1/clients/{client_id}`, `GET /api/v1/clients`.
- Habitaciones: `POST /api/v1/rooms`, `GET /api/v1/rooms/{room_number}`, `PUT /api/v1/rooms/{room_number}`, `PATCH /api/v1/rooms/{room_number}/status`, `GET /api/v1/rooms`, `GET /api/v1/rooms?available=true`.
- Reservaciones: `POST /api/v1/bookings`, `GET /api/v1/bookings/{booking_id}`, `PUT /api/v1/bookings/{booking_id}/dates`, `GET /api/v1/bookings/client/{client_id}/history`, `GET /api/v1/bookings`.
- Facturas: `POST /api/v1/bills`, `GET /api/v1/bills/{bill_id}`, `GET /api/v1/bills/booking/{booking_id}`, `GET /api/v1/bills/{bill_id}/summary`.
- Autenticacion: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `PUT /api/v1/auth/password`.

Ademas, la aplicacion expone la documentacion automatica de FastAPI en `/docs` y `/redoc`, salvo que esa configuracion cambie en el futuro.

Nota: los cuerpos de peticion y ejemplos de respuesta aun no estan documentados manualmente en el proyecto.

## Reglas de Negocio

- Clientes: se exige que `client_id` tenga valor, que `name` y `last_name` no incluyan numeros, que `email` tenga un formato valido y que `phone` sea un entero positivo de exactamente 8 digitos.
- Habitaciones: cada `room_number` debe ser positivo, `room_type` no puede estar vacio, `price` no puede ser negativo y al registrar una habitacion debe ser mayor que cero; para reservar, todas las habitaciones deben estar disponibles.
- Reservaciones: siempre deben incluir al menos una habitacion, trabajar con un cliente existente y con habitaciones existentes; ademas, `check_in` no puede estar en el pasado, la estancia debe durar al menos una noche, `check_in` no puede ser mayor que `check_out` y no se permiten traslapes por habitacion.
- Facturas: solo pueden generarse sobre una reservacion existente y con un metodo de pago existente y activo; ademas, solo puede existir una factura por reservacion, el total no puede ser negativo y debe coincidir con el calculo de la reservacion.
- Usuarios: `username` debe tener valor y no contener espacios, la contrasena se almacena como hash con `bcrypt`, los roles validos son `ADMIN` y `EMPLOYEE`, y tanto el login como el cambio de contrasena verifican las credenciales contra el hash guardado.

## Base de Datos

La persistencia se implementa con SQLModel sobre SQL Server. El proyecto registra directamente las siguientes tablas como base de su modelo de datos:

- `Clients`: almacena los datos principales de los clientes del sistema mediante los campos `client_id`, `name`, `last_name`, `phone` y `email`.
- `Rooms`: conserva la informacion de las habitaciones a traves de `room_number`, `room_type`, `price` y `available`.
- `Bookings`: registra las reservaciones con `booking_id`, `check_in`, `check_out` y `client_id`, permitiendo que un cliente tenga multiples reservaciones.
- `Bookings_Rooms`: funciona como tabla intermedia entre reservaciones y habitaciones, guardando `booking_room_id`, `booking_id`, `room_number`, `price_per_night` y `subtotal`.
- `Payment_methods`: describe los metodos de pago disponibles mediante `payment_method_id`, `name` y `active`.
- `Bills`: guarda las facturas con `bill_id`, `booking_id`, `payment_method_id` y `total`; cada factura pertenece a una reservacion y a un metodo de pago, y `booking_id` es unico para evitar duplicados por reservacion.
- `Users`: almacena los usuarios del backend con `username`, `password_hash` y `role`.

Relaciones generales:

- `Clients` 1:N `Bookings`.
- `Bookings` N:M `Rooms` mediante `Bookings_Rooms`.
- `Bookings` 1:1 `Bills`.
- `Payment_methods` 1:N `Bills`.
