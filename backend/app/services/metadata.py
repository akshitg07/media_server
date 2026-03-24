import httpx

from app.core.config import get_settings

settings = get_settings()


async def fetch_tmdb_metadata(title: str, media_type: str) -> dict:
    if not settings.tmdb_api_key:
        return {}

    endpoint = "movie" if media_type == "movie" else "tv"
    params = {"api_key": settings.tmdb_api_key, "query": title}

    async with httpx.AsyncClient(timeout=8.0) as client:
        response = await client.get(f"{settings.tmdb_base_url}/search/{endpoint}", params=params)
        response.raise_for_status()
        results = response.json().get("results", [])

    if not results:
        return {}
    first = results[0]
    return {
        "title": first.get("title") or first.get("name") or title,
        "overview": first.get("overview", ""),
        "poster_url": f"https://image.tmdb.org/t/p/w500{first.get('poster_path', '')}" if first.get("poster_path") else "",
        "backdrop_url": f"https://image.tmdb.org/t/p/w780{first.get('backdrop_path', '')}" if first.get("backdrop_path") else "",
    }
