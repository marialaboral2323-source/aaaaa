<template>
  <div id="app">
    <nav class="nav" v-if="authStore.isAuthenticated">
      <div class="container nav-content">
        <router-link to="/slot" class="nav-logo">🎰 Avaritia</router-link>
        <div class="nav-links">
          <router-link to="/slot" class="nav-link">Game</router-link>
          <router-link to="/wallet" class="nav-link">Wallet</router-link>
          <router-link to="/mypage" class="nav-link">My Page</router-link>
          <div class="nav-balances">
            <span class="nav-balance game">🎮 ${{ authStore.user?.gameBalance?.toFixed(2) }}</span>
            <span class="nav-balance main">💰 ${{ authStore.user?.mainBalance?.toFixed(2) }}</span>
          </div>
          <button @click="logout" class="btn btn-secondary">Logout</button>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
.nav-balances {
  display: flex;
  gap: 8px;
}

.nav-balance {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
}

.nav-balance.game {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.nav-balance.main {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}
</style>
