<template>
  <ul>
    <li v-for="song in songs" :key="song.id">
      <RouterLink :to="`/songs/${song.id}`">
        {{ song.artist }} - {{ song.title }}
      </RouterLink>
    </li>
  </ul>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  songs: Array
})
</script>