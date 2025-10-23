<template>
  <div class="min-h-screen flex items-center justify-center gradient-bg relative">
    <!-- Theme Toggle Button -->
    <button
      @click="themeStore.toggleTheme()"
      class="absolute top-4 right-4 p-2 rounded-lg bg-white/20 hover:bg-white/30 dark:bg-gray-800/50 dark:hover:bg-gray-700/50 backdrop-blur-sm transition-all"
      :title="themeStore.isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
    >
      <SunIcon v-if="themeStore.isDark" class="w-6 h-6 text-white" />
      <MoonIcon v-else class="w-6 h-6 text-white" />
    </button>

    <div class="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-xl shadow-2xl transition-colors duration-200">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
          Create your account
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Or
          <router-link to="/login" class="font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500">
            sign in to existing account
          </router-link>
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Full Name</label>
            <input
              id="full_name"
              v-model="form.full_name"
              name="full_name"
              type="text"
              required
              class="input-field mt-1"
              placeholder="Enter your full name"
            />
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email address</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              required
              class="input-field mt-1"
              placeholder="Enter your email"
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="input-field mt-1"
              placeholder="Enter your password"
            />
          </div>
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700">Confirm Password</label>
            <input
              id="confirm_password"
              v-model="form.confirm_password"
              name="confirm_password"
              type="password"
              required
              class="input-field mt-1"
              placeholder="Confirm your password"
            />
          </div>
        </div>

        <div v-if="error" class="text-red-600 text-sm text-center">
          {{ error }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="btn-primary w-full flex justify-center"
          >
            <span v-if="authStore.isLoading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating account...
            </span>
            <span v-else>Create Account</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'
import { useToast } from 'vue-toastification'
import { MoonIcon, SunIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const toast = useToast()

onMounted(() => {
  themeStore.initTheme()
})

const form = ref({
  full_name: '',
  email: '',
  password: '',
  confirm_password: ''
})

const error = ref('')

const handleRegister = async () => {
  error.value = ''
  
  if (form.value.password !== form.value.confirm_password) {
    error.value = 'Passwords do not match'
    return
  }
  
  const result = await authStore.register({
    full_name: form.value.full_name,
    email: form.value.email,
    password: form.value.password
  })
  
  if (result.success) {
    toast.success('Account created successfully! Please sign in.')
    router.push('/login')
  } else {
    error.value = result.error
  }
}
</script>
