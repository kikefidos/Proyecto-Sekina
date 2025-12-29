'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import { useAuth } from '@/context/AuthProvider'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const { login, loading } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      await login({ email, password })
    } catch (err) {
      setError(err.message || 'Error en login')
    }
  }

  return (
    <div>
      <Header />
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-4">Iniciar Sesión</h1>
        <form onSubmit={handleSubmit} className="max-w-md">
          {error && <div className="text-red-600 mb-3">{error}</div>}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border p-2 w-full mb-2"
            required
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border p-2 w-full mb-2"
            required
          />
          <button type="submit" disabled={loading} className="btn-primary w-full">{loading ? 'Ingresando...' : 'Iniciar Sesión'}</button>
        </form>
      </div>
    </div>
  )
}