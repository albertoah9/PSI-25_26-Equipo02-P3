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

  if (!title.value.trim()) return

  try {
    songs.value = await searchSongs(title.value)
  } catch (err) {
    error.value = 'No songs found'
  }
}
</script>

<template>
  <section>
    <form class="search-form" @submit.prevent="handleSearch">
      <input
        v-model="title"
        type="text"
        placeholder="Search songs by title"
      />

      <button type="submit" class="btn-secondary">
        Search
      </button>
    </form>

    <p v-if="error">
      {{ error }}
    </p>

    <SongList
      v-if="songs.length > 0"
      :songs="songs"
    />
  </section>
</template>
