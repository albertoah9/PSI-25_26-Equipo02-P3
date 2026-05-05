<template>
  <div class="song-cards">
    <RouterLink
      v-for="song in songs"
      :key="song.id"
      class="song-card"
      :to="`/songs/${song.id}`"
    >
      <img
        :src="song.background_image"
        :alt="song.title"
      />

      <div class="song-card-body">
        <div class="song-title">
          {{ song.title }}
        </div>

        <div class="song-artist">
          {{ song.artist }}
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  songs: {
    type: Array,
    default: () => [],
  },
})
</script>