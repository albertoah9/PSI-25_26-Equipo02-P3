<template>
  <div>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      |

      <RouterLink v-if="!auth.isAuthenticated" to="/log-in">
        Log In
      </RouterLink>

      <RouterLink v-else to="/log-out">
        Log Out
      </RouterLink>

      |
      <RouterLink to="/faq">FAQ</RouterLink>
      |
      <RouterLink to="/songs/1">Song 1</RouterLink>
    </nav>

    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
</script>