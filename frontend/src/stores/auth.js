import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  // Set up axios interceptor
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  const login = async (email, password) => {
    isLoading.value = true
    try {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)

      const response = await axios.post('/api/login', formData)
      token.value = response.data.access_token
      localStorage.setItem('token', token.value)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      // Get user info
      await getCurrentUser()
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    isLoading.value = true
    try {
      await axios.post('/api/register', userData)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const getCurrentUser = async () => {
    try {
      const response = await axios.get('/api/me')
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  // Initialize user if token exists (commented out for now to avoid backend dependency)
  // if (token.value) {
  //   getCurrentUser()
  // }

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    getCurrentUser
  }
})
