import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Dashboard from '@/views/Dashboard.vue'
import { useFinanceStore } from '@/stores/finance'
import { useAuthStore } from '@/stores/auth'

describe('Dashboard View', () => {
  let wrapper
  let financeStore
  let authStore

  beforeEach(() => {
    setActivePinia(createPinia())
    financeStore = useFinanceStore()
    authStore = useAuthStore()

    // Mock de usuario autenticado
    authStore.user = {
      id: 1,
      email: 'test@example.com',
      full_name: 'Test User'
    }

    // Mock de datos financieros
    financeStore.accounts = [
      { id: 1, account_name: 'Checking', current_balance: 1000 },
      { id: 2, account_name: 'Savings', current_balance: 5000 }
    ]

    financeStore.financialOverview = {
      total_balance: 6000,
      monthly_income: 5000,
      monthly_expenses: 3000,
      savings_rate: 40
    }

    wrapper = mount(Dashboard, {
      global: {
        plugins: [createPinia()],
        stubs: {
          'router-link': true
        }
      }
    })
  })

  it('renderiza el dashboard correctamente', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('muestra el saludo al usuario', () => {
    expect(wrapper.text()).toContain('Test User' || 'Bienvenido')
  })

  it('muestra el balance total', () => {
    expect(wrapper.text()).toContain('6000' || '6,000')
  })

  it('muestra ingresos mensuales', () => {
    expect(wrapper.text()).toContain('5000' || '5,000')
  })

  it('muestra gastos mensuales', () => {
    expect(wrapper.text()).toContain('3000' || '3,000')
  })

  it('muestra la tasa de ahorro', () => {
    expect(wrapper.text()).toContain('40')
  })

  it('muestra el número de cuentas', () => {
    expect(wrapper.text()).toContain('2')
  })

  it('carga los datos al montar el componente', async () => {
    const fetchOverviewSpy = vi.spyOn(financeStore, 'fetchFinancialOverview')
    const fetchAccountsSpy = vi.spyOn(financeStore, 'fetchAccounts')

    const newWrapper = mount(Dashboard, {
      global: {
        plugins: [createPinia()]
      }
    })

    await newWrapper.vm.$nextTick()

    expect(fetchOverviewSpy).toHaveBeenCalled()
    expect(fetchAccountsSpy).toHaveBeenCalled()
  })

  it('muestra mensaje cuando no hay cuentas', () => {
    financeStore.accounts = []
    
    const newWrapper = mount(Dashboard, {
      global: {
        plugins: [createPinia()]
      }
    })

    expect(newWrapper.text()).toContain('No tienes cuentas' || 'Crear cuenta')
  })

  it('muestra enlaces de navegación rápida', () => {
    expect(wrapper.findAllComponents({ name: 'router-link' }).length).toBeGreaterThan(0)
  })
})
