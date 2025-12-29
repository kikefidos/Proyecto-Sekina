'use client'

import { useEffect } from 'react'
import { useAuth } from '@/context/AuthProvider'
import { useRouter } from 'next/navigation'
import Header from '@/components/Header'

export default function ProfilePage() {
  const { user } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!user) router.push('/login')
  }, [user, router])

  if (!user) return <div><Header /><div className="container p-6">Redirigiendo a login...</div></div>

  return (
    <div>
      <Header />
      <main className="container p-6">
        <h1 className="text-3xl font-bold mb-4">Mi perfil</h1>
        <div className="card max-w-md">
          <p><strong>Nombre:</strong> {user.name || '—'}</p>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
      </main>
    </div>
  )
}
