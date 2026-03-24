import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api/client'
import VideoPlayer from '../components/VideoPlayer'

export default function DetailPage() {
  const { id } = useParams()
  const [item, setItem] = useState(null)
  const [manifest, setManifest] = useState(null)

  useEffect(() => {
    api.get(`/media/${id}`).then((r) => setItem(r.data))
    api.get(`/stream/${id}/manifest`).then((r) => setManifest(r.data))
  }, [id])

  const reportProgress = (seconds) => {
    api.post('/media/history', { media_id: Number(id), progress_seconds: seconds, completed: false }).catch(() => {})
  }

  if (!item) return <p>Loading...</p>

  const subtitle = item.subtitles?.[0]
  const subtitleUrl = subtitle
    ? `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'}/media/${id}/subs/${subtitle.id}`
    : null

  return (
    <div className="detail-page dark">
      <h1>{item.title}</h1>
      <p>{item.overview || 'No description available.'}</p>
      {manifest && (
        <VideoPlayer
          manifest={manifest}
          fallbackUrl={`/api/stream/${id}/direct`}
          subtitleUrl={subtitleUrl}
          onProgress={reportProgress}
        />
      )}
    </div>
  )
}
