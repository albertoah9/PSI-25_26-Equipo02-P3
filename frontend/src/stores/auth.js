import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const token = ref(sessionStorage.getItem('auth_token') || '')

    const isAuthenticated = computed(() => token.value !== '')

    function setToken(newToken) {
        token.value = newToken
        sessionStorage.setItem('auth_token', newToken)
    }

    function clearToken() {
        token.value = ''
        sessionStorage.removeItem('auth_token')
    }

    return {
        token,
        isAuthenticated,
        setToken,
        clearToken,
    }
})