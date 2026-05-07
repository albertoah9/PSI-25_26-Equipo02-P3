const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function loginUser(username, password) {
  const response = await fetch(`${API_BASE_URL}/token/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      password,
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || 'Login failed')
  }

  console.log(data)

  return data
}


export async function apiFetch(path, options = {}) {
  const token = sessionStorage.getItem('auth_token')

  const headers = {
    ...options.headers,
  }

  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }

  if (token) {
    headers.Authorization = `Token ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
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
