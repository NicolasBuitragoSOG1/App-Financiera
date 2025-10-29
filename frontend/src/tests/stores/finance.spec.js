import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useFinanceStore } from '@/stores/finance'
import axios from 'axios'

vi.mock('axios')

describe('Finance Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('Accounts', () => {
    it('debe obtener cuentas del usuario', async () => {
      const store = useFinanceStore()
      const mockAccounts = [
        { id: 1, account_name: 'Checking', current_balance: 1000 },
        { id: 2, account_name: 'Savings', current_balance: 5000 }
      ]
      
      axios.get.mockResolvedValueOnce({ data: mockAccounts })

      await store.fetchAccounts()

      expect(store.accounts).toEqual(mockAccounts)
      expect(store.accounts.length).toBe(2)
    })

    it('debe crear nueva cuenta', async () => {
      const store = useFinanceStore()
      const newAccount = {
        id: 3,
        account_name: 'Investment',
        current_balance: 10000
      }
      
      axios.post.mockResolvedValueOnce({ data: newAccount })
      axios.get.mockResolvedValueOnce({ data: [newAccount] })

      await store.createAccount({
        account_name: 'Investment',
        current_balance: 10000
      })

      expect(axios.post).toHaveBeenCalled()
    })

    it('debe eliminar cuenta', async () => {
      const store = useFinanceStore()
      store.accounts = [
        { id: 1, account_name: 'Checking', current_balance: 1000 }
      ]
      
      axios.delete.mockResolvedValueOnce({ data: {} })

      await store.deleteAccount(1)

      expect(axios.delete).toHaveBeenCalledWith(
        expect.stringContaining('/api/accounts/1'),
        expect.any(Object)
      )
    })
  })

  describe('Transactions', () => {
    it('debe obtener transacciones del usuario', async () => {
      const store = useFinanceStore()
      const mockTransactions = [
        { id: 1, transaction_type: 'income', amount: 1000 },
        { id: 2, transaction_type: 'expense', amount: 500 }
      ]
      
      axios.get.mockResolvedValueOnce({ data: mockTransactions })

      await store.fetchTransactions()

      expect(store.transactions).toEqual(mockTransactions)
      expect(store.transactions.length).toBe(2)
    })

    it('debe crear nueva transacción', async () => {
      const store = useFinanceStore()
      const newTransaction = {
        id: 3,
        transaction_type: 'income',
        amount: 2000
      }
      
      axios.post.mockResolvedValueOnce({ data: newTransaction })
      axios.get.mockResolvedValueOnce({ data: [newTransaction] })

      await store.createTransaction({
        transaction_type: 'income',
        amount: 2000
      })

      expect(axios.post).toHaveBeenCalled()
    })

    it('debe filtrar transacciones por tipo', () => {
      const store = useFinanceStore()
      store.transactions = [
        { id: 1, transaction_type: 'income', amount: 1000 },
        { id: 2, transaction_type: 'expense', amount: 500 },
        { id: 3, transaction_type: 'income', amount: 1500 }
      ]

      const incomeTransactions = store.getTransactionsByType('income')

      expect(incomeTransactions.length).toBe(2)
      expect(incomeTransactions[0].transaction_type).toBe('income')
    })
  })

  describe('Goals', () => {
    it('debe obtener metas financieras', async () => {
      const store = useFinanceStore()
      const mockGoals = [
        { id: 1, goal_name: 'Emergency Fund', target_amount: 10000 },
        { id: 2, goal_name: 'Vacation', target_amount: 5000 }
      ]
      
      axios.get.mockResolvedValueOnce({ data: mockGoals })

      await store.fetchGoals()

      expect(store.goals).toEqual(mockGoals)
      expect(store.goals.length).toBe(2)
    })

    it('debe crear nueva meta', async () => {
      const store = useFinanceStore()
      const newGoal = {
        id: 3,
        goal_name: 'Car Fund',
        target_amount: 20000
      }
      
      axios.post.mockResolvedValueOnce({ data: newGoal })
      axios.get.mockResolvedValueOnce({ data: [newGoal] })

      await store.createGoal({
        goal_name: 'Car Fund',
        target_amount: 20000
      })

      expect(axios.post).toHaveBeenCalled()
    })

    it('debe actualizar progreso de meta', async () => {
      const store = useFinanceStore()
      const updatedGoal = {
        id: 1,
        goal_name: 'Emergency Fund',
        current_amount: 5000
      }
      
      axios.patch.mockResolvedValueOnce({ data: updatedGoal })
      axios.get.mockResolvedValueOnce({ data: [updatedGoal] })

      await store.updateGoalProgress(1, 5000)

      expect(axios.patch).toHaveBeenCalled()
    })
  })

  describe('Analytics', () => {
    it('debe obtener overview financiero', async () => {
      const store = useFinanceStore()
      const mockOverview = {
        total_balance: 15000,
        monthly_income: 5000,
        monthly_expenses: 3000,
        savings_rate: 40
      }
      
      axios.get.mockResolvedValueOnce({ data: mockOverview })

      await store.fetchFinancialOverview()

      expect(store.financialOverview).toEqual(mockOverview)
    })

    it('debe calcular balance total', () => {
      const store = useFinanceStore()
      store.accounts = [
        { current_balance: 1000 },
        { current_balance: 5000 },
        { current_balance: 3000 }
      ]

      expect(store.totalBalance).toBe(9000)
    })

    it('debe calcular ingresos mensuales', () => {
      const store = useFinanceStore()
      const today = new Date()
      store.transactions = [
        {
          transaction_type: 'income',
          amount: 1000,
          transaction_date: today.toISOString()
        },
        {
          transaction_type: 'income',
          amount: 2000,
          transaction_date: today.toISOString()
        },
        {
          transaction_type: 'expense',
          amount: 500,
          transaction_date: today.toISOString()
        }
      ]

      expect(store.monthlyIncome).toBe(3000)
    })

    it('debe calcular gastos mensuales', () => {
      const store = useFinanceStore()
      const today = new Date()
      store.transactions = [
        {
          transaction_type: 'expense',
          amount: 500,
          transaction_date: today.toISOString()
        },
        {
          transaction_type: 'expense',
          amount: 300,
          transaction_date: today.toISOString()
        }
      ]

      expect(store.monthlyExpenses).toBe(800)
    })
  })

  describe('Error Handling', () => {
    it('debe manejar errores al obtener cuentas', async () => {
      const store = useFinanceStore()
      axios.get.mockRejectedValueOnce(new Error('Network error'))

      await expect(store.fetchAccounts()).rejects.toThrow()
    })

    it('debe manejar errores al crear transacción', async () => {
      const store = useFinanceStore()
      axios.post.mockRejectedValueOnce(new Error('Insufficient balance'))

      await expect(
        store.createTransaction({ transaction_type: 'expense', amount: 10000 })
      ).rejects.toThrow()
    })
  })
})
