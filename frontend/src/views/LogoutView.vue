<template>
  <main>
    <h1>Logout</h1>
    <p>You have logged out successfully.</p>
    <p>Redirecting to Home in 5 seconds...</p>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(async () => {
  const token = sessionStorage.getItem('token')

  try {
    if (token) {
      await fetch('http://127.0.0.1:8000/api/v1/token/logout/', {
        method: 'POST',
        headers: {
          Authorization: `Token ${token}`
        }
      })
    }
  } catch (e) {
    console.error(e)
  }

  sessionStorage.removeItem('token')

  setTimeout(() => {
    router.push('/')
  }, 5000)
})
</script>

