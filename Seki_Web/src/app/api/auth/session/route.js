import { NextResponse } from 'next/server'

const isProd = process.env.NODE_ENV === 'production'

export async function POST(req) {
  try {
    const body = await req.json()
    const token = body?.token
    if (!token) return NextResponse.json({ error: 'token missing' }, { status: 400 })

    const res = NextResponse.json({ ok: true })
    // Set HttpOnly cookie for session token (expires in 7 days)
    res.cookies.set({
      name: 'session',
      value: token,
      httpOnly: true,
      path: '/',
      maxAge: 60 * 60 * 24 * 7,
      secure: isProd,
      sameSite: 'lax',
    })
    return res
  } catch (e) {
    return NextResponse.json({ error: 'invalid' }, { status: 400 })
  }
}

export async function DELETE() {
  const res = NextResponse.json({ ok: true })
  res.cookies.set({ name: 'session', value: '', path: '/', maxAge: 0, secure: isProd, sameSite: 'lax' })
  return res
}
