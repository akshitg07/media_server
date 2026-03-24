import { Link } from 'react-router-dom'

export default function MediaCard({ item }) {
  return (
    <Link className="media-card" to={`/media/${item.id}`}>
      <div className="poster-wrap">
        {item.poster_url ? <img src={item.poster_url} alt={item.title} /> : <div className="placeholder">No Image</div>}
      </div>
      <p>{item.title}</p>
    </Link>
  )
}
