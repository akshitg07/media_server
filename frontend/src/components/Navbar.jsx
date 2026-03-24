import { useAuth } from '../context/AuthContext'

export default function Navbar({ onSearch }) {
  const { logout } = useAuth()

  return (
    <header className="navbar">
      <h1>Media Server</h1>
      <input placeholder="Search titles..." onChange={(e) => onSearch(e.target.value)} />
      <button onClick={logout}>Logout</button>
    </header>
  )
}
