<template>
  <section class="lyrics-display">
    <div v-if="!lines.length">
      Loading lyrics...
    </div>

    <div
      v-for="line in visibleLines"
      :key="line.index"
      :class="['lyrics-line', { current: line.index === activeIndex }]"
    >
      <template v-if="line.index === activeIndex && line.missingWord && !solved[line.index]">
        {{ line.text.split('{')[0] }}

        <input
          data-cy="blankInput"
          v-model="currentInput"
          type="text"
          @keyup.enter="checkAnswer(line.index)"
        />

        {{ line.text.split('}')[1] }}

        <button
          data-cy="skip"
          type="button"
          class="skip-btn"
          @click="skip(line.index)"
        >
          Skip
        </button>
      </template>

      <template v-else>
        {{ renderLine(line) }}
      </template>
    </div>
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
  console.log('LRC URL:', props.song.lrc_file)

  const response = await fetch(props.song.lrc_file)

  console.log('LRC response status:', response.status)

  const text = await response.text()

  console.log('LRC text:', text)

  lines.value = parseLrc(text)

  console.log('Parsed lines:', lines.value)
}

function checkIfFinished() {
  const missingLines = lines.value
    .map((line, index) => ({ line, index }))
    .filter(({ line }) => line.missingWord)

  const allSolved = missingLines.every(({ index }) => solved.value[index])

  if (allSolved && !summarySent.value) {
    sendSummary()
  }
}

function parseLrc(text) {
  return text
    .split(/\r?\n/)
    .map((rawLine) => {
      const match = rawLine.match(/^\[(\d{1,2}):(\d{2})(?:[:.](\d{1,2}))?\](.*)$/)

      if (!match) return null

      const minutes = Number(match[1])
      const seconds = Number(match[2])
      const fraction = match[3] ? Number(`0.${match[3]}`) : 0
      const time = minutes * 60 + seconds + fraction
      const lyric = match[4].trim()

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
  if (activeIndex.value === -1) return []

  return lines.value
    .map((line, index) => ({ ...line, index }))
    .filter((line) => (
      line.index === activeIndex.value - 1 ||
      line.index === activeIndex.value ||
      line.index === activeIndex.value + 1
    ))
})

const pendingLineIndex = computed(() => {
  const previousIndex = currentIndex.value - 1

  if (previousIndex < 0) return -1

  const previousLine = lines.value[previousIndex]

  if (
    previousLine?.missingWord &&
    !solved.value[previousIndex]
  ) {
    return previousIndex
  }

  return -1
})

const activeIndex = computed(() => {
  return pendingLineIndex.value !== -1
    ? pendingLineIndex.value
    : currentIndex.value
})

watch(
  () => currentIndex.value,
  (newIndex, oldIndex) => {
    if (newIndex === -1) return

    const previousIndex = oldIndex

    if (previousIndex !== undefined && previousIndex !== -1) {
      const previousLine = lines.value[previousIndex]

      if (
        previousLine?.missingWord &&
        !solved.value[previousIndex]
      ) {
        currentInput.value = ''
        emit('stopAudio')
        return
      }
    }

    currentInput.value = ''

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
    checkIfFinished()
  } else {
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
  checkIfFinished()
}

function sendSummary() {
  summarySent.value = true

  const data = {
    correct: correctGuesses.value,
    wrong: wrongGuesses.value,
  }

  console.log('SUMMARY SENT:', data)

  emit('summary', data)
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
