<template>
  <div class="slot-page">
    <div class="slot-container">
      <div class="slot-machine">
        <h1 class="slot-title">🎰 SPIN TO WIN</h1>

        <div class="balance-info">
          <span class="game-balance">🎮 Game: ${{ authStore.user?.gameBalance?.toFixed(2) }}</span>
        </div>

        <div class="slot-reels">
          <div
            v-for="(symbol, index) in displaySymbols"
            :key="index"
            class="slot-reel"
            :class="{ spinning: isSpinning, win: showWin && result?.isWin }"
          >
            {{ symbol }}
          </div>
        </div>

        <div class="bet-controls">
          <span class="bet-label">Bet Amount:</span>
          <div class="bet-buttons">
            <button
              v-for="amount in betAmounts"
              :key="amount"
              class="bet-btn"
              :class="{ active: betAmount === amount }"
              @click="betAmount = amount"
              :disabled="isSpinning"
            >
              ${{ amount }}
            </button>
          </div>
        </div>

        <button
          class="spin-btn"
          @click="spin"
          :disabled="isSpinning || !canSpin"
        >
          {{ isSpinning ? 'Spinning...' : canSpin ? `SPIN ($${betAmount})` : 'Insufficient Game Balance' }}
        </button>

        <div
          v-if="result && showResult"
          class="result-message"
          :class="{ win: result.isWin, lose: !result.isWin }"
        >
          <template v-if="result.isWin">
            🎉 {{ result.multiplier }}x Win! +${{ result.payout.toFixed(2) }}
          </template>
          <template v-else>
            😢 No win! -${{ betAmount.toFixed(2) }}
          </template>
        </div>
      </div>

      <div class="card" style="margin-top: 24px; text-align: center;">
        <h3 style="margin-bottom: 16px;">💎 Payout Table</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; font-size: 0.9rem;">
          <div>🍒🍒🍒 = 2x</div>
          <div>🍋🍋🍋 = 3x</div>
          <div>🍊🍊🍊 = 5x</div>
          <div>🍇🍇🍇 = 10x</div>
          <div>💎💎💎 = 25x</div>
          <div>7️⃣7️⃣7️⃣ = 100x</div>
        </div>
        <p style="margin-top: 12px; color: var(--text-secondary); font-size: 0.85rem;">
          First 2 matching = 50% payout
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const authStore = useAuthStore()

const symbols = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣']
const betAmounts = [1, 5, 10, 25]
const betAmount = ref(1)
const isSpinning = ref(false)
const showWin = ref(false)
const showResult = ref(false)

interface SpinResult {
  symbols: string[]
  payout: number
  multiplier: number
  isWin: boolean
  gameBalance: number
  mainBalance: number
}

const result = ref<SpinResult | null>(null)
const displaySymbols = ref(['❓', '❓', '❓'])

const canSpin = computed(() => {
  return authStore.user && authStore.user.gameBalance >= betAmount.value
})

async function spin() {
  if (isSpinning.value || !canSpin.value) return

  isSpinning.value = true
  showResult.value = false
  showWin.value = false

  // Animate random symbols while spinning
  const spinInterval = setInterval(() => {
    displaySymbols.value = [
      symbols[Math.floor(Math.random() * symbols.length)],
      symbols[Math.floor(Math.random() * symbols.length)],
      symbols[Math.floor(Math.random() * symbols.length)]
    ]
  }, 100)

  try {
    const response = await api.post('/slot/spin', { betAmount: betAmount.value })
    result.value = response.data

    // Stop spinning after delay
    setTimeout(() => {
      clearInterval(spinInterval)
      displaySymbols.value = result.value!.symbols
      isSpinning.value = false
      showResult.value = true

      if (result.value!.isWin) {
        showWin.value = true
      }

      // Update both balances
      authStore.updateBalances(result.value!.gameBalance, result.value!.mainBalance)
    }, 1500)
  } catch (error) {
    clearInterval(spinInterval)
    isSpinning.value = false
    console.error('Spin error:', error)
  }
}
</script>

<style scoped>
.balance-info {
  margin-bottom: 16px;
}

.game-balance {
  padding: 8px 16px;
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border-radius: 8px;
  font-weight: 600;
}
</style>
