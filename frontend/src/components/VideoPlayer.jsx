import { useEffect, useRef } from 'react'
import Hls from 'hls.js'

export default function VideoPlayer({ manifest, fallbackUrl, subtitleUrl, onProgress }) {
  const ref = useRef(null)

  useEffect(() => {
    const video = ref.current
    if (!video || !manifest) return

    if (manifest.mode === 'hls' && Hls.isSupported()) {
      const hls = new Hls()
      hls.loadSource((import.meta.env.VITE_BACKEND_ORIGIN || 'http://localhost:8000') + manifest.url)
      hls.attachMedia(video)
      return () => hls.destroy()
    }

    video.src = (import.meta.env.VITE_BACKEND_ORIGIN || 'http://localhost:8000') + (fallbackUrl || manifest.url)
  }, [manifest, fallbackUrl])

  return (
    <video
      ref={ref}
      className="video-player"
      controls
      onTimeUpdate={(e) => onProgress?.(Math.floor(e.target.currentTime))}
    >
      {subtitleUrl && <track label="Subtitle" kind="subtitles" srcLang="en" src={subtitleUrl} default />}
    </video>
  )
}
