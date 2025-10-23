<template>
  <div class="p-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Financial Analytics</h1>
      <p class="text-gray-600 dark:text-gray-400">Analyze your financial patterns and trends</p>
    </div>

    <!-- Time Period Selector -->
    <div class="card mb-6">
      <div class="flex items-center space-x-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Year</label>
          <select v-model="selectedYear" @change="loadMetrics" class="input-field">
            <option v-for="year in availableYears" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Month</label>
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
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Income</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">${{ formatCurrency(metrics.monthly_income || 0) }}</p>
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
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Expenses</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">${{ formatCurrency(metrics.monthly_expenses || 0) }}</p>
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
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Savings Rate</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ formatPercentage(metrics.savings_rate || 0) }}%</p>
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
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Income vs Expenses</h3>
          <div class="h-64">
            <canvas ref="incomeExpenseChart"></canvas>
          </div>
        </div>

        <!-- Expense Categories Chart -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Expense Categories</h3>
          <div class="h-64">
            <canvas ref="expenseCategoriesChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Detailed Analysis -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Monthly Trends -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Monthly Trends</h3>
          <div class="space-y-4">
            <div class="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Net Income</span>
              <span class="text-lg font-bold" :class="netIncome >= 0 ? 'text-green-600' : 'text-red-600'">
                ${{ formatCurrency(Math.abs(netIncome)) }}
              </span>
            </div>
            <div class="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Daily Average Spending</span>
              <span class="text-lg font-bold text-gray-900 dark:text-white">
                ${{ formatCurrency(dailyAverageSpending) }}
              </span>
            </div>
            <div class="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Largest Expense</span>
              <span class="text-lg font-bold text-red-600">
                ${{ formatCurrency(largestExpense) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Financial Health Score -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Financial Health Score</h3>
          <div class="text-center">
            <div class="relative w-32 h-32 mx-auto mb-4">
              <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  class="text-gray-300 dark:text-gray-600"
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
                <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ healthScore }}/100</span>
              </div>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">{{ getHealthScoreDescription(healthScore) }}</p>
            <div class="space-y-2 text-left">
              <div v-for="recommendation in healthRecommendations" :key="recommendation" 
                   class="flex items-start">
                <CheckCircleIcon class="w-4 h-4 text-green-500 mt-0.5 mr-2 flex-shrink-0" />
                <span class="text-sm text-gray-700 dark:text-gray-300">{{ recommendation }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Account Performance -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Account Performance</h3>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Account
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Platform
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Current Balance
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Monthly Change
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Performance
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="account in financeStore.accounts" :key="account.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white">{{ account.account_name }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400 capitalize">{{ account.account_type }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                  {{ account.platform.name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  ${{ formatCurrency(account.current_balance) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                  <span class="text-green-600">+${{ formatCurrency(Math.random() * 500) }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
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

let incomeExpenseChartInstance = null
let expenseCategoriesChartInstance = null

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
  console.log('Analytics component mounted')
  await financeStore.initializeData()
  console.log('Store initialized, transactions:', financeStore.transactions.length)
  await loadMetrics()
})

const loadMetrics = async () => {
  console.log('*** LOAD METRICS CALLED ***')
  console.log('Year:', selectedYear.value, 'Month:', selectedMonth.value)
  
  isLoading.value = true
  
  try {
    // Calculate metrics from transactions
    calculateMetricsFromTransactions()
    
    // IMPORTANT: Set loading to false BEFORE creating charts
    // so the v-else content (with canvas elements) becomes visible
    isLoading.value = false
    console.log('Loading set to false, waiting for DOM...')
    
    // Wait for DOM to update and canvas elements to appear
    await nextTick()
    
    // Additional delay to ensure canvas is fully rendered
    setTimeout(() => {
      console.log('DOM ready, creating charts now...')
      createCharts()
      console.log('*** CHARTS CREATION COMPLETE ***')
    }, 150)
    
  } catch (error) {
    console.error('Error in loadMetrics:', error)
    isLoading.value = false
  }
}

const calculateMetricsFromTransactions = () => {
  const startDate = new Date(selectedYear.value, selectedMonth.value - 1, 1)
  const endDate = new Date(selectedYear.value, selectedMonth.value, 0, 23, 59, 59)
  
  const monthTransactions = financeStore.transactions.filter(t => {
    const tDate = new Date(t.transaction_date)
    return tDate >= startDate && tDate <= endDate
  })
  
  const income = monthTransactions
    .filter(t => t.transaction_type === 'income')
    .reduce((sum, t) => sum + t.amount, 0)
  
  const expenses = monthTransactions
    .filter(t => t.transaction_type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0)
  
  metrics.value = {
    monthly_income: income,
    monthly_expenses: expenses,
    savings_rate: income > 0 ? ((income - expenses) / income * 100) : 0
  }
  
  console.log('Calculated metrics from transactions:', metrics.value)
}

