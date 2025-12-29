import { NextResponse } from 'next/server'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'

// This route attempts to refresh an access token by forwarding the
// incoming cookie header to the external API refresh endpoint.
export async function GET(req) {
  try {
    const cookieHeader = req.headers.get('cookie') || ''
    // Try external refresh endpoint. Adjust path if your API uses a different route.
    const res = await fetch(`${API_URL}/auth/refresh`, {
      method: 'GET',
      headers: { cookie: cookieHeader },
    })

    if (!res.ok) return NextResponse.json({ ok: false }, { status: res.status })

    const data = await res.json()

    // Expecting { accessToken, refreshToken?, user? }
    const accessToken = data.accessToken || data.token || null
    const refreshToken = data.refreshToken || null

    const out = NextResponse.json({ token: accessToken, user: data.user || null })

    // If external returned a refreshToken, set it as HttpOnly cookie
    if (refreshToken) {
      const isProd = process.env.NODE_ENV === 'production'
      out.cookies.set({ name: 'session', value: refreshToken, httpOnly: true, path: '/', maxAge: 60 * 60 * 24 * 30, secure: isProd, sameSite: 'lax' })
    }

    return out
  } catch (e) {
    return NextResponse.json({ ok: false }, { status: 500 })
  }
}
