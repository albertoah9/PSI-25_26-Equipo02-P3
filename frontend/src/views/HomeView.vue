<template>
  <main>
    <h1>SongProject</h1>

    <p>
      Listen to songs and complete the missing words in the lyrics.
    </p>

    <button @click="goToRandomSong">
      Random song
    </button>

    <section>
      <h2>Most popular songs</h2>
      <p v-if="error">{{ error }}</p>
      <SongList :songs="topSongs" />
    </section>

    <SongSearch />
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getTopSongs, getRandomSong } from '../api'
import SongList from '../components/SongList.vue'
import SongSearch from '../components/SongSearch.vue'

const router = useRouter()

const topSongs = ref([])
const error = ref('')

onMounted(async () => {
  try {
    topSongs.value = await getTopSongs()
  } catch (e) {
    error.value = 'Could not load top songs'
  }
})

async function goToRandomSong() {
  try {
    const song = await getRandomSong()
    router.push(`/songs/${song.id}`)
  } catch (e) {
    error.value = 'Could not load random song'
  }
}
</script>

