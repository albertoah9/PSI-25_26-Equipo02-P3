<template>
  <main>
    <div class="login-card">
      <h2>Log Out</h2>

      <p>You will be redirected to home in 5 seconds.</p>
    </div>
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