const createCharts = () => {
  console.log('=== START CREATE CHARTS ===')
  console.log('Canvas refs - Income:', incomeExpenseChart.value, 'Categories:', expenseCategoriesChart.value)
  console.log('Metrics:', metrics.value)
  console.log('Transactions:', financeStore.transactions.length)
  
  try {
    // Destroy existing charts
    if (incomeExpenseChartInstance) {
      console.log('Destroying old income chart')
      incomeExpenseChartInstance.destroy()
      incomeExpenseChartInstance = null
    }
    if (expenseCategoriesChartInstance) {
      console.log('Destroying old categories chart')
      expenseCategoriesChartInstance.destroy()
      expenseCategoriesChartInstance = null
    }

    // Income vs Expenses Chart
    console.log('Creating Income vs Expenses chart...')
    if (incomeExpenseChart.value) {
      const ctx = incomeExpenseChart.value.getContext('2d')
      const income = metrics.value.monthly_income || 0
      const expenses = metrics.value.monthly_expenses || 0
      const net = income - expenses
      
      console.log('Chart data - Income:', income, 'Expenses:', expenses, 'Net:', net)
      
      const isDark = document.documentElement.classList.contains('dark')
      const textColor = isDark ? '#e5e7eb' : '#374151'
      const gridColor = isDark ? '#4b5563' : '#e5e7eb'
      
      incomeExpenseChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Income', 'Expenses', 'Net'],
          datasets: [{
            label: 'Amount',
            data: [income, expenses, Math.abs(net)],
            backgroundColor: [
              'rgba(16, 185, 129, 0.8)', 
              'rgba(239, 68, 68, 0.8)', 
              net >= 0 ? 'rgba(16, 185, 129, 0.8)' : 'rgba(239, 68, 68, 0.8)'
            ],
            borderColor: [
              'rgb(16, 185, 129)', 
              'rgb(239, 68, 68)', 
              net >= 0 ? 'rgb(16, 185, 129)' : 'rgb(239, 68, 68)'
            ],
            borderWidth: 2,
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            title: {
              display: true,
              text: `Monthly Overview (${months[selectedMonth.value - 1]} ${selectedYear.value})`,
              color: textColor,
              font: {
                size: 14,
                weight: 'normal'
              }
            }
          },
          scales: {
            x: {
              ticks: {
                color: textColor
              },
              grid: {
                color: gridColor
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: textColor,
                callback: function(value) {
                  return '$' + value.toLocaleString()
                }
              },
              grid: {
                color: gridColor
              }
            }
          }
        }
      })
      console.log('✓ Income vs Expenses chart created successfully!')
    } else {
      console.error('✗ Income expense chart canvas not found!')
    }

    // Expense Categories Chart
    if (expenseCategoriesChart.value) {
      const ctx = expenseCategoriesChart.value.getContext('2d')
      
      // Group ALL expenses by category (not filtered by month for better visualization)
      const expensesByCategory = {}
      const expenseTransactions = financeStore.transactions.filter(t => t.transaction_type === 'expense')
      
      if (expenseTransactions.length === 0) {
        console.warn('No expense transactions found')
        return
      }
      
      expenseTransactions.forEach(t => {
        if (t.category) {
          expensesByCategory[t.category] = (expensesByCategory[t.category] || 0) + parseFloat(t.amount)
        }
      })

      const categories = Object.keys(expensesByCategory)
      const amounts = Object.values(expensesByCategory)

      if (categories.length > 0) {
        const isDark = document.documentElement.classList.contains('dark')
        const textColor = isDark ? '#e5e7eb' : '#374151'
        const borderColor = isDark ? '#1f2937' : '#ffffff'
        
        expenseCategoriesChartInstance = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: categories,
            datasets: [{
              data: amounts,
              backgroundColor: [
                '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6',
                '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6b7280',
                '#0ea5e9', '#f43f5e', '#22c55e', '#eab308', '#a855f7'
              ],
              borderWidth: 2,
              borderColor: borderColor
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'right',
                labels: {
                  color: textColor,
                  padding: 10,
                  font: {
                    size: 11
                  }
                }
              },
              title: {
                display: true,
                text: 'Expense Distribution by Category',
                color: textColor,
                font: {
                  size: 14,
                  weight: 'normal'
                }
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const label = context.label || ''
                    const value = context.parsed || 0
                    const total = context.dataset.data.reduce((a, b) => a + b, 0)
                    const percentage = ((value / total) * 100).toFixed(1)
                    return label + ': $' + value.toFixed(2) + ' (' + percentage + '%)'
                  }
                }
              }
            }
          }
        })
        console.log('✓ Expense Categories chart created successfully!')
      } else {
        console.warn('⚠ No expense categories found')
      }
    } else {
      console.error('✗ Expense categories chart canvas not found!')
    }
    
    console.log('=== END CREATE CHARTS ===')
  } catch (error) {
    console.error('✗✗✗ ERROR CREATING CHARTS:', error)
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
