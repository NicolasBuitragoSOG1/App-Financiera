import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useThemeStore } from '@/stores/theme'

describe('Theme Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  describe('State', () => {
    it('inicia con tema claro por defecto', () => {
      const store = useThemeStore()
      expect(store.isDark).toBe(false)
    })
  })

  describe('toggleTheme', () => {
    it('debe cambiar de tema claro a oscuro', () => {
      const store = useThemeStore()
      expect(store.isDark).toBe(false)

      store.toggleTheme()

      expect(store.isDark).toBe(true)
    })

    it('debe cambiar de tema oscuro a claro', () => {
      const store = useThemeStore()
      store.isDark = true

      store.toggleTheme()

      expect(store.isDark).toBe(false)
    })

    it('debe guardar preferencia en localStorage', () => {
      const store = useThemeStore()
      
      store.toggleTheme()

      expect(localStorage.setItem).toHaveBeenCalledWith('theme', 'dark')
    })
  })

  describe('setTheme', () => {
    it('debe establecer tema oscuro', () => {
      const store = useThemeStore()
      
      store.setTheme('dark')

      expect(store.isDark).toBe(true)
      expect(localStorage.setItem).toHaveBeenCalledWith('theme', 'dark')
    })

    it('debe establecer tema claro', () => {
      const store = useThemeStore()
      store.isDark = true
      
      store.setTheme('light')

      expect(store.isDark).toBe(false)
      expect(localStorage.setItem).toHaveBeenCalledWith('theme', 'light')
    })
  })

  describe('loadTheme', () => {
    it('debe cargar tema desde localStorage', () => {
      localStorage.getItem.mockReturnValueOnce('dark')
      const store = useThemeStore()
      
      store.loadTheme()

      expect(store.isDark).toBe(true)
    })

    it('debe usar tema claro si no hay preferencia guardada', () => {
      localStorage.getItem.mockReturnValueOnce(null)
      const store = useThemeStore()
      
      store.loadTheme()

      expect(store.isDark).toBe(false)
    })
  })

  describe('Computed Properties', () => {
    it('debe retornar el nombre del tema actual', () => {
      const store = useThemeStore()
      
      expect(store.currentTheme).toBe('light')
      
      store.isDark = true
      expect(store.currentTheme).toBe('dark')
    })
  })
})
