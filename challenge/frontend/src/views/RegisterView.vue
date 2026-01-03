<template>
  <div class="auth-page">
    <div class="card auth-card">
      <h1 class="auth-title">🎰 Sign Up</h1>
      <p class="auth-subtitle">Create an account and start playing</p>

      <div v-if="error" class="error-message">{{ error }}</div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label class="form-label">Email</label>
          <input
            v-model="email"
            type="email"
            class="form-input"
            placeholder="your@email.com"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-input"
            placeholder="6+ characters"
            minlength="6"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">Confirm Password</label>
          <input
            v-model="passwordConfirm"
            type="password"
            class="form-input"
            placeholder="Re-enter password"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%" :disabled="loading">
          {{ loading ? 'Signing up...' : 'Sign Up' }}
        </button>
      </form>

      <div class="auth-footer">
        Already have an account? <router-link to="/login">Login</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''

  if (password.value !== passwordConfirm.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }

  loading.value = true

  try {
    await authStore.register(email.value, password.value)
    router.push('/slot')
  } catch (e: any) {
    error.value = e.response?.data?.error || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
