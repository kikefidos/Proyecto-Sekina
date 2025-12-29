import { NextResponse } from 'next/server'

export function middleware(req) {
  const { pathname } = req.nextUrl

  // Protect /profile and any /dashboard routes
  const protectedPaths = ['/profile']
  const needsAuth = protectedPaths.some((p) => pathname === p || pathname.startsWith(p + '/'))

  if (!needsAuth) return NextResponse.next()

  const session = req.cookies.get('session')
  if (!session) {
    const url = req.nextUrl.clone()
    url.pathname = '/login'
    url.search = `returnTo=${encodeURIComponent(pathname)}`
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/profile', '/profile/:path*'],
}
