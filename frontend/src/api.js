const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export async function apiFetch(path, options = {}) {
  const token = sessionStorage.getItem('token')

  const headers = {
    ...options.headers,
  }

  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }

  if (token) {
    headers.Authorization = `Token ${token}`
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw error
  }

  return response.json()
}

export function getTopSongs() {
  return apiFetch('/songs/top/?n=3')
}

export function searchSongs(title) {
  return apiFetch(`/songs/search/?title=${encodeURIComponent(title)}`)
}

export function getRandomSong() {
  return apiFetch('/songs/random/')
}

export function getSong(id) {
  return apiFetch(`/songs/${id}/`)
}

export function createSongUser(data) {
  return apiFetch('/songusers/', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}