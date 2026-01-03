<template>
  <div class="mypage">
    <div class="mypage-container">
      <h1 class="mypage-title">📊 My Page</h1>

      <div v-if="loading" class="card" style="text-align: center; padding: 40px;">
        Loading...
      </div>

      <template v-else-if="stats">
        <div class="stats-grid">
          <div class="stat-card game">
            <div class="stat-label">🎮 Game Balance</div>
            <div class="stat-value">${{ stats.user.gameBalance.toFixed(2) }}</div>
          </div>
          <div class="stat-card main">
            <div class="stat-label">💰 Main Balance</div>
            <div class="stat-value">${{ stats.user.mainBalance.toFixed(2) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Total Games</div>
            <div class="stat-value">{{ stats.stats.totalGames }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Total Bet</div>
            <div class="stat-value">${{ stats.stats.totalBet.toFixed(2) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Total Payout</div>
            <div class="stat-value">${{ stats.stats.totalPayout.toFixed(2) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Net Profit/Loss</div>
            <div
              class="stat-value"
              :class="{ positive: stats.stats.totalProfit >= 0, negative: stats.stats.totalProfit < 0 }"
            >
              {{ stats.stats.totalProfit >= 0 ? '+' : '' }}${{ stats.stats.totalProfit.toFixed(2) }}
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-label">ROI</div>
            <div
              class="stat-value"
              :class="{ positive: parseFloat(stats.stats.roi) >= 0, negative: parseFloat(stats.stats.roi) < 0 }"
            >
              {{ stats.stats.roi }}
            </div>
          </div>
        </div>

        <div class="recent-games">
          <h3>🎮 Recent Games</h3>

          <div v-if="stats.recentGames.length === 0" class="empty-state">
            No games yet. Try the slot machine!
          </div>

          <div v-else class="game-list">
            <div
              v-for="game in stats.recentGames"
              :key="game.id"
              class="game-item"
            >
              <div class="game-symbols">
                <span v-for="(symbol, i) in game.symbols" :key="i">{{ symbol }}</span>
              </div>
              <div class="game-result">
                <div class="game-bet">Bet: ${{ game.bet_amount.toFixed(2) }}</div>
                <div
                  class="game-payout"
                  :class="{ positive: game.payout > game.bet_amount, negative: game.payout <= game.bet_amount }"
                >
                  {{ game.payout > game.bet_amount ? '+' : '' }}${{ (game.payout - game.bet_amount).toFixed(2) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

interface Stats {
  user: {
    id: number
    email: string
    gameBalance: number
    mainBalance: number
    createdAt: string
  }
  stats: {
    totalGames: number
    totalBet: number
    totalPayout: number
    totalProfit: number
    roi: string
  }
  recentGames: {
    id: number
    bet_amount: number
    symbols: string[]
    payout: number
    created_at: string
  }[]
}

const loading = ref(true)
const stats = ref<Stats | null>(null)

onMounted(async () => {
  try {
    const response = await api.get('/user/stats')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load stats:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stat-card.game {
  border: 2px solid #4caf50;
  background: rgba(76, 175, 80, 0.1);
}

.stat-card.game .stat-value {
  color: #4caf50;
}

.stat-card.main {
  border: 2px solid #ffc107;
  background: rgba(255, 193, 7, 0.1);
}

.stat-card.main .stat-value {
  color: #ffc107;
}
</style>
