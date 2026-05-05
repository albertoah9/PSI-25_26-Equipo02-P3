<template>
  <div class="app-shell">
    <header class="app-header">
      <RouterLink class="brand" to="/">🎶 Songs</RouterLink>

      <nav>
        <RouterLink data-cy="home-cypress-test" to="/">Home</RouterLink>

        <RouterLink
          v-if="!auth.isAuthenticated"
          data-cy="login-cypress-test"
          to="/log-in"
        >
          Log-In
        </RouterLink>

        <RouterLink
          v-else
          to="/log-out"
        >
          Log-Out
        </RouterLink>

        <RouterLink to="/faq">FAQ</RouterLink>
      </nav>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
</script>