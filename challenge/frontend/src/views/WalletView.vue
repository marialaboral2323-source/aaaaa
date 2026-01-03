<template>
  <div class="wallet-page">
    <div class="wallet-container">
      <h1 class="wallet-title">💼 Wallet</h1>

      <!-- Dual Balance Display -->
      <div class="balance-section">
        <div class="wallet-balance card game-balance-card">
          <div class="balance-label">🎮 Game Balance</div>
          <div class="balance-value game">${{ authStore.user?.gameBalance?.toFixed(2) }}</div>
          <p class="balance-desc">Used for slots. Earned from Faucet.</p>
        </div>
        <div class="wallet-balance card main-balance-card">
          <div class="balance-label">💰 Main Balance</div>
          <div class="balance-value main">${{ authStore.user?.mainBalance?.toFixed(2) }}</div>
          <p class="balance-desc">Real Money! Withdraw from Game to transfer here.</p>
        </div>
      </div>

      <!-- Flag Progress -->
      <div class="card flag-progress-card" v-if="(authStore.user?.mainBalance || 0) < 1000000000">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: Math.min((authStore.user?.mainBalance || 0) / 10000000, 100) + '%' }"></div>
        </div>
        <span class="progress-text">Flag requires $1,000,000,000 in Main Balance</span>
      </div>

      <!-- Flag Section -->
      <div class="card flag-card" v-if="flagData">
        <div class="flag-content" :class="{ success: flagData.success }">
          <template v-if="flagData.success">
            <h2>Congratulations!</h2>
            <div class="flag-value">{{ flagData.flag }}</div>
          </template>
          <template v-else>
            <h3>To Get the Flag</h3>
            <p>{{ flagData.message }}</p>
          </template>
        </div>

        <div class="button-center-container">
          <button class="btn btn-gold btn-large" @click="checkFlag" :disabled="flagLoading">
            {{ flagLoading ? 'Processing...' : '🏆 Buy Flag' }}
          </button>
        </div>
      </div>

      <div class="wallet-actions">
        <!-- Faucet (Free USD → Game Balance) -->
        <div class="card action-card faucet-card">
          <h3>🚰 Daily USD</h3>
          <p class="action-desc">50 USD free per day → Game Balance</p>
          
          <div class="faucet-status" v-if="faucetStatus">
            <div class="status-badge" :class="{ available: faucetStatus.canClaim, claimed: !faucetStatus.canClaim }">
              {{ faucetStatus.canClaim ? '✅ Available' : '⏳ Come back tomorrow' }}
            </div>
          </div>

          <button
            class="btn btn-success btn-large"
            @click="claimFaucet"
            :disabled="faucetLoading || !faucetStatus?.canClaim"
          >
            {{ faucetLoading ? 'Processing...' : '🎁 Claim Daily USD' }}
          </button>

          <!-- Last Receipt -->
          <div class="receipt-section" v-if="lastReceipt">
            <div class="receipt-header">🧾 Last Receipt</div>
            <div class="receipt-content">
              <div class="receipt-row">
                <span class="receipt-label">Amount:</span>
                <span class="receipt-value">{{ lastReceipt.amount }} USD</span>
              </div>
              <div class="receipt-row">
                <span class="receipt-label">Signature (r):</span>
                <code class="receipt-value">{{ truncateKey(lastReceipt.signature.r) }}</code>
              </div>
              <div class="receipt-row">
                <span class="receipt-label">Signature (s):</span>
                <code class="receipt-value">{{ truncateKey(lastReceipt.signature.s) }}</code>
              </div>
              <button class="btn btn-outline" @click="viewFullReceipt">View Full Receipt</button>
            </div>
          </div>

          <div v-if="faucetMessage" class="action-message" :class="{ success: !faucetError, error: faucetError }">
            {{ faucetMessage }}
          </div>
        </div>

        <!-- Withdrawal (Game → Main Balance) -->
        <div class="card action-card withdraw-card">
          <h3>📤 Withdraw</h3>
          <p class="action-desc">Transfer Game Balance → Main Balance (requires signature)</p>
          <div class="form-group">
            <input
              v-model.number="withdrawAmount"
              type="number"
              class="form-input"
              placeholder="Amount to withdraw"
              min="1"
              :max="authStore.user?.gameBalance"
            />
          </div>
          <div class="form-group">
            <input
              v-model.number="withdrawAmount"
              type="number"
              class="form-input"
              placeholder="Amount to withdraw"
              min="1"
              :max="authStore.user?.gameBalance"
            />
          </div>
          <button
            class="btn btn-secondary"
            @click="requestWithdraw"
            :disabled="withdrawLoading || !withdrawAmount"
          >
            {{ withdrawLoading ? 'Processing...' : 'Transfer to Main Balance' }}
          </button>
          <div v-if="withdrawMessage" class="action-message" :class="{ error: withdrawError, success: !withdrawError }">
            {{ withdrawMessage }}
          </div>
        </div>
      </div>
      <div class="card transaction-history">
        <h3>📋 Transaction History</h3>
        <div v-if="transactions.length === 0" class="empty-state">
          No transactions yet
        </div>
        <div v-else class="tx-list">
          <div v-for="tx in transactions" :key="tx.id" class="tx-item">
            <div class="tx-type" :class="tx.type">
              {{ tx.type === 'deposit' ? '📥' : '📤' }}
              {{ tx.type === 'deposit' ? 'Faucet' : 'Withdraw' }}
            </div>
            <div class="tx-amount">{{ tx.amount.toFixed(2) }} USD</div>
            <div class="tx-signature" v-if="tx.sig_r">
              <code>r: {{ truncateKey(tx.sig_r) }}</code>
            </div>
            <div class="tx-status" :class="tx.status">{{ tx.status }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const authStore = useAuthStore()

// Faucet state
const faucetStatus = ref<{ canClaim: boolean; todayClaim: any; claims: any[] } | null>(null)
const faucetLoading = ref(false)
const faucetMessage = ref('')
const faucetError = ref(false)
const lastReceipt = ref<{ amount: number; message: string; msgHash: string; signature: { r: string; s: string }; timestamp: number } | null>(null)

// Flag state
const flagData = ref<{ success: boolean; message: string; flag?: string; gameBalance?: number; mainBalance?: number } | null>(null)
const flagLoading = ref(false)

// Withdraw state
const withdrawAmount = ref<number | null>(null)
const withdrawLoading = ref(false)
const withdrawMessage = ref('')
const withdrawError = ref(false)

const transactions = ref<any[]>([])

onMounted(async () => {
  await Promise.all([loadBalances(), loadTransactions(), loadFaucetStatus(), checkFlag()])
})

async function loadBalances() {
  try {
    const response = await api.get('/transaction/balance')
    authStore.updateBalances(response.data.gameBalance, response.data.mainBalance)
  } catch (error) {
    console.error('Failed to load balances:', error)
  }
}

async function loadFaucetStatus() {
  try {
    const response = await api.get('/transaction/faucet/status')
    faucetStatus.value = response.data
  } catch (error) {
    console.error('Failed to load faucet status:', error)
  }
}

async function claimFaucet() {
  faucetLoading.value = true
  faucetMessage.value = ''
  faucetError.value = false

  try {
    const response = await api.post('/transaction/faucet')
    faucetMessage.value = response.data.message
    lastReceipt.value = response.data.receipt
    authStore.updateBalances(response.data.gameBalance, response.data.mainBalance)
    await Promise.all([loadFaucetStatus(), loadTransactions()])
  } catch (error: any) {
    faucetError.value = true
    faucetMessage.value = error.response?.data?.error || 'An error occurred'
  } finally {
    faucetLoading.value = false
  }
}

async function checkFlag() {
  flagLoading.value = true
  try {
    const response = await api.get('/transaction/flag')
    flagData.value = response.data
  } catch (error) {
    console.error('Failed to check flag:', error)
  } finally {
    flagLoading.value = false
  }
}



async function loadTransactions() {
  try {
    const response = await api.get('/transaction/history')
    transactions.value = response.data.transactions
  } catch (error) {
    console.error('Failed to load transactions:', error)
  }
}

async function requestWithdraw() {
  if (!withdrawAmount.value) return
  withdrawLoading.value = true
  withdrawMessage.value = ''
  withdrawError.value = false

  try {
    const response = await api.post('/transaction/withdraw', {
      amount: withdrawAmount.value,
      timestamp: Date.now()
    })
    withdrawMessage.value = response.data.message
    authStore.updateBalances(response.data.gameBalance, response.data.mainBalance)
    withdrawAmount.value = null
    await loadTransactions()
  } catch (error: any) {
    withdrawError.value = true
    withdrawMessage.value = error.response?.data?.error || 'An error occurred'
  } finally {
    withdrawLoading.value = false
  }
}

function truncateKey(key: string): string {
  if (!key) return ''
  if (key.length <= 20) return key
  return `${key.slice(0, 10)}...${key.slice(-10)}`
}

function viewFullReceipt() {
  if (!lastReceipt.value) return
  const receiptData = JSON.stringify({
    amount: lastReceipt.value.amount,
    message: lastReceipt.value.message,
    msgHash: lastReceipt.value.msgHash,
    signature: {
      r: lastReceipt.value.signature.r,
      s: lastReceipt.value.signature.s
    },
    timestamp: lastReceipt.value.timestamp
  }, null, 2)
  alert(receiptData)
}


</script>

<style scoped>
.wallet-page {
  flex: 1;
  padding: 40px 20px;
}

.wallet-container {
  max-width: 900px;
  margin: 0 auto;
}

.wallet-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 24px;
}

