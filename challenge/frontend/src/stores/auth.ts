import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

interface User {
    id: number
    email: string
    gameBalance: number
    mainBalance: number
}

export const useAuthStore = defineStore('auth', () => {
    const token = ref<string | null>(localStorage.getItem('token'))
    const user = ref<User | null>(null)

    const isAuthenticated = computed(() => !!token.value)

    async function login(email: string, password: string) {
        const response = await api.post('/auth/login', { email, password })
        token.value = response.data.token
        user.value = response.data.user
        localStorage.setItem('token', response.data.token)
    }

    async function register(email: string, password: string) {
        const response = await api.post('/auth/register', { email, password })
        token.value = response.data.token
        user.value = response.data.user
        localStorage.setItem('token', response.data.token)
    }

    async function fetchUser() {
        if (!token.value) return
        try {
            const response = await api.get('/auth/me')
            user.value = response.data.user
        } catch (error) {
            logout()
        }
    }

    function updateBalances(gameBalance: number, mainBalance: number) {
        if (user.value) {
            user.value.gameBalance = gameBalance
            user.value.mainBalance = mainBalance
        }
    }

    function updateGameBalance(newBalance: number) {
        if (user.value) {
            user.value.gameBalance = newBalance
        }
    }

    function updateMainBalance(newBalance: number) {
        if (user.value) {
            user.value.mainBalance = newBalance
        }
    }

    function logout() {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
    }

    // Initialize
    if (token.value) {
        fetchUser()
    }

    return {
        token,
        user,
        isAuthenticated,
        login,
        register,
        fetchUser,
        updateBalances,
        updateGameBalance,
        updateMainBalance,
        logout
    }
})
