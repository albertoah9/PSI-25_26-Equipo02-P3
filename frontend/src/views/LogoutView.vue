<template>
  <main>
    <h1>Log Out</h1>
    <p>You have logged out succesfully</p>
    <p>Redirecting to Home in 5 seconds...</p>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  authStore.clearToken()

  setTimeout(() => {
    router.push('/')
  }, 5000)
})
</script>
