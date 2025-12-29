'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { login as apiLogin } from '@/lib/api'
import { fetchWithAuth } from '@/lib/fetcher'
import { useRouter } from 'next/navigation'

const AuthContext = createContext({})

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const t = localStorage.getItem('token')
    if (t) {
      setToken(t)
      // intentar recuperar user desde /me usando fetchWithAuth
      ;(async () => {
        try {
          const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'
          const res = await fetchWithAuth(`${base}/me`)
          if (res.ok) {
            const data = await res.json()
            setUser(data)
          }
        } catch (e) {
          // no pasar nada si falla
        } finally {
          setLoading(false)
        }
      })()
    } else {
      // Try to refresh using server-side cookie (HttpOnly)
      ;(async () => {
        try {
          const r = await fetch('/api/auth/refresh')
          if (r.ok) {
            const d = await r.json()
            if (d?.token) {
              localStorage.setItem('token', d.token)
              setToken(d.token)
              setUser(d.user || null)
            }
          }
        } catch (e) {
          // no pasar nada
        } finally {
          setLoading(false)
        }
      })()
    }
  }, [])

  const login = async (credentials) => {
    setLoading(true)
    try {
      const data = await apiLogin(credentials)
      if (data?.token) {
        // store token for client fetches
        localStorage.setItem('token', data.token)
        setToken(data.token)
        setUser(data.user || null)

        // set HttpOnly cookie via internal API route
        try {
          await fetch('/api/auth/session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: data.token }),
          })
        } catch (e) {
          // ignore cookie set failures
        }

        router.push('/')
        return data
      }
      throw new Error('No token received')
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    // clear cookie via internal API route
    fetch('/api/auth/session', { method: 'DELETE' }).finally(() => {
      router.push('/login')
    })
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
