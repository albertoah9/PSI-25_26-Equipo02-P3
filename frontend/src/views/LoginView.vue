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

const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  error.value = ''

  try {
    const response = await fetch(
      'http://127.0.0.1:8000/api/v1/token/login/',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value
        })
      }
    )

    if (!response.ok) {
      throw new Error()
    }

    const data = await response.json()

    sessionStorage.setItem('token', data.auth_token)

    router.push('/')

  } catch (e) {
    error.value = 'Invalid username or password'
  }
}
</script>

