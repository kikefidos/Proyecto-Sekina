import './globals.css'
import Providers from '@/components/Providers'

export const metadata = {
  title: 'SekiWeb - Plataforma de Cursos',
  description: 'Aprende con nosotros',
}

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}