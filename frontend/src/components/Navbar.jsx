export default function Navbar({ onSearch }) {
  return (
    <header className="navbar">
      <h1>Media Server</h1>
      <input placeholder="Search titles..." onChange={(e) => onSearch(e.target.value)} />
    </header>
  )
}
