<template>
  <section>
    <h2>Lyrics</h2>

    <div v-if="!lines.length">
      Loading lyrics...
    </div>
    <!--Recorre las 3 lineas visibles y pone en current la actual-->
    <div
      v-for="line in visibleLines"
      :key="line.index"
      :class="{ current: line.index === currentIndex }"
    > 
      <p>
        {{ renderLine(line) }}
      </p>
      <!-- SOLO muestra input (hueco para escribir) si es la linea actual, tiene hueco y no esta resuelta -->
      <div
        v-if="line.index === currentIndex && line.missingWord && !solved[line.index]"
      >
        <input
          v-model="currentInput"
          type="text"
          placeholder="Missing word"
          @keyup.enter="checkAnswer(line.index)"
        />
        <!-- Boton para corregir -->
        <button @click="checkAnswer(line.index)">
          Check
        </button>
        <!-- Boton para skip -->
        <button @click="skip(line.index)">
          Skip
        </button>
      </div>
    </div>

    <p>Correct: {{ correctGuesses }}</p>
    <p>Wrong: {{ wrongGuesses }}</p>
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
// LyricsDisplay recibe la canción y el segundo actual del audio (song y currentTime)
const props = defineProps({
  song: {
    type: Object,
    required: true,
  },
  currentTime: {
    type: Number,
    required: true,
  },
})
// Puede emitir tres eventos, parar el audio, reanudarlo y mandar el summaty que tiene las correct y wrong answers
const emit = defineEmits(['stopAudio', 'startAudio', 'summary'])

const lines = ref([])
const answers = ref({})
const solved = ref({})
const currentInput = ref('')
const correctGuesses = ref(0)
const wrongGuesses = ref(0)
const summarySent = ref(false)
// carga la letra con loadLyrics
onMounted(async () => {
  await loadLyrics()
})

// Esto lo que hace es fetch del archivo .lrc, lee el texto, y lo parsea a líneas utíles con parseLRC
async function loadLyrics() {
  const response = await fetch(props.song.lrc_file)
  const text = await response.text()

  lines.value = parseLrc(text)
}

// coge lineas con ese formato [00:22.48]You're so {hot}, teasing me y extrae los minutos, los segundos y el texto
function parseLrc(text) {
  return text
    .split('\n')
    .map((rawLine) => {
      const match = rawLine.match(/^\[(\d{2}):(\d{2}\.\d{2})\](.*)$/)

      if (!match) return null

      const minutes = Number(match[1])
      const seconds = Number(match[2])
      const time = minutes * 60 + seconds // convierte todo el tiempo a segundos
      const lyric = match[3].trim()

      const missingMatch = lyric.match(/\{([^}]+)\}/) // detecta la palabra oculta (la que hay que adivinar)
      const missingWord = missingMatch ? missingMatch[1].trim() : null // guarda la palabra en missing word
      // aqui crea el displayText para mostrar esto You're so _____, teasing me
      return {
        time,
        text: lyric,
        missingWord,
        displayText: lyric.replace(/\{([^}]+)\}/, '_____'),
      }
    })
    .filter(Boolean)
}

// Esto sirve para saber la linea actual
// lo que hace es comparar el tiempo actual del audio con el tiempo de la letra de manera que si
// la cancion va por el 22.50 y hay una linea en el 22.48 esa sera la actual
const currentIndex = computed(() => {
  if (!lines.value.length) return -1

  let index = 0

  for (let i = 0; i < lines.value.length; i++) {
    if (props.currentTime >= lines.value[i].time) {
      index = i
    }
  }

  return index
})

// esto muestra solo 3 líneas, la anterior, actual y siguiente
const visibleLines = computed(() => {
  if (currentIndex.value === -1) return []

  return lines.value
    .map((line, index) => ({ ...line, index }))
    .filter((line) => {
      return (
        line.index === currentIndex.value - 1 || line.index === currentIndex.value || line.index === currentIndex.value + 1)
    })
})

// vigila el cambio de linea, cuando se cambia de linea limpia el input, mira si la linea tiene palabra oculta
// si tiene hueco sin resolver emite el evento de parar canción, y si esta en la ultima linea emite evento de enseñar summary
watch(
  () => currentIndex.value,
  (newIndex) => {
    if (newIndex === -1) return

    currentInput.value = ''

    const line = lines.value[newIndex]

    if (line?.missingWord && !solved.value[newIndex]) {
      emit('stopAudio')
    }

    if (newIndex === lines.value.length - 1 && !summarySent.value) {
      sendSummary()
    }
  }
)

// para evitar problemas con espacios o mayusculas
function normalize(value) {
  return value.trim().toLowerCase()
}

// comprueba si la respuesta es correcta y en ese caso guarda la linea como resuelta, guarda la respuesta, suma acierto
// limpia el input y emite evento para reanudar
// si falla summa un intento fallido y mantiene la cancion parada
function checkAnswer(lineIndex) {
  const line = lines.value[lineIndex]

  if (!line?.missingWord) return

  if (normalize(currentInput.value) === normalize(line.missingWord)) {
    solved.value[lineIndex] = true
    answers.value[lineIndex] = currentInput.value
    correctGuesses.value += 1
    currentInput.value = ''
    emit('startAudio')
  } else {
    wrongGuesses.value += 1
    emit('stopAudio')
  }
}

// si se skipea se muestra el resultado, se guarda el resultado, se suma un intento fallido, se limpia input y se reanuda el audio
function skip(lineIndex) {
  const line = lines.value[lineIndex]

  if (!line?.missingWord) return

  solved.value[lineIndex] = true
  answers.value[lineIndex] = line.missingWord
  wrongGuesses.value += 1
  currentInput.value = ''
  emit('startAudio')
}

// Manda el resumen
function sendSummary() {
  summarySent.value = true

  emit('summary', {
    correct: correctGuesses.value,
    wrong: wrongGuesses.value,
  })
}

// pinta las lineas, si no tiene hueco pone el texto tal cual, si tiene hueco y esta resuelto lo muestra con el resultado
// y si esta sin resolver lo pone en el formato de antes 
function renderLine(line) {
  if (!line.missingWord) {
    return line.text
  }

  if (solved.value[line.index]) {
    return line.text.replace(/\{([^}]+)\}/, answers.value[line.index])
  }

  return line.displayText
}
</script>

<style scoped>
.current {
  font-weight: bold;
  background: #eeeeee;
  padding: 8px;
}
</style>