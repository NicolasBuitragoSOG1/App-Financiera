<template>
  <div class="p-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Financial Analytics</h1>
      <p class="text-gray-600">Analyze your financial patterns and trends</p>
    </div>

    <!-- Time Period Selector -->
    <div class="card mb-6">
      <div class="flex items-center space-x-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Year</label>
          <select v-model="selectedYear" @change="loadMetrics" class="input-field">
            <option v-for="year in availableYears" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Month</label>
          <select v-model="selectedMonth" @change="loadMetrics" class="input-field">
            <option v-for="(month, index) in months" :key="index" :value="index + 1">
              {{ month }}
            </option>
          </select>
        </div>
        <div class="flex items-end">
          <button @click="loadMetrics" class="btn-primary">
            <ChartBarIcon class="w-5 h-5 mr-2" />
            Analyze
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Analytics Content -->
    <div v-else class="space-y-6">
      <!-- Key Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card">
          <div class="flex items-center">
            <div class="p-3 bg-green-100 rounded-lg">
              <ArrowUpIcon class="w-8 h-8 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Monthly Income</p>
              <p class="text-3xl font-bold text-gray-900">${{ formatCurrency(metrics.monthly_income || 0) }}</p>
              <p class="text-sm text-green-600">+{{ incomeGrowth }}% from last month</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-3 bg-red-100 rounded-lg">
              <ArrowDownIcon class="w-8 h-8 text-red-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Monthly Expenses</p>
              <p class="text-3xl font-bold text-gray-900">${{ formatCurrency(metrics.monthly_expenses || 0) }}</p>
              <p class="text-sm text-red-600">+{{ expenseGrowth }}% from last month</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-3 bg-blue-100 rounded-lg">
              <ChartBarIcon class="w-8 h-8 text-blue-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Savings Rate</p>
              <p class="text-3xl font-bold text-gray-900">{{ formatPercentage(metrics.savings_rate || 0) }}%</p>
              <p class="text-sm" :class="savingsRateChange >= 0 ? 'text-green-600' : 'text-red-600'">
                {{ savingsRateChange >= 0 ? '+' : '' }}{{ savingsRateChange }}% from last month
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Income vs Expenses Chart -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Income vs Expenses</h3>
          <div class="h-64">
            <canvas ref="incomeExpenseChart"></canvas>
          </div>
        </div>

        <!-- Expense Categories Chart -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Expense Categories</h3>
          <div class="h-64">
            <canvas ref="expenseCategoriesChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Detailed Analysis -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Monthly Trends -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Monthly Trends</h3>
          <div class="space-y-4">
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-sm font-medium text-gray-700">Net Income</span>
              <span class="text-lg font-bold" :class="netIncome >= 0 ? 'text-green-600' : 'text-red-600'">
                ${{ formatCurrency(Math.abs(netIncome)) }}
              </span>
            </div>
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-sm font-medium text-gray-700">Daily Average Spending</span>
              <span class="text-lg font-bold text-gray-900">
                ${{ formatCurrency(dailyAverageSpending) }}
              </span>
            </div>
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-sm font-medium text-gray-700">Largest Expense</span>
              <span class="text-lg font-bold text-red-600">
                ${{ formatCurrency(largestExpense) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Financial Health Score -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Financial Health Score</h3>
          <div class="text-center">
            <div class="relative w-32 h-32 mx-auto mb-4">
              <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  class="text-gray-300"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  class="text-primary-600"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="`${healthScore}, 100`"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-2xl font-bold text-gray-900">{{ healthScore }}/100</span>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-4">{{ getHealthScoreDescription(healthScore) }}</p>
            <div class="space-y-2 text-left">
              <div v-for="recommendation in healthRecommendations" :key="recommendation" 
                   class="flex items-start">
                <CheckCircleIcon class="w-4 h-4 text-green-500 mt-0.5 mr-2 flex-shrink-0" />
                <span class="text-sm text-gray-700">{{ recommendation }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Account Performance -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Account Performance</h3>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Account
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Platform
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Current Balance
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Monthly Change
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Performance
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="account in financeStore.accounts" :key="account.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ account.account_name }}</div>
                  <div class="text-sm text-gray-500 capitalize">{{ account.account_type }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ account.platform.name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  ${{ formatCurrency(account.current_balance) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <span class="text-green-600">+${{ formatCurrency(Math.random() * 500) }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Growing
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useFinanceStore } from '../stores/finance'
import {
  ChartBarIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const financeStore = useFinanceStore()

const isLoading = ref(false)
const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth() + 1)
const metrics = ref({})

const incomeExpenseChart = ref(null)
const expenseCategoriesChart = ref(null)

const months = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

const availableYears = computed(() => {
  const currentYear = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => currentYear - i)
})

const netIncome = computed(() => {
  return (metrics.value.monthly_income || 0) - (metrics.value.monthly_expenses || 0)
})

const dailyAverageSpending = computed(() => {
  const daysInMonth = new Date(selectedYear.value, selectedMonth.value, 0).getDate()
  return (metrics.value.monthly_expenses || 0) / daysInMonth
})

const largestExpense = computed(() => {
  // This would come from actual transaction data
  return Math.max(...financeStore.transactions
    .filter(t => t.transaction_type === 'expense')
    .map(t => t.amount)) || 0
})

const healthScore = computed(() => {
  let score = 50 // Base score
  
  // Savings rate contribution (0-30 points)
  const savingsRate = metrics.value.savings_rate || 0
  if (savingsRate >= 20) score += 30
  else if (savingsRate >= 10) score += 20
  else if (savingsRate >= 5) score += 10
  
  // Income vs expenses (0-20 points)
  if (netIncome.value > 0) score += 20
  else if (netIncome.value >= -100) score += 10
  
  // Account diversity (0-20 points)
  const accountTypes = new Set(financeStore.accounts.map(a => a.account_type))
  score += Math.min(accountTypes.size * 5, 20)
  
  // Goal progress (0-10 points)
  const activeGoals = financeStore.goals.filter(g => g.is_active)
  if (activeGoals.length > 0) {
    const avgProgress = activeGoals.reduce((sum, g) => sum + (g.current_amount / g.target_amount), 0) / activeGoals.length
    score += Math.min(avgProgress * 10, 10)
  }
  
  return Math.min(Math.max(score, 0), 100)
})

const healthRecommendations = computed(() => {
  const recommendations = []
  
  if ((metrics.value.savings_rate || 0) < 20) {
    recommendations.push('Increase your savings rate to at least 20%')
  }
  
  if (netIncome.value <= 0) {
    recommendations.push('Focus on reducing expenses or increasing income')
  }
  
  if (financeStore.goals.length === 0) {
    recommendations.push('Set specific financial goals to stay motivated')
  }
  
  const accountTypes = new Set(financeStore.accounts.map(a => a.account_type))
  if (accountTypes.size < 3) {
    recommendations.push('Diversify your accounts across different types')
  }
  
  return recommendations.slice(0, 3) // Show max 3 recommendations
})

// Mock data for growth calculations
const incomeGrowth = ref(5.2)
const expenseGrowth = ref(2.1)
const savingsRateChange = ref(1.3)

onMounted(async () => {
  await financeStore.initializeData()
  await loadMetrics()
})

const loadMetrics = async () => {
  isLoading.value = true
  try {
    const result = await financeStore.fetchMonthlyMetrics(selectedYear.value, selectedMonth.value)
    if (result) {
      metrics.value = result
    }
    
    await nextTick()
    createCharts()
  } catch (error) {
    console.error('Error loading metrics:', error)
  } finally {
    isLoading.value = false
  }
}

const createCharts = () => {
  // Income vs Expenses Chart
  if (incomeExpenseChart.value) {
    const ctx = incomeExpenseChart.value.getContext('2d')
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Income', 'Expenses', 'Net'],
        datasets: [{
          data: [
            metrics.value.monthly_income || 0,
            metrics.value.monthly_expenses || 0,
            netIncome.value
          ],
          backgroundColor: ['#10b981', '#ef4444', netIncome.value >= 0 ? '#10b981' : '#ef4444'],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return '$' + value.toLocaleString()
              }
            }
          }
        }
      }
    })
  }

  // Expense Categories Chart
  if (expenseCategoriesChart.value) {
    const ctx = expenseCategoriesChart.value.getContext('2d')
    
    // Group expenses by category
    const expensesByCategory = {}
    financeStore.transactions
      .filter(t => t.transaction_type === 'expense')
      .forEach(t => {
        expensesByCategory[t.category] = (expensesByCategory[t.category] || 0) + t.amount
      })

    const categories = Object.keys(expensesByCategory)
    const amounts = Object.values(expensesByCategory)

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: categories,
        datasets: [{
          data: amounts,
          backgroundColor: [
            '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6',
            '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6b7280'
          ]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  }
}

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

const getHealthScoreDescription = (score) => {
  if (score >= 80) return 'Excellent financial health!'
  if (score >= 60) return 'Good financial health'
  if (score >= 40) return 'Fair financial health'
  return 'Needs improvement'
}
</script>
