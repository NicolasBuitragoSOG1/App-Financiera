<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Transactions</h1>
        <p class="text-gray-600">Track your income and expenses</p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary">
        <PlusIcon class="w-5 h-5 mr-2" />
        Add Transaction
      </button>
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
          <select v-model="filters.type" class="input-field">
            <option value="">All Types</option>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
            <option value="transfer">Transfer</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
          <select v-model="filters.category" class="input-field">
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Account</label>
          <select v-model="filters.account" class="input-field">
            <option value="">All Accounts</option>
            <option v-for="account in financeStore.accounts" :key="account.id" :value="account.id">
              {{ account.account_name }} - {{ account.platform.name }}
            </option>
          </select>
        </div>
        <div class="flex items-end">
          <button @click="clearFilters" class="btn-secondary w-full">
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Transactions Table -->
    <div class="card">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Description
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Category
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Account
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="transaction in filteredTransactions" :key="transaction.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatDate(transaction.transaction_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ transaction.description }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  {{ transaction.category }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ transaction.account.account_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getTypeClass(transaction.transaction_type)">
                  {{ transaction.transaction_type }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                  :class="getAmountClass(transaction.transaction_type)">
                {{ transaction.transaction_type === 'income' ? '+' : '-' }}${{ formatCurrency(transaction.amount) }}
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Empty State -->
        <div v-if="filteredTransactions.length === 0" class="text-center py-12">
          <ArrowsRightLeftIcon class="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">No transactions found</h3>
          <p class="text-gray-500 mb-6">Start tracking your finances by adding your first transaction</p>
          <button @click="showCreateModal = true" class="btn-primary">
            Add Transaction
          </button>
        </div>
      </div>
    </div>

    <!-- Create Transaction Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Add New Transaction</h3>
        
        <form @submit.prevent="createTransaction" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Account</label>
            <select v-model="newTransaction.account_id" required class="input-field">
              <option value="">Select an account</option>
              <option
                v-for="account in financeStore.accounts"
                :key="account.id"
                :value="account.id"
              >
                {{ account.account_name }} - {{ account.platform.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
            <select v-model="newTransaction.transaction_type" required class="input-field">
              <option value="">Select type</option>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
              <option value="transfer">Transfer</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select v-model="newTransaction.category" required class="input-field">
              <option value="">Select category</option>
              <option v-for="category in getCategories(newTransaction.transaction_type)" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Amount</label>
            <input
              v-model.number="newTransaction.amount"
              type="number"
              step="0.01"
              required
              class="input-field"
              placeholder="0.00"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <input
              v-model="newTransaction.description"
              type="text"
              required
              class="input-field"
              placeholder="Transaction description"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input
              v-model="newTransaction.transaction_date"
              type="datetime-local"
              required
              class="input-field"
            />
          </div>

          <div v-if="createError" class="text-red-600 text-sm">
            {{ createError }}
          </div>

          <div class="flex space-x-3 pt-4">
            <button type="submit" class="btn-primary flex-1">
              Add Transaction
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '../stores/finance'
import { useToast } from 'vue-toastification'
import {
  PlusIcon,
  ArrowsRightLeftIcon
} from '@heroicons/vue/24/outline'
import { format } from 'date-fns'

const financeStore = useFinanceStore()
const toast = useToast()

const showCreateModal = ref(false)
const createError = ref('')

const filters = ref({
  type: '',
  category: '',
  account: ''
})

const newTransaction = ref({
  account_id: '',
  transaction_type: '',
  category: '',
  amount: 0,
  description: '',
  transaction_date: new Date().toISOString().slice(0, 16)
})

const incomeCategories = [
  'Salary', 'Freelance', 'Investment', 'Business', 'Gift', 'Other Income'
]

const expenseCategories = [
  'Food & Dining', 'Transportation', 'Shopping', 'Entertainment', 'Bills & Utilities',
  'Healthcare', 'Education', 'Travel', 'Insurance', 'Other Expenses'
]

const transferCategories = [
  'Account Transfer', 'Investment', 'Savings', 'Other Transfer'
]

const categories = computed(() => {
  const allCategories = [...incomeCategories, ...expenseCategories, ...transferCategories]
  return [...new Set(allCategories)].sort()
})

const filteredTransactions = computed(() => {
  let filtered = financeStore.transactions

  if (filters.value.type) {
    filtered = filtered.filter(t => t.transaction_type === filters.value.type)
  }

  if (filters.value.category) {
    filtered = filtered.filter(t => t.category === filters.value.category)
  }

  if (filters.value.account) {
    filtered = filtered.filter(t => t.account_id === parseInt(filters.value.account))
  }

  return filtered
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
  return format(new Date(dateString), 'MMM dd, yyyy')
}

const getTypeClass = (type) => {
  switch (type) {
    case 'income':
      return 'bg-green-100 text-green-800'
    case 'expense':
      return 'bg-red-100 text-red-800'
    case 'transfer':
      return 'bg-blue-100 text-blue-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const getAmountClass = (type) => {
  switch (type) {
    case 'income':
      return 'text-green-600'
    case 'expense':
      return 'text-red-600'
    case 'transfer':
      return 'text-blue-600'
    default:
      return 'text-gray-900'
  }
}

const getCategories = (type) => {
  switch (type) {
    case 'income':
      return incomeCategories
    case 'expense':
      return expenseCategories
    case 'transfer':
      return transferCategories
    default:
      return []
  }
}

const clearFilters = () => {
  filters.value = {
    type: '',
    category: '',
    account: ''
  }
}

const createTransaction = async () => {
  createError.value = ''
  
  const result = await financeStore.createTransaction(newTransaction.value)
  
  if (result.success) {
    toast.success('Transaction added successfully!')
    cancelCreate()
  } else {
    createError.value = result.error
  }
}

const cancelCreate = () => {
  showCreateModal.value = false
  newTransaction.value = {
    account_id: '',
    transaction_type: '',
    category: '',
    amount: 0,
    description: '',
    transaction_date: new Date().toISOString().slice(0, 16)
  }
  createError.value = ''
}
</script>
