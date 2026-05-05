<template>
  <section>
    <h2>Lyrics</h2>

    <div v-if="!lines.length">
      Loading lyrics...
    </div>

    <div
      v-for="line in visibleLines"
      :key="line.index"
      :class="{ current: line.index === currentIndex }"
    >
      <p>
        {{ renderLine(line) }}
      </p>

      <div
        v-if="line.index === currentIndex && line.missingWord && !solved[line.index]"
      >
        <input
          v-model="currentInput"
          type="text"
          placeholder="Missing word"
          @input="checkAnswer(line.index)"
        />

        <button type="button" @click="skip(line.index)">
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

const emit = defineEmits(['stopAudio', 'startAudio', 'summary'])

const lines = ref([])
const answers = ref({})
const solved = ref({})
const currentInput = ref('')
const correctGuesses = ref(0)
const wrongGuesses = ref(0)
const summarySent = ref(false)

onMounted(async () => {
  await loadLyrics()
})

async function loadLyrics() {
  const response = await fetch(props.song.lrc_file)
  const text = await response.text()

  lines.value = parseLrc(text)
}

function parseLrc(text) {
  return text
    .split('\n')
    .map((rawLine) => {
      const match = rawLine.match(/^\[(\d{2}):(\d{2}\.\d{2})\](.*)$/)

      if (!match) return null

      const minutes = Number(match[1])
      const seconds = Number(match[2])
      const time = minutes * 60 + seconds
      const lyric = match[3].trim()

      const missingMatch = lyric.match(/\{([^}]+)\}/)
      const missingWord = missingMatch ? missingMatch[1].trim() : null

      return {
        time,
        text: lyric,
        missingWord,
        displayText: lyric.replace(/\{([^}]+)\}/, '_____'),
      }
    })
    .filter(Boolean)
}

const currentIndex = computed(() => {
  if (!lines.value.length) return -1

  let index = 0

  for (let i = 0; i < lines.value.length; i += 1) {
    if (props.currentTime >= lines.value[i].time) {
      index = i
    }
  }

  return index
})

const visibleLines = computed(() => {
  if (currentIndex.value === -1) return []

  return lines.value
    .map((line, index) => ({ ...line, index }))
    .filter((line) => (
      line.index === currentIndex.value - 1 ||
      line.index === currentIndex.value ||
      line.index === currentIndex.value + 1
    ))
})

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

function normalize(value) {
  return value.trim().toLowerCase()
}

function checkAnswer(lineIndex) {
  const line = lines.value[lineIndex]

  if (!line?.missingWord) return
  if (!currentInput.value.trim()) return

  if (normalize(currentInput.value) === normalize(line.missingWord)) {
    solved.value[lineIndex] = true
    answers.value[lineIndex] = currentInput.value
    correctGuesses.value += 1
    currentInput.value = ''
    emit('startAudio')
  } else if (currentInput.value.length >= line.missingWord.length) {
    wrongGuesses.value += 1
    emit('stopAudio')
  }
}

function skip(lineIndex) {
  const line = lines.value[lineIndex]

  if (!line?.missingWord) return

  solved.value[lineIndex] = true
  answers.value[lineIndex] = line.missingWord
  wrongGuesses.value += 1
  currentInput.value = ''
  emit('startAudio')
}

function sendSummary() {
  summarySent.value = true

  emit('summary', {
    correct: correctGuesses.value,
    wrong: wrongGuesses.value,
  })
}

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