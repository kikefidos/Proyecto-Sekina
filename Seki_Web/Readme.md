# SekiWeb

Plataforma de cursos en línea similar a Platzi.

## Instalación

1. Copia `.env.local.example` a `.env.local` y ajusta `NEXT_PUBLIC_API_URL` si es necesario.
2. Instala dependencias: `npm install`
3. Ejecuta el servidor de desarrollo: `npm run dev`
4. Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

## API

Asegúrate de que tu API esté corriendo y que `NEXT_PUBLIC_API_URL` apunte a su base.

Endpoints usados:
- GET /courses: Lista de cursos
- GET /courses/:id: Detalle de un curso
- POST /login: Iniciar sesión

### Flujo de autenticación usado por el MVP

- El frontend guarda un token temporal en `localStorage` para llamadas desde el cliente.
- Además, tras un login exitoso el frontend llama a la API interna `POST /api/auth/session` para establecer una cookie `session` HttpOnly (usada por `middleware.js` para proteger rutas como `/profile`).
- Al hacer logout, el frontend borra `localStorage` y llama `DELETE /api/auth/session` para eliminar la cookie.

### Cómo probar el login y la sesión

1. Arranca tu API (ej. en `http://localhost:3001`). El endpoint `POST /login` debe devolver JSON con `{ token: string, user: { email, name } }` en caso de éxito.
2. Copia `.env.local.example` a `.env.local` si no lo hiciste y ajusta `NEXT_PUBLIC_API_URL` si tu API no está en `http://localhost:3001`.
3. Corre el frontend:

```bash
npm install
npm run dev
```

4. Abre `http://localhost:3000/login`, completa credenciales y envía el formulario.
	- Si el login es exitoso: el token se almacena en `localStorage`, se llama a `POST /api/auth/session` que escribe la cookie HttpOnly `session`, y serás redirigido a `/`.
	- Visita `/profile` para verificar que la ruta está protegida; si la cookie no existe serás redirigido a `/login`.

### Variables de entorno

- `NEXT_PUBLIC_API_URL` — URL base de la API (por defecto `http://localhost:3001`).

### Notas de seguridad y siguientes pasos

- En este MVP la cookie `session` se escribe desde el servidor de Next.js con `HttpOnly`, pero no está marcada como `secure`/`sameSite` en todos los entornos. Para producción debes activar `secure: true` y `sameSite: 'lax'`/`strict` según tu estrategia, y servir sobre HTTPS.
- Considera usar refresh tokens y rotación de tokens para mayor seguridad.
- Para APIs sensibles, valida el JWT en el servidor y no confíes en `localStorage` para seguridad crítica.
 
### Refresh tokens y comportamiento en este proyecto

- El MVP incluye un endpoint interno `GET /api/auth/refresh` que intenta renovar el access token consultando al endpoint externo de tu API (`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/auth/refresh`). Si el backend externo devuelve un `accessToken` (y opcionalmente un `refreshToken`), el endpoint interno devuelve `{ token, user }` y, si viene `refreshToken`, escribe una cookie `session` HttpOnly con él.
- En el frontend `AuthProvider` en el arranque intenta lo siguiente:
	1. Si existe un `token` en `localStorage`, lo usa y obtiene el perfil `/me`.
	2. Si no existe token, llama `GET /api/auth/refresh` para intentar renovar usando la cookie HttpOnly y, si recibe un `token`, lo guarda en `localStorage` y carga el `user`.

Esto permite mantener la cookie HttpOnly como refresh token y el `accessToken` en `localStorage` para llamadas cliente, con la posibilidad de rotar tokens desde el servidor externo.

## Tecnologías

- Next.js
- React
- Tailwind CSS