<template>
  <audio
    ref="audio"
    controls
    :src="song.audio_file"
    @timeupdate="emitTimeUpdate"
    @ended="emitEnded"
  />
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  song: {
    type: Object,
    required: true,
  },
  stopAudio: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['onTimeUpdate', 'onEnded'])

const audio = ref(null)

watch(
  () => props.stopAudio,
  async (value) => {
    if (!audio.value) return

    if (value) {
      audio.value.pause()
    } else {
      try {
        await audio.value.play()
      } catch {
        // El navegador puede bloquear play() si no hubo interacción del usuario.
      }
    }
  }
)

function emitTimeUpdate() {
  if (!audio.value) return
  emit('onTimeUpdate', audio.value.currentTime)
}

function emitEnded() {
  emit('onEnded')
}
</script>