/* Dual Balance Section */
.balance-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.wallet-balance {
  text-align: center;
  padding: 24px;
}

.game-balance-card {
  border: 2px solid #4caf50;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(0, 0, 0, 0) 100%);
}

.main-balance-card {
  border: 2px solid #ffc107;
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(0, 0, 0, 0) 100%);
}

.balance-label {
  color: var(--text-secondary);
  margin-bottom: 8px;
  font-size: 1.1rem;
}

.balance-value {
  font-size: 2rem;
  font-weight: 700;
}

.balance-value.game {
  color: #4caf50;
}

.balance-value.main {
  color: #ffc107;
}

.balance-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 8px;
}

/* Flag Progress */
.flag-progress-card {
  margin-bottom: 24px;
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--bg-secondary);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-purple), var(--accent-gold));
  transition: width 0.3s;
}

.progress-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 8px;
  display: block;
}

/* Flag Card */
.flag-card {
  margin-bottom: 24px;
  border: 2px solid var(--accent-gold);
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(0, 0, 0, 0) 100%);
}

.flag-content {
  text-align: center;
  margin-bottom: 16px;
}

.flag-content.success {
  color: var(--accent-green);
}

.flag-value {
  font-family: monospace;
  font-size: 1.2rem;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  margin-top: 16px;
  word-break: break-all;
}

