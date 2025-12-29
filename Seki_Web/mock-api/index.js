const express = require('express')
const cookieParser = require('cookie-parser')
const app = express()
app.use(express.json())
app.use(cookieParser())

const PORT = process.env.PORT || 3001

const mockUser = { email: 'test@example.com', name: 'Test User' }

app.post('/login', (req, res) => {
  const { email, password } = req.body
  if (email === 'test@example.com' && password === 'password') {
    return res.json({ token: 'mock-access-token', user: mockUser, refreshToken: 'mock-refresh-token' })
  }
  return res.status(401).json({ error: 'invalid credentials' })
})

app.get('/courses', (req, res) => {
  res.json([
    { id: '1', title: 'Curso 1', description: 'Descripción 1' },
    { id: '2', title: 'Curso 2', description: 'Descripción 2' },
  ])
})

app.get('/courses/:id', (req, res) => {
  res.json({ id: req.params.id, title: `Curso ${req.params.id}`, description: 'Detalle del curso', lessons: [] })
})

app.get('/me', (req, res) => {
  const auth = req.headers.authorization || ''
  if (auth === 'Bearer mock-access-token') return res.json(mockUser)
  return res.status(401).json({ error: 'unauthorized' })
})

app.get('/auth/refresh', (req, res) => {
  const sessionCookie = req.cookies.session
  if (sessionCookie === 'mock-refresh-token') {
    return res.json({ accessToken: 'mock-access-token', refreshToken: 'mock-refresh-token', user: mockUser })
  }
  return res.status(401).json({ error: 'no refresh' })
})

app.listen(PORT, () => console.log(`Mock API listening on http://localhost:${PORT}`))
