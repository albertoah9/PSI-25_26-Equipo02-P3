<template>
  <section>
    <h2>Search songs</h2>

    <form @submit.prevent="handleSearch">
      <input
        v-model="title"
        type="text"
        placeholder="Song title"
      />
      <button type="submit">Search</button>
    </form>

    <p v-if="error">{{ error }}</p>

    <SongList v-if="songs.length" :songs="songs" />
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { searchSongs } from '../services/api'
import SongList from './SongList.vue'

const title = ref('')
const songs = ref([])
const error = ref('')

async function handleSearch() {
  error.value = ''
  songs.value = []

  if (!title.value.trim()) {
    error.value = 'Write a song title'
    return
  }

  try {
    songs.value = await searchSongs(title.value)
  } catch {
    error.value = 'No songs found'
  }
}
</script>
