import { useEffect, useState } from 'react'
import { api } from '../api/client'
import Navbar from '../components/Navbar'
import MediaCard from '../components/MediaCard'

export default function HomePage() {
  const [items, setItems] = useState([])
  const [query, setQuery] = useState('')

  useEffect(() => {
    api.get('/media', { params: query ? { q: query } : {} }).then((r) => setItems(r.data))
  }, [query])

  return (
    <div className="page dark">
      <Navbar onSearch={setQuery} />
      <section>
        <h2>Continue Watching</h2>
        <div className="grid">{items.slice(0, 6).map((item) => <MediaCard item={item} key={item.id} />)}</div>
      </section>
      <section>
        <h2>All Media</h2>
        <div className="grid">{items.map((item) => <MediaCard item={item} key={item.id} />)}</div>
      </section>
    </div>
  )
}
