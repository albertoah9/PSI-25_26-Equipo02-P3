<template>
  <main>
    <section>
      <h1>Learn a language through songs</h1>

      <p>
        "Songs" is the new way to learn English and other languages through music
        and the lyrics of your favourite songs. Improve and practise your listening
        skills with the best music videos. Fill in the gaps to the lyrics as you
        listen and sing Karaoke to your favourites.
      </p>

      <button
        :disabled="loadingRandom"
        @click="goRandom"
      >
        Random song
      </button>
    </section>

    <section>
      <h2>Top Songs</h2>

      <div v-if="topSongs.length > 0" class="song-cards">
        <SongList :songs="topSongs" />
      </div>

      <p v-else>
        Loading...
      </p>
    </section>

    <section>
      <SongSearch />
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTopSongs, getRandomSong } from '../services/api'
import SongList from '../components/SongList.vue'
import SongSearch from '../components/SongSearch.vue'

const router = useRouter()
const topSongs = ref([])
const loadingRandom = ref(false)

async function loadTop() {
  try {
    topSongs.value = await getTopSongs()
  } catch (err) {
    console.error('Error loading top songs:', err)
  }
}

async function goRandom() {
  loadingRandom.value = true

  try {
    const song = await getRandomSong()

    if (song && song.id) {
      router.push(`/songs/${song.id}`)
    }
  } catch (err) {
    console.error('Random error:', err)
  } finally {
    loadingRandom.value = false
  }
}

onMounted(loadTop)
</script>
