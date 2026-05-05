<template>
  <main v-if="song" class="play-view">
    <section
      class="song-bg"
      :style="{ backgroundImage: `url(${song.background_image})` }"
    >
      <h2>{{ song.title }} - {{ song.artist }}</h2>

      <AudioPlayer
        :song="song"
        :stop-audio="stopAudio"
        @onTimeUpdate="handleTimeUpdate"
        @onEnded="handleEnded"
      />

      <LyricsDisplay
        :song="song"
        :current-time="currentTime"
        @stopAudio="handleStopAudio"
        @startAudio="handleStartAudio"
        @summary="handleSummary"
      />
    </section>

    <div v-if="summary" class="summary-card">
      <h3>Results</h3>
      <p>Correct answers: {{ summary.correct }}</p>
      <p>Wrong answers: {{ summary.wrong }}</p>
    </div>
  </main>

  <p v-else>Loading song...</p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSong, createSongUser } from '../services/api'
import AudioPlayer from '../components/AudioPlayer.vue'
import LyricsDisplay from '../components/LyricsDisplay.vue'
import { useAuthStore } from '../stores/auth'

const route = useRoute()

const song = ref(null)
const stopAudio = ref(false)
const currentTime = ref(0)
const auth = useAuthStore()
const summary = ref(null)

onMounted(async () => {
  song.value = await getSong(route.params.id)
})

function handleTimeUpdate(time) {
  currentTime.value = time
}

function handleEnded() {
  console.log('Song finished')
}

function handleStopAudio() {
  stopAudio.value = true
}

function handleStartAudio() {
  stopAudio.value = false
}

async function handleSummary(data) {
  summary.value = data

  if (auth.isAuthenticated) {
    await createSongUser({
      song: song.value.id,
      correct_guesses: data.correct,
      wrong_guesses: data.wrong,
    })
  }
}
</script>