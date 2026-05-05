<template>
  <main>
    <div class="login-card">
      <h2>Login</h2>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <input
            data-cy="username"
            v-model="username"
            type="text"
            placeholder="Username"
          />
        </div>

        <div class="field">
          <input
            data-cy="password"
            v-model="password"
            type="password"
            placeholder="Password"
          />
        </div>

        <button type="submit">
          Login
        </button>
      </form>

      <p v-if="error" class="error">
        {{ error }}
      </p>
    </div>
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
