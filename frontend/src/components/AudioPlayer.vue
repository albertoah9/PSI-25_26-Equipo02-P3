<template>
  <audio
    ref="audio"
    controls
    :src="song.audio_file"
    @timeupdate="emitTimeUpdate" 
    @ended="emitEnded"
  />
  <!-- el emitTimeUpdate envia todo el rato el segundo por el que va la cancion, esto lo usa lyricsDisplay-->
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  song: {
    type: Object,
    required: true,
  },
  stopAudio: {
    type: Boolean, // true pausado, false reproduce
    default: false,
  },
})

const emit = defineEmits(['onTimeUpdate', 'onEnded'])

const audio = ref(null)
// esto provoca la reacción cuando cambia stopAudio
watch(
  () => props.stopAudio, // esta linea es lo que marca lo que se quiere vigilar, en este caso el cambio de pausa a reporucir
  (value) => { // aqui coge el valor de porps.stopAudio
    if (!audio.value) return // si no existe la canción vuelve

    if (value) {
      audio.value.pause()
    } else {
      audio.value.play()
    }
  }
)
// manda al padre el tiempo actual
function emitTimeUpdate() {
  emit('onTimeUpdate', audio.value.currentTime)
}
// evento para avisar a PlayView que la canción ha terminado
function emitEnded() {
  emit('onEnded')
}
</script>