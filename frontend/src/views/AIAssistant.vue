<template>
  <div class="p-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">AI Financial Assistant</h1>
      <p class="text-gray-600">Get personalized financial advice and recommendations</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Chat Interface -->
      <div class="lg:col-span-2">
        <div class="card h-96 flex flex-col">
          <!-- Chat Messages -->
          <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="chatContainer">
            <div v-if="aiStore.chatHistory.length === 0" class="text-center py-8">
              <ChatBubbleLeftRightIcon class="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 class="text-lg font-medium text-gray-900 mb-2">Welcome to your AI Financial Assistant</h3>
              <p class="text-gray-500 mb-4">Ask me anything about your finances, budgeting, or investment strategies.</p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-2 max-w-md mx-auto">
                <button
                  v-for="suggestion in quickSuggestions"
                  :key="suggestion"
                  @click="askQuestion(suggestion)"
                  class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-lg transition-colors"
                >
                  {{ suggestion }}
                </button>
              </div>
            </div>

            <div
              v-for="(message, index) in aiStore.chatHistory"
              :key="index"
              class="flex"
              :class="message.type === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div
                class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg"
                :class="message.type === 'user' 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-gray-100 text-gray-900'"
              >
                <p class="text-sm">{{ message.message }}</p>
                <p class="text-xs mt-1 opacity-75">
                  {{ formatTime(message.timestamp) }}
                </p>
                
                <!-- AI Recommendations -->
                <div v-if="message.type === 'ai' && message.recommendations?.length > 0" class="mt-3">
                  <p class="text-xs font-medium mb-2">Recommendations:</p>
                  <ul class="space-y-1">
                    <li
                      v-for="rec in message.recommendations"
                      :key="rec"
                      class="text-xs flex items-start"
                    >
                      <CheckCircleIcon class="w-3 h-3 text-green-500 mt-0.5 mr-1 flex-shrink-0" />
                      {{ rec }}
                    </li>
                  </ul>
                </div>

                <!-- Confidence Score -->
                <div v-if="message.type === 'ai' && message.confidence" class="mt-2">
                  <div class="flex items-center">
                    <span class="text-xs mr-2">Confidence:</span>
                    <div class="flex-1 bg-gray-200 rounded-full h-1">
                      <div
                        class="bg-green-500 h-1 rounded-full"
                        :style="{ width: `${message.confidence * 100}%` }"
                      ></div>
                    </div>
                    <span class="text-xs ml-2">{{ Math.round(message.confidence * 100) }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Loading indicator -->
            <div v-if="aiStore.isLoading" class="flex justify-start">
              <div class="bg-gray-100 text-gray-900 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
                <div class="flex items-center space-x-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                  <span class="text-sm">AI is thinking...</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Chat Input -->
          <div class="border-t border-gray-200 p-4">
            <form @submit.prevent="sendMessage" class="flex space-x-2">
              <input
                v-model="currentMessage"
                type="text"
                placeholder="Ask about your finances..."
                class="flex-1 input-field"
                :disabled="aiStore.isLoading"
              />
              <button
                type="submit"
                :disabled="!currentMessage.trim() || aiStore.isLoading"
                class="btn-primary"
              >
                <PaperAirplaneIcon class="w-5 h-5" />
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Financial Summary & Quick Actions -->
      <div class="space-y-6">
        <!-- Financial Overview -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Your Financial Snapshot</h3>
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Total Balance</span>
              <span class="text-sm font-medium">${{ formatCurrency(financeStore.totalBalance) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Monthly Income</span>
              <span class="text-sm font-medium text-green-600">
                ${{ formatCurrency(financeStore.overview?.monthly_income || 0) }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Monthly Expenses</span>
              <span class="text-sm font-medium text-red-600">
                ${{ formatCurrency(financeStore.overview?.monthly_expenses || 0) }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Savings Rate</span>
              <span class="text-sm font-medium text-blue-600">
                {{ formatPercentage(financeStore.overview?.savings_rate || 0) }}%
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Active Goals</span>
              <span class="text-sm font-medium">{{ financeStore.goals.length }}</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div class="space-y-2">
            <button
              v-for="action in quickActions"
              :key="action.text"
              @click="askQuestion(action.query)"
              class="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <div class="flex items-center">
                <component :is="action.icon" class="w-5 h-5 text-primary-600 mr-3" />
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ action.text }}</p>
                  <p class="text-xs text-gray-500">{{ action.description }}</p>
                </div>
              </div>
            </button>
          </div>
        </div>

        <!-- AI Tips -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">AI Tips</h3>
          <div class="space-y-3">
            <div v-for="tip in aiTips" :key="tip.title" class="p-3 bg-blue-50 rounded-lg">
              <h4 class="text-sm font-medium text-blue-900">{{ tip.title }}</h4>
              <p class="text-xs text-blue-700 mt-1">{{ tip.description }}</p>
            </div>
          </div>
        </div>

        <!-- Clear Chat -->
        <div class="card">
          <button
            @click="clearChat"
            class="w-full btn-secondary text-sm"
          >
            <TrashIcon class="w-4 h-4 mr-2" />
            Clear Chat History
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useFinanceStore } from '../stores/finance'
import { useAIStore } from '../stores/ai'
import { useToast } from 'vue-toastification'
import {
  ChatBubbleLeftRightIcon,
  PaperAirplaneIcon,
  CheckCircleIcon,
  TrashIcon,
  ChartBarIcon,
  CurrencyDollarIcon,
  LightBulbIcon,
  ShieldCheckIcon
} from '@heroicons/vue/24/outline'
import { format } from 'date-fns'

const financeStore = useFinanceStore()
const aiStore = useAIStore()
const toast = useToast()

const currentMessage = ref('')
const chatContainer = ref(null)

const quickSuggestions = [
  'How can I improve my savings rate?',
  'What should I budget for next month?',
  'How am I doing with my financial goals?',
  'Should I invest more money?'
]

const quickActions = [
  {
    text: 'Budget Analysis',
    description: 'Get insights on your spending',
    query: 'Analyze my current budget and spending patterns',
    icon: ChartBarIcon
  },
  {
    text: 'Savings Strategy',
    description: 'Improve your savings rate',
    query: 'What are the best strategies to increase my savings?',
    icon: CurrencyDollarIcon
  },
  {
    text: 'Goal Planning',
    description: 'Plan your financial goals',
    query: 'Help me create a plan to achieve my financial goals',
    icon: LightBulbIcon
  },
  {
    text: 'Risk Assessment',
    description: 'Evaluate your financial health',
    query: 'Assess my financial health and identify potential risks',
    icon: ShieldCheckIcon
  }
]

const aiTips = [
  {
    title: 'Be Specific',
    description: 'Ask detailed questions about your finances for better advice'
  },
  {
    title: 'Context Matters',
    description: 'The AI uses your actual financial data to provide personalized recommendations'
  },
  {
    title: 'Follow Up',
    description: 'Ask follow-up questions to dive deeper into any topic'
  }
]

onMounted(() => {
  financeStore.initializeData()
})

const sendMessage = async () => {
  if (!currentMessage.value.trim()) return

  const message = currentMessage.value.trim()
  currentMessage.value = ''

  const result = await aiStore.getFinancialAdvice(message)

  if (!result.success) {
    toast.error(result.error)
  }

  // Scroll to bottom
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const askQuestion = async (question) => {
  currentMessage.value = question
  await sendMessage()
}

const clearChat = () => {
  aiStore.clearChatHistory()
  toast.success('Chat history cleared')
}

const formatTime = (timestamp) => {
  return format(new Date(timestamp), 'HH:mm')
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatPercentage = (value) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value)
}
</script>
