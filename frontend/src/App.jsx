import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import LoginPage from './pages/LoginPage'
import HomePage from './pages/HomePage'
import DetailPage from './pages/DetailPage'

function ProtectedRoutes() {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/media/:id" element={<DetailPage />} />
    </Routes>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/*" element={<ProtectedRoutes />} />
      </Routes>
    </AuthProvider>
  )
}
