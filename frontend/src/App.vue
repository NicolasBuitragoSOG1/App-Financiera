<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <div v-if="!authStore.isAuthenticated">
      <router-view />
    </div>
    <div v-else class="flex h-screen">
      <!-- Sidebar -->
      <aside class="w-64 bg-white shadow-lg">
        <div class="p-6">
          <h1 class="text-2xl font-bold text-gray-800">Finance Manager</h1>
        </div>
        <nav class="mt-6">
          <router-link
            v-for="item in navigation"
            :key="item.name"
            :to="item.href"
            class="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 hover:text-primary-600 transition-colors"
            :class="{ 'bg-primary-50 text-primary-600 border-r-2 border-primary-600': $route.name === item.name }"
          >
            <component :is="item.icon" class="w-5 h-5 mr-3" />
            {{ item.name }}
          </router-link>
        </nav>
        <div class="absolute bottom-0 w-64 p-6">
          <div class="flex items-center">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-700">{{ authStore.user?.full_name }}</p>
              <p class="text-xs text-gray-500">{{ authStore.user?.email }}</p>
            </div>
            <button
              @click="logout"
              class="ml-3 text-gray-400 hover:text-gray-600"
              title="Logout"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </aside>

      <!-- Main content -->
      <main class="flex-1 overflow-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import {
  HomeIcon,
  CreditCardIcon,
  ArrowsRightLeftIcon,
  ChartBarIcon,
  FlagIcon,
  ChatBubbleLeftRightIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Accounts', href: '/accounts', icon: CreditCardIcon },
  { name: 'Transactions', href: '/transactions', icon: ArrowsRightLeftIcon },
  { name: 'Goals', href: '/goals', icon: FlagIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'AIAssistant', href: '/ai-assistant', icon: ChatBubbleLeftRightIcon }
]

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