.wallet-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.action-card h3 {
  margin-bottom: 8px;
}

.action-desc {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 16px;
}

/* Faucet Styles */
.faucet-card {
  border: 2px solid var(--accent-green);
}

/* Withdraw Styles */
.withdraw-card {
  border: 2px solid var(--accent-purple);
}

.faucet-status {
  margin-bottom: 16px;
}

.status-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 16px;
  font-size: 0.9rem;
  font-weight: 600;
}

.status-badge.available {
  background: rgba(76, 175, 80, 0.2);
  color: var(--accent-green);
}

.status-badge.claimed {
  background: rgba(255, 193, 7, 0.2);
  color: var(--accent-gold);
}

.btn-large {
  width: 100%;
  padding: 16px;
  font-size: 1.1rem;
}

/* Receipt styles */
.receipt-section {
  margin-top: 20px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.receipt-header {
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--accent-gold);
}

.receipt-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.receipt-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.receipt-label {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.receipt-value {
  font-family: monospace;
  font-size: 0.85rem;
  color: var(--text-primary);
}

.form-group {
  margin-bottom: 12px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.action-message {
  margin-top: 12px;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.9rem;
}

.action-message.success {
  background: rgba(76, 175, 80, 0.1);
  color: var(--accent-green);
}

.action-message.error {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}



.transaction-history {
  margin-bottom: 24px;
}

.tx-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tx-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 8px;
}

.tx-type {
  font-weight: 600;
}

.tx-type.deposit {
  color: var(--accent-green);
}

.tx-type.withdraw {
  color: var(--accent-gold);
}

.tx-amount {
  flex: 1;
}

.tx-signature {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.tx-signature code {
  font-family: monospace;
}

.tx-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.tx-status.approved {
  background: rgba(76, 175, 80, 0.2);
  color: var(--accent-green);
}

.tx-status.pending {
  background: rgba(255, 193, 7, 0.2);
  color: var(--accent-gold);
}

.empty-state {
  text-align: center;
  padding: 32px;
  color: var(--text-secondary);
}

.card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--border-color);
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
  color: white;
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-outline {
  background: transparent;
  color: var(--accent-purple);
  border: 1px solid var(--accent-purple);
  margin-top: 12px;
}

.btn-success {
  background: linear-gradient(135deg, #4caf50, #2e7d32);
  color: white;
  box-shadow: 0 4px 6px rgba(76, 175, 80, 0.3);
}

.btn-gold {
  background: linear-gradient(135deg, #ffc107, #ff9800);
  color: black;
  font-weight: 800;
  box-shadow: 0 4px 6px rgba(255, 193, 7, 0.3);
}

.button-center-container {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

@media (max-width: 600px) {
  .balance-section {
    grid-template-columns: 1fr;
  }
}
</style>
