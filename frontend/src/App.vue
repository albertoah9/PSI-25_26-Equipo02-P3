<script setup></script>

<template>
  <div>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      |
      <RouterLink to="/log-in">Log In</RouterLink>
      |
      <RouterLink to="/log-out">Log Out</RouterLink>
      |
      <RouterLink to="/faq">FAQ</RouterLink>
      |
      <RouterLink to="/songs/1">Song 1</RouterLink>
    </nav>

    <RouterView /> <!-- Aquí se renderiza la vista qye esté activa -->
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped></style>
