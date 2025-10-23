<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Accounts</h1>
        <p class="text-gray-600 dark:text-gray-400">Manage your financial accounts across different platforms</p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary">
        <PlusIcon class="w-5 h-5 mr-2" />
        Add Account
      </button>
    </div>

    <!-- Accounts Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="account in financeStore.accounts"
        :key="account.id"
        class="card hover:shadow-md transition-shadow"
      >
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <span class="text-primary-600 font-semibold">
                {{ account.platform.name.charAt(0).toUpperCase() }}
              </span>
            </div>
            <div class="ml-3">
              <h3 class="font-semibold text-gray-900 dark:text-white">{{ account.account_name }}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ account.platform.name }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="editAccount(account)"
              class="p-2 text-gray-400 hover:text-gray-600"
              title="Edit account"
            >
              <PencilIcon class="w-4 h-4" />
            </button>
            <button
              @click="deleteAccount(account)"
              class="p-2 text-red-400 hover:text-red-600"
              title="Delete account"
            >
              <TrashIcon class="w-4 h-4" />
            </button>
          </div>
        </div>

        <div class="space-y-2">
          <div class="flex justify-between">
            <span class="text-sm text-gray-600 dark:text-gray-400">Account Type</span>
            <span class="text-sm font-medium capitalize text-gray-900 dark:text-white">{{ account.account_type }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-gray-600 dark:text-gray-400">Account Number</span>
            <span class="text-sm font-mono text-gray-900 dark:text-white">****{{ account.account_number.slice(-4) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-gray-600 dark:text-gray-400">Currency</span>
            <span class="text-sm font-medium text-gray-900 dark:text-white">{{ account.currency }}</span>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">Current Balance</span>
            <span class="text-xl font-bold text-gray-900 dark:text-white">
              ${{ formatCurrency(account.current_balance) }}
            </span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Last updated: {{ formatDate(account.last_updated) }}
          </p>
        </div>

        <button
          @click="updateBalance(account)"
          class="w-full mt-4 btn-secondary text-sm"
        >
          Update Balance
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="financeStore.accounts.length === 0" class="col-span-full">
        <div class="text-center py-12">
          <CreditCardIcon class="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No accounts yet</h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6">Get started by adding your first financial account</p>
          <button @click="showCreateModal = true" class="btn-primary">
            Add Your First Account
          </button>
        </div>
      </div>
    </div>

    <!-- Create Account Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Add New Account</h3>
        
        <form @submit.prevent="createAccount" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Platform</label>
            <select v-model="newAccount.platform_id" required class="input-field">
              <option value="">Select a platform</option>
              <option
                v-for="platform in financeStore.platforms"
                :key="platform.id"
                :value="platform.id"
              >
                {{ platform.name }} ({{ platform.platform_type }})
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Name</label>
            <input
              v-model="newAccount.account_name"
              type="text"
              required
              class="input-field"
              placeholder="e.g., Main Checking"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Type</label>
            <select v-model="newAccount.account_type" required class="input-field">
              <option value="">Select type</option>
              <option value="checking">Checking</option>
              <option value="savings">Savings</option>
              <option value="credit">Credit</option>
              <option value="investment">Investment</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Number</label>
            <input
              v-model="newAccount.account_number"
              type="text"
              required
              class="input-field"
              placeholder="Account number"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Current Balance</label>
            <input
              v-model.number="newAccount.current_balance"
              type="number"
              step="0.01"
              required
              class="input-field"
              placeholder="0.00"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Currency</label>
            <select v-model="newAccount.currency" class="input-field">
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="GBP">GBP</option>
            </select>
          </div>

          <div v-if="createError" class="text-red-600 dark:text-red-400 text-sm">
            {{ createError }}
          </div>

          <div class="flex space-x-3 pt-4">
            <button type="submit" class="btn-primary flex-1">
              Create Account
            </button>
            <button
              type="button"
              @click="cancelCreate"
              class="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Account Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Edit Account</h3>
        
        <form @submit.prevent="saveEditAccount" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Platform</label>
            <select v-model="editAccountData.platform_id" required class="input-field">
              <option value="">Select a platform</option>
              <option
                v-for="platform in financeStore.platforms"
                :key="platform.id"
                :value="platform.id"
              >
                {{ platform.name }} ({{ platform.platform_type }})
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Name</label>
            <input
              v-model="editAccountData.account_name"
              type="text"
              required
              class="input-field"
              placeholder="e.g., Main Checking"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Type</label>
            <select v-model="editAccountData.account_type" required class="input-field">
              <option value="">Select type</option>
              <option value="checking">Checking</option>
              <option value="savings">Savings</option>
              <option value="credit">Credit</option>
              <option value="investment">Investment</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Number</label>
            <input
              v-model="editAccountData.account_number"
              type="text"
              required
              class="input-field"
              placeholder="Account number"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Current Balance</label>
            <input
              v-model.number="editAccountData.current_balance"
              type="number"
              step="0.01"
              required
              class="input-field"
              placeholder="0.00"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Currency</label>
            <select v-model="editAccountData.currency" class="input-field">
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="GBP">GBP</option>
            </select>
          </div>

          <div v-if="editError" class="text-red-600 dark:text-red-400 text-sm">
            {{ editError }}
          </div>

          <div class="flex space-x-3 pt-4">
            <button type="submit" class="btn-primary flex-1">
              Save Changes
            </button>
            <button
              type="button"
              @click="cancelEdit"
              class="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Update Balance Modal -->
    <div v-if="showUpdateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Update Balance</h3>
        
        <div class="mb-4">
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ selectedAccount?.account_name }}</p>
          <p class="text-lg font-semibold text-gray-900 dark:text-white">Current: ${{ formatCurrency(selectedAccount?.current_balance || 0) }}</p>
        </div>

        <form @submit.prevent="saveBalance" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">New Balance</label>
            <input
              v-model.number="newBalance"
              type="number"
              step="0.01"
              required
              class="input-field"
              placeholder="0.00"
            />
          </div>

          <div v-if="updateError" class="text-red-600 dark:text-red-400 text-sm">
            {{ updateError }}
          </div>

          <div class="flex space-x-3 pt-4">
            <button type="submit" class="btn-primary flex-1">
              Update Balance
            </button>
            <button
              type="button"
              @click="cancelUpdate"
              class="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useFinanceStore } from '../stores/finance'
import { useToast } from 'vue-toastification'
import {
  PlusIcon,
  CreditCardIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import { format } from 'date-fns'

const financeStore = useFinanceStore()
const toast = useToast()

const showCreateModal = ref(false)
const showUpdateModal = ref(false)
const showEditModal = ref(false)
const selectedAccount = ref(null)
const createError = ref('')
const updateError = ref('')
const editError = ref('')

const newAccount = ref({
  platform_id: '',
  account_name: '',
  account_type: '',
  account_number: '',
  current_balance: 0,
  currency: 'USD'
})

const newBalance = ref(0)

const editAccountData = ref({
  id: null,
  platform_id: '',
  account_name: '',
  account_type: '',
  account_number: '',
  current_balance: 0,
  currency: 'USD'
})

onMounted(() => {
  financeStore.initializeData()
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatDate = (dateString) => {
  return format(new Date(dateString), 'MMM dd, yyyy HH:mm')
}

const createAccount = async () => {
  createError.value = ''
  
  const result = await financeStore.createAccount(newAccount.value)
  
  if (result.success) {
    toast.success('Account created successfully!')
    cancelCreate()
  } else {
    createError.value = result.error
  }
}

const cancelCreate = () => {
  showCreateModal.value = false
  newAccount.value = {
    platform_id: '',
    account_name: '',
    account_type: '',
    account_number: '',
    current_balance: 0,
    currency: 'USD'
  }
  createError.value = ''
}

const updateBalance = (account) => {
  selectedAccount.value = account
  newBalance.value = account.current_balance
  showUpdateModal.value = true
}

const saveBalance = async () => {
  updateError.value = ''
  
  const result = await financeStore.updateAccountBalance(selectedAccount.value.id, newBalance.value)
  
  if (result.success) {
    toast.success('Balance updated successfully!')
    cancelUpdate()
  } else {
    updateError.value = result.error
  }
}

const cancelUpdate = () => {
  showUpdateModal.value = false
  selectedAccount.value = null
  newBalance.value = 0
  updateError.value = ''
}

const editAccount = (account) => {
  selectedAccount.value = account
  editAccountData.value = {
    id: account.id,
    platform_id: account.platform_id,
    account_name: account.account_name,
    account_type: account.account_type,
    account_number: account.account_number,
    current_balance: account.current_balance,
    currency: account.currency
  }
  showEditModal.value = true
}

const saveEditAccount = async () => {
  editError.value = ''
  
  const result = await financeStore.updateAccount(editAccountData.value.id, editAccountData.value)
  
  if (result.success) {
    toast.success('Account updated successfully!')
    cancelEdit()
  } else {
    editError.value = result.error
  }
}

const cancelEdit = () => {
  showEditModal.value = false
  selectedAccount.value = null
  editAccountData.value = {
    id: null,
    platform_id: '',
    account_name: '',
    account_type: '',
    account_number: '',
    current_balance: 0,
    currency: 'USD'
  }
  editError.value = ''
}

const deleteAccount = async (account) => {
  if (confirm(`Are you sure you want to delete "${account.account_name}"? This action cannot be undone.`)) {
    const result = await financeStore.deleteAccount(account.id)
    
    if (result.success) {
      toast.success('Account deleted successfully!')
    } else {
      toast.error(result.error || 'Failed to delete account')
    }
  }
}
</script>
