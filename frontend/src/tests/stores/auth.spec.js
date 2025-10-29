import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

vi.mock('axios')

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  describe('State', () => {
    it('inicia con estado por defecto', () => {
      const store = useAuthStore()
      expect(store.user).toBeNull()
      expect(store.token).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('login', () => {
    it('debe hacer login exitosamente', async () => {
      const store = useAuthStore()
      const mockResponse = {
        data: {
          access_token: 'test-token-123',
          token_type: 'bearer'
        }
      }
      
      axios.post.mockResolvedValueOnce(mockResponse)
      axios.get.mockResolvedValueOnce({
        data: {
          id: 1,
          email: 'test@example.com',
          full_name: 'Test User'
        }
      })

      await store.login('test@example.com', 'password123')

      expect(store.token).toBe('test-token-123')
      expect(store.isAuthenticated).toBe(true)
      expect(store.user).not.toBeNull()
      expect(localStorage.setItem).toHaveBeenCalledWith('token', 'test-token-123')
    })

    it('debe manejar errores de login', async () => {
      const store = useAuthStore()
      axios.post.mockRejectedValueOnce(new Error('Invalid credentials'))

      await expect(store.login('test@example.com', 'wrong')).rejects.toThrow()
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('register', () => {
    it('debe registrar usuario exitosamente', async () => {
      const store = useAuthStore()
      const mockUser = {
        id: 1,
        email: 'newuser@example.com',
        full_name: 'New User'
      }
      
      axios.post.mockResolvedValueOnce({ data: mockUser })

      const result = await store.register({
        email: 'newuser@example.com',
        password: 'password123',
        full_name: 'New User'
      })

      expect(result).toEqual(mockUser)
    })
  })

  describe('logout', () => {
    it('debe limpiar el estado al hacer logout', () => {
      const store = useAuthStore()
      store.token = 'test-token'
      store.user = { id: 1, email: 'test@example.com' }

      store.logout()

      expect(store.token).toBeNull()
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
      expect(localStorage.removeItem).toHaveBeenCalledWith('token')
    })
  })

  describe('loadUserFromToken', () => {
    it('debe cargar usuario desde localStorage', async () => {
      const store = useAuthStore()
      localStorage.getItem.mockReturnValueOnce('stored-token')
      axios.get.mockResolvedValueOnce({
        data: {
          id: 1,
          email: 'test@example.com',
          full_name: 'Test User'
        }
      })

      await store.loadUserFromToken()

      expect(store.token).toBe('stored-token')
      expect(store.user).not.toBeNull()
      expect(store.isAuthenticated).toBe(true)
    })

    it('debe manejar token inválido', async () => {
      const store = useAuthStore()
      localStorage.getItem.mockReturnValueOnce('invalid-token')
      axios.get.mockRejectedValueOnce(new Error('Unauthorized'))

      await store.loadUserFromToken()

      expect(store.token).toBeNull()
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })
  })
})
