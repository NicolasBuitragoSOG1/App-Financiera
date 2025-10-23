import { ref, watch } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  // Initialize theme from localStorage or system preference
  const initTheme = () => {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      // Check system preference
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    applyTheme()
  }

  const applyTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      console.log('✓ Dark mode ENABLED - HTML classes:', document.documentElement.className)
    } else {
      document.documentElement.classList.remove('dark')
      console.log('✓ Light mode ENABLED - HTML classes:', document.documentElement.className)
    }
  }

  const toggleTheme = () => {
    isDark.value = !isDark.value
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
    console.log('🌓 Theme toggled to:', isDark.value ? 'DARK' : 'LIGHT')
    applyTheme()
  }

  // Watch for changes and apply
  watch(isDark, () => {
    applyTheme()
  })

  return {
    isDark,
    initTheme,
    toggleTheme
  }
})
