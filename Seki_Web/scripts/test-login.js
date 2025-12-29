const fetch = require('node-fetch')

async function run() {
  const API = process.env.API || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'
  const FRONT = process.env.FRONT || 'http://localhost:3000'

  const LOGIN_PATH = process.env.LOGIN_PATH || '/auth/login'
  const EMAIL = process.env.EMAIL || process.env.USER_EMAIL || 'test@example.com'
  const PASSWORD = process.env.PASSWORD || process.env.USER_PASSWORD || 'password'
  console.log(`1) Calling external ${LOGIN_PATH}`)
  const loginRes = await fetch(`${API}${LOGIN_PATH}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: EMAIL, contrasena: PASSWORD }),
  })

  const loginData = await loginRes.json()
  console.log('login response:', loginData)
  if (!loginData.token) {
    console.error('Login failed; aborting')
    return
  }

  console.log('2) Calling frontend /api/auth/session to write cookie')
  const sessionRes = await fetch(`${FRONT}/api/auth/session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: loginData.refreshToken || loginData.token }),
  })
  console.log('session status', sessionRes.status)

  // Capture Set-Cookie from session response and forward it to refresh
  const rawSetCookie = sessionRes.headers && (sessionRes.headers.get('set-cookie') || (sessionRes.headers.raw && sessionRes.headers.raw()['set-cookie'] && sessionRes.headers.raw()['set-cookie'][0]))
  if (!rawSetCookie) {
    console.log('No Set-Cookie header from session response; refresh may fail from node')
  }

  console.log('3) Calling frontend internal refresh endpoint to obtain access token using cookie')
  const refreshRes = await fetch(`${FRONT}/api/auth/refresh`, {
    method: 'GET',
    headers: rawSetCookie ? { cookie: rawSetCookie.split(';')[0] } : {},
  })
  try {
    const refreshData = await refreshRes.json()
    console.log('refresh response:', refreshData)
  } catch (e) {
    console.log('no json in refresh response', e)
  }

  console.log('Test complete')
}

run().catch((e) => { console.error(e); process.exit(1) })
