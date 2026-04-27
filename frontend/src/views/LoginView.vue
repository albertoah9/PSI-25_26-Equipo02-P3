<template>
  <main>
    <h1>Login</h1>

    <form @submit.prevent="handleLogin">
      <input
        v-model="username"
        type="text"
        placeholder="Username"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
      />

      <button type="submit">
        Login
      </button>
    </form>

    <p v-if="error">{{ error }}</p>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { loginUser } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  error.value = ''

  try {
    const data = await loginUser(username.value, password.value)

    authStore.setToken(data.auth_token)
    router.push('/')
  } catch (e) {
    error.value = e.message || 'Login failed'
  }
}
</script>
