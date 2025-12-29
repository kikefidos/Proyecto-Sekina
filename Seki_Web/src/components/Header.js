 'use client'

import Link from 'next/link'
import { useAuth } from '@/context/AuthProvider'

export default function Header() {
  const { user, logout, loading } = useAuth()

  return (
    <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 shadow">
      <nav className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold">SekiWeb</Link>
        <div className="flex items-center">
          <Link href="/courses" className="mr-4 hover:underline">Cursos</Link>
          {loading ? (
            <span className="text-sm text-white/90">Cargando...</span>
          ) : user ? (
            <>
              <Link href="/profile" className="mr-4">{user.name || user.email}</Link>
              <button onClick={logout} className="bg-white text-blue-600 px-3 py-1 rounded">Salir</button>
            </>
          ) : (
            <Link href="/login" className="mr-2 hover:underline">Iniciar Sesión</Link>
          )}
        </div>
      </nav>
    </header>
  )
}