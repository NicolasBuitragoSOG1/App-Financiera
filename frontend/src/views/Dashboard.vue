<template>
  <div class="p-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Financial Dashboard</h1>
      <p class="text-gray-600 dark:text-gray-400">Welcome back, {{ authStore.user?.full_name }}!</p>
    </div>

    <!-- Loading State -->
    <div v-if="financeStore.isLoading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="space-y-6">
      <!-- Financial Overview Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="card">
          <div class="flex items-center">
            <div class="p-2 bg-green-100 rounded-lg">
              <CurrencyDollarIcon class="w-6 h-6 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Balance</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">${{ formatCurrency(financeStore.totalBalance) }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-2 bg-blue-100 rounded-lg">
              <ArrowUpIcon class="w-6 h-6 text-blue-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Income</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">${{ formatCurrency(financeStore.overview?.monthly_income || 0) }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-2 bg-red-100 rounded-lg">
              <ArrowDownIcon class="w-6 h-6 text-red-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Expenses</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">${{ formatCurrency(financeStore.overview?.monthly_expenses || 0) }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-2 bg-purple-100 rounded-lg">
              <ChartBarIcon class="w-6 h-6 text-purple-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Savings Rate</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatPercentage(financeStore.overview?.savings_rate || 0) }}%</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Accounts by Platform -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Accounts by Platform</h3>
          <div class="space-y-4">
            <div
              v-for="(platformData, platformName) in financeStore.accountsByPlatform"
              :key="platformName"
              class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
            >
              <div class="flex items-center">
                <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                  <span class="text-primary-600 font-semibold text-sm">
                    {{ platformName.charAt(0).toUpperCase() }}
                  </span>
                </div>
                <div class="ml-3">
                  <p class="font-medium text-gray-900 dark:text-white">{{ platformName }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">{{ platformData.accounts.length }} accounts</p>
                </div>
              </div>
              <div class="text-right">
                <p class="font-semibold text-gray-900 dark:text-white">${{ formatCurrency(platformData.totalBalance) }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400 capitalize">{{ platformData.platform.platform_type }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Transactions -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Recent Transactions</h3>
            <router-link to="/transactions" class="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 text-sm font-medium">
              View all
            </router-link>
          </div>
          <div class="space-y-3">
            <div
              v-for="transaction in financeStore.overview?.recent_transactions?.slice(0, 5) || []"
              :key="transaction.id"
              class="flex items-center justify-between"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full flex items-center justify-center"
                     :class="transaction.transaction_type === 'income' ? 'bg-green-100' : 'bg-red-100'">
                  <ArrowUpIcon v-if="transaction.transaction_type === 'income'" class="w-4 h-4 text-green-600" />
                  <ArrowDownIcon v-else class="w-4 h-4 text-red-600" />
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ transaction.description }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ transaction.category }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold"
                   :class="transaction.transaction_type === 'income' ? 'text-green-600' : 'text-red-600'">
                  {{ transaction.transaction_type === 'income' ? '+' : '-' }}${{ formatCurrency(transaction.amount) }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(transaction.transaction_date) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Financial Goals -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Financial Goals</h3>
          <router-link to="/goals" class="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 text-sm font-medium">
            Manage goals
          </router-link>
        </div>
        <div v-if="financeStore.overview?.active_goals?.length === 0" class="text-center py-8">
          <FlagIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p class="text-gray-500 dark:text-gray-400">No financial goals set yet</p>
          <router-link to="/goals" class="btn-primary mt-4 inline-block">
            Create your first goal
          </router-link>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="goal in financeStore.overview?.active_goals?.slice(0, 3) || []"
            :key="goal.id"
            class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-gray-900 dark:text-white">{{ goal.goal_name }}</h4>
              <span class="text-xs px-2 py-1 rounded-full"
                    :class="getPriorityClass(goal.priority)">
                {{ goal.priority }}
              </span>
            </div>
            <div class="mb-2">
              <div class="flex justify-between text-sm text-gray-600 dark:text-gray-300 mb-1">
                <span>${{ formatCurrency(goal.current_amount) }}</span>
                <span>${{ formatCurrency(goal.target_amount) }}</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                <div
                  class="bg-primary-600 h-2 rounded-full"
                  :style="{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }"
                ></div>
              </div>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ Math.round((goal.current_amount / goal.target_amount) * 100) }}% complete
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useFinanceStore } from '../stores/finance'
import {
  CurrencyDollarIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  ChartBarIcon,
  FlagIcon
} from '@heroicons/vue/24/outline'
import { format } from 'date-fns'

const authStore = useAuthStore()
const financeStore = useFinanceStore()

onMounted(() => {
  financeStore.initializeData()
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatPercentage = (value) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value)
}

const formatDate = (dateString) => {
  return format(new Date(dateString), 'MMM dd')
}

const getPriorityClass = (priority) => {
  switch (priority) {
    case 'high':
      return 'bg-red-100 text-red-800'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800'
    case 'low':
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}
</script>
