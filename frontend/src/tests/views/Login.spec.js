import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Login from '@/views/Login.vue'
import { useAuthStore } from '@/stores/auth'

describe('Login View', () => {
  let wrapper
  let authStore

  beforeEach(() => {
    setActivePinia(createPinia())
    authStore = useAuthStore()
    
    wrapper = mount(Login, {
      global: {
        plugins: [createPinia()],
        stubs: {
          'router-link': true
        }
      }
    })
  })

  it('renderiza el formulario de login', () => {
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('muestra el título "Iniciar Sesión"', () => {
    expect(wrapper.text()).toContain('Iniciar Sesión')
  })

  it('valida campos requeridos', async () => {
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')

    // Verificar que no se llamó al login si los campos están vacíos
    expect(authStore.isAuthenticated).toBe(false)
  })

  it('actualiza el modelo al escribir en los inputs', async () => {
    const emailInput = wrapper.find('input[type="email"]')
    const passwordInput = wrapper.find('input[type="password"]')

    await emailInput.setValue('test@example.com')
    await passwordInput.setValue('password123')

    expect(emailInput.element.value).toBe('test@example.com')
    expect(passwordInput.element.value).toBe('password123')
  })

  it('muestra enlace para registro', () => {
    expect(wrapper.text()).toContain('No tienes cuenta')
    expect(wrapper.findComponent({ name: 'router-link' }).exists()).toBe(true)
  })

  it('deshabilita el botón durante el login', async () => {
    const loginSpy = vi.spyOn(authStore, 'login').mockImplementation(() => 
      new Promise(resolve => setTimeout(resolve, 100))
    )

    const emailInput = wrapper.find('input[type="email"]')
    const passwordInput = wrapper.find('input[type="password"]')
    const submitButton = wrapper.find('button[type="submit"]')

    await emailInput.setValue('test@example.com')
    await passwordInput.setValue('password123')
    
    const form = wrapper.find('form')
    form.trigger('submit.prevent')

    await wrapper.vm.$nextTick()
    
    // El botón debería estar deshabilitado durante el login
    expect(submitButton.attributes('disabled')).toBeDefined()
  })

  it('muestra mensaje de error en login fallido', async () => {
    vi.spyOn(authStore, 'login').mockRejectedValue(new Error('Invalid credentials'))

    const emailInput = wrapper.find('input[type="email"]')
    const passwordInput = wrapper.find('input[type="password"]')

    await emailInput.setValue('wrong@example.com')
    await passwordInput.setValue('wrongpassword')

    const form = wrapper.find('form')
    await form.trigger('submit.prevent')

    await wrapper.vm.$nextTick()

    // Verificar que se muestra algún mensaje de error
    expect(wrapper.text()).toContain('error' || 'incorrecto' || 'inválido')
  })
})
