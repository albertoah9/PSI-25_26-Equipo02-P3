<template>
  <main>
    <h1>SongProject</h1>

    <section>
      <p>
        Practice your listening skills by completing missing words
        while listening to songs.
      </p>
    </section>

    <section>
      <button type="button" @click="handleRandomSong">
        Random song
      </button>

      <p v-if="randomError">{{ randomError }}</p>
    </section>

    <section>
      <h2>Most popular songs</h2>

      <p v-if="loadingTopSongs">Loading songs...</p>
      <p v-else-if="topSongsError">{{ topSongsError }}</p>

      <ul v-else>
        <li
          v-for="song in topSongs"
          :key="song.id"
        >
          <RouterLink :to="`/songs/${song.id}`">
            {{ song.title }} - {{ song.artist }}
          </RouterLink>
        </li>
      </ul>
    </section>

    <section>
      <h2>Search songs</h2>

      <form @submit.prevent="handleSearch">
        <input
          v-model="searchTitle"
          type="text"
          placeholder="Search by title"
        />

        <button type="submit">
          Search
        </button>
      </form>

      <p v-if="searchError">{{ searchError }}</p>

      <ul v-if="searchResults.length > 0">
        <li
          v-for="song in searchResults"
          :key="song.id"
        >
          <RouterLink :to="`/songs/${song.id}`">
            {{ song.title }} - {{ song.artist }}
          </RouterLink>
        </li>
      </ul>

      <p v-else-if="searchDone">
        No songs found.
      </p>
    </section>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { getTopSongs, searchSongs, getRandomSong } from '../services/api'

const router = useRouter()

const topSongs = ref([])
const loadingTopSongs = ref(false)
const topSongsError = ref('')

const searchTitle = ref('')
const searchResults = ref([])
const searchError = ref('')
const searchDone = ref(false)

const randomError = ref('')

onMounted(async () => {
  loadingTopSongs.value = true
  topSongsError.value = ''

  try {
    topSongs.value = await getTopSongs()
  } catch {
    topSongsError.value = 'Could not load top songs'
  } finally {
    loadingTopSongs.value = false
  }
})

async function handleSearch() {
  searchError.value = ''
  searchResults.value = []
  searchDone.value = false

  const title = searchTitle.value.trim()

  if (!title) {
    searchError.value = 'Please enter a title'
    return
  }

  try {
    searchResults.value = await searchSongs(title)
  } catch {
    searchError.value = 'Could not search songs'
  } finally {
    searchDone.value = true
  }
}

async function handleRandomSong() {
  randomError.value = ''

  try {
    const song = await getRandomSong()
    router.push(`/songs/${song.id}`)
  } catch {
    randomError.value = 'Could not load random song'
  }
}
</script>