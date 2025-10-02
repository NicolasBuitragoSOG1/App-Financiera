import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  const accounts = ref([])
  const transactions = ref([])
  const goals = ref([])
  const platforms = ref([])
  const overview = ref(null)
  const isLoading = ref(false)

  const totalBalance = computed(() => {
    return accounts.value.reduce((sum, account) => sum + account.current_balance, 0)
  })

  const accountsByPlatform = computed(() => {
    const grouped = {}
    accounts.value.forEach(account => {
      const platformName = account.platform.name
      if (!grouped[platformName]) {
        grouped[platformName] = {
          platform: account.platform,
          accounts: [],
          totalBalance: 0
        }
      }
      grouped[platformName].accounts.push(account)
      grouped[platformName].totalBalance += account.current_balance
    })
    return grouped
  })

  // Account operations
  const fetchAccounts = async () => {
    isLoading.value = true
    try {
      const response = await axios.get('/api/accounts')
      accounts.value = response.data
    } catch (error) {
      console.error('Error fetching accounts:', error)
    } finally {
      isLoading.value = false
    }
  }

  const createAccount = async (accountData) => {
    try {
      const response = await axios.post('/api/accounts', accountData)
      accounts.value.push(response.data)
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to create account' 
      }
    }
  }

  const updateAccountBalance = async (accountId, newBalance) => {
    try {
      await axios.put(`/api/accounts/${accountId}/balance`, { new_balance: newBalance })
      const account = accounts.value.find(a => a.id === accountId)
      if (account) {
        account.current_balance = newBalance
        account.last_updated = new Date().toISOString()
      }
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to update balance' 
      }
    }
  }

  // Transaction operations
  const fetchTransactions = async (limit = 50) => {
    try {
      const response = await axios.get(`/api/transactions?limit=${limit}`)
      transactions.value = response.data
    } catch (error) {
      console.error('Error fetching transactions:', error)
    }
  }

  const createTransaction = async (transactionData) => {
    try {
      const response = await axios.post('/api/transactions', transactionData)
      transactions.value.unshift(response.data)
      
      // Update account balance locally
      const account = accounts.value.find(a => a.id === transactionData.account_id)
      if (account) {
        if (transactionData.transaction_type === 'income') {
          account.current_balance += transactionData.amount
        } else if (transactionData.transaction_type === 'expense') {
          account.current_balance -= transactionData.amount
        }
      }
      
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to create transaction' 
      }
    }
  }

  // Goal operations
  const fetchGoals = async () => {
    try {
      const response = await axios.get('/api/goals')
      goals.value = response.data
    } catch (error) {
      console.error('Error fetching goals:', error)
    }
  }

  const createGoal = async (goalData) => {
    try {
      const response = await axios.post('/api/goals', goalData)
      goals.value.push(response.data)
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to create goal' 
      }
    }
  }

  const updateGoalProgress = async (goalId, currentAmount) => {
    try {
      await axios.put(`/api/goals/${goalId}/progress`, { current_amount: currentAmount })
      const goal = goals.value.find(g => g.id === goalId)
      if (goal) {
        goal.current_amount = currentAmount
      }
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to update goal progress' 
      }
    }
  }

  const updateGoal = async (goalId, goalData) => {
    try {
      const response = await axios.put(`/api/goals/${goalId}`, goalData)
      const goalIndex = goals.value.findIndex(g => g.id === goalId)
      if (goalIndex !== -1) {
        goals.value[goalIndex] = response.data
      }
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to update goal' 
      }
    }
  }

  const deleteGoal = async (goalId) => {
    try {
      await axios.delete(`/api/goals/${goalId}`)
      const goalIndex = goals.value.findIndex(g => g.id === goalId)
      if (goalIndex !== -1) {
        goals.value.splice(goalIndex, 1)
      }
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to delete goal' 
      }
    }
  }

  // Platform operations
  const fetchPlatforms = async () => {
    try {
      const response = await axios.get('/api/platforms')
      platforms.value = response.data
    } catch (error) {
      console.error('Error fetching platforms:', error)
    }
  }

  // Analytics operations
  const fetchOverview = async () => {
    isLoading.value = true
    try {
      const response = await axios.get('/api/analytics/overview')
      overview.value = response.data
    } catch (error) {
      console.error('Error fetching overview:', error)
    } finally {
      isLoading.value = false
    }
  }

  const fetchMonthlyMetrics = async (year, month) => {
    try {
      const response = await axios.get(`/api/analytics/monthly/${year}/${month}`)
      return response.data
    } catch (error) {
      console.error('Error fetching monthly metrics:', error)
      return null
    }
  }

  // Initialize data
  const initializeData = async () => {
    await Promise.all([
      fetchPlatforms(),
      fetchAccounts(),
      fetchTransactions(),
      fetchGoals(),
      fetchOverview()
    ])
  }

  return {
    accounts,
    transactions,
    goals,
    platforms,
    overview,
    isLoading,
    totalBalance,
    accountsByPlatform,
    fetchAccounts,
    createAccount,
    updateAccountBalance,
    fetchTransactions,
    createTransaction,
    fetchGoals,
    createGoal,
    updateGoal,
    updateGoalProgress,
    deleteGoal,
    fetchPlatforms,
    fetchOverview,
    fetchMonthlyMetrics,
    initializeData
  }
})
