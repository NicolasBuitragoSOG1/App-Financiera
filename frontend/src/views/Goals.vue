<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Financial Goals</h1>
        <p class="text-gray-600 dark:text-gray-400">Set and track your financial objectives</p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary">
        <PlusIcon class="w-5 h-5 mr-2" />
        Add Goal
      </button>
    </div>

    <!-- Goals Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="goal in financeStore.goals"
        :key="goal.id"
        class="card hover:shadow-md transition-shadow"
      >
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <FlagIcon class="w-6 h-6 text-primary-600" />
            </div>
            <div class="ml-3">
              <h3 class="font-semibold text-gray-900 dark:text-white">{{ goal.goal_name }}</h3>
              <p class="text-sm text-gray-500 capitalize">{{ goal.goal_type.replace('_', ' ') }}</p>
            </div>
          </div>
          <span class="text-xs px-2 py-1 rounded-full"
                :class="getPriorityClass(goal.priority)">
            {{ goal.priority }}
          </span>
        </div>

        <div class="space-y-3">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Progress</span>
            <span class="font-medium text-gray-900 dark:text-white">{{ Math.round((goal.current_amount / goal.target_amount) * 100) }}%</span>
          </div>
          
          <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-3">
            <div
              class="bg-primary-600 h-3 rounded-full transition-all duration-300"
              :style="{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }"
            ></div>
          </div>

          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Current</span>
            <span class="font-medium text-gray-900 dark:text-white">${{ formatCurrency(goal.current_amount) }}</span>
          </div>
          
          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Target</span>
            <span class="font-medium text-gray-900 dark:text-white">${{ formatCurrency(goal.target_amount) }}</span>
          </div>

          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Target Date</span>
            <span class="font-medium text-gray-900 dark:text-white">{{ formatDate(goal.target_date) }}</span>
          </div>

          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Remaining</span>
            <span class="font-medium text-primary-600 dark:text-primary-400">
              ${{ formatCurrency(goal.target_amount - goal.current_amount) }}
            </span>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 flex space-x-2">
          <button
            @click="updateProgress(goal)"
            class="btn-primary flex-1 text-sm"
          >
            Update Progress
          </button>
          <button
            @click="editGoal(goal)"
            class="btn-secondary text-sm"
          >
            <PencilIcon class="w-4 h-4" />
          </button>
          <button
            @click="deleteGoal(goal)"
            class="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg text-sm transition-colors"
          >
            <TrashIcon class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="financeStore.goals.length === 0" class="col-span-full">
        <div class="text-center py-12">
          <FlagIcon class="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No goals yet</h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6">Set your first financial goal to start tracking your progress</p>
          <button @click="showCreateModal = true" class="btn-primary">
            Create Your First Goal
          </button>
        </div>
      </div>
    </div>

    <!-- Create Goal Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Create New Goal</h3>
        
        <form @submit.prevent="createGoal" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Goal Name</label>
            <input
              v-model="newGoal.goal_name"
              type="text"
              required
              class="input-field"
              placeholder="e.g., Emergency Fund"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Goal Type</label>
            <select v-model="newGoal.goal_type" required class="input-field">
              <option value="">Select type</option>
              <option value="savings">Savings</option>
              <option value="debt_reduction">Debt Reduction</option>
              <option value="investment">Investment</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Target Amount</label>
            <input
              v-model.number="newGoal.target_amount"
              type="number"
              step="0.01"
              required
              class="input-field"
              placeholder="0.00"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Target Date</label>
            <input
              v-model="newGoal.target_date"
              type="date"
              required
              class="input-field"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Priority</label>
            <select v-model="newGoal.priority" class="input-field">
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <div v-if="createError" class="text-red-600 dark:text-red-400 text-sm">
            {{ createError }}
          </div>

          <div class="flex space-x-3 pt-4">
            <button type="submit" class="btn-primary flex-1">
              Create Goal
            </button>
            <button
              type="button"
              @click="cancelCreate"
              class="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Goal Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Edit Goal</h3>
        
        <form @submit.prevent="saveEditGoal" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Goal Name</label>
            <input
              v-model="editGoalData.goal_name"
              type="text"
              required
              class="input-field"
              placeholder="e.g., Emergency Fund"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Goal Type</label>
            <select v-model="editGoalData.goal_type" required class="input-field">
              <option value="">Select type</option>
              <option value="savings">Savings</option>
              <option value="debt_reduction">Debt Reduction</option>
              <option value="investment">Investment</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Target Amount</label>
            <input
              v-model.number="editGoalData.target_amount"
              type="number"
              step="0.01"
              required
              class="input-field"
              placeholder="0.00"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Current Amount</label>
            <input
              v-model.number="editGoalData.current_amount"
              type="number"
              step="0.01"
              required
              class="input-field"
              placeholder="0.00"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Target Date</label>
            <input
              v-model="editGoalData.target_date"
              type="date"
              required
              class="input-field"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Priority</label>
            <select v-model="editGoalData.priority" class="input-field">
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <div v-if="editError" class="text-red-600 dark:text-red-400 text-sm">
            {{ editError }}
          </div>

          <div class="flex space-x-3 pt-4">
            <button type="submit" class="btn-primary flex-1">
              Save Changes
            </button>
            <button
              type="button"
              @click="cancelEdit"
              class="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Update Progress Modal -->
    <div v-if="showUpdateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Update Progress</h3>
        
        <div class="mb-4">
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ selectedGoal?.goal_name }}</p>
          <p class="text-lg font-semibold text-gray-900 dark:text-white">Current: ${{ formatCurrency(selectedGoal?.current_amount || 0) }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">Target: ${{ formatCurrency(selectedGoal?.target_amount || 0) }}</p>
        </div>

        <form @submit.prevent="saveProgress" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">New Amount</label>
            <input
              v-model.number="newAmount"
              type="number"
              step="0.01"
              required
              class="input-field"
              placeholder="0.00"
            />
          </div>

          <div v-if="updateError" class="text-red-600 text-sm">
            {{ updateError }}
          </div>

          <div class="flex space-x-3 pt-4">
            <button type="submit" class="btn-primary flex-1">
              Update Progress
            </button>
            <button
              type="button"
              @click="cancelUpdate"
              class="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useFinanceStore } from '../stores/finance'
import { useToast } from 'vue-toastification'
import {
  PlusIcon,
  FlagIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import { format } from 'date-fns'

const financeStore = useFinanceStore()
const toast = useToast()

const showCreateModal = ref(false)
const showUpdateModal = ref(false)
const showEditModal = ref(false)
const selectedGoal = ref(null)
const createError = ref('')
const updateError = ref('')
const editError = ref('')

const newGoal = ref({
  goal_name: '',
  goal_type: '',
  target_amount: 0,
  target_date: '',
  priority: 'medium'
})

const newAmount = ref(0)

const editGoalData = ref({
  id: null,
  goal_name: '',
  goal_type: '',
  target_amount: 0,
  current_amount: 0,
  target_date: '',
  priority: 'medium'
})

onMounted(() => {
  financeStore.initializeData()
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatDate = (dateString) => {
  return format(new Date(dateString), 'MMM dd, yyyy')
}

const getPriorityClass = (priority) => {
  switch (priority) {
    case 'high':
      return 'bg-red-100 text-red-800'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800'
    case 'low':
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const createGoal = async () => {
  createError.value = ''
  
  const goalData = {
    ...newGoal.value,
    target_date: new Date(newGoal.value.target_date).toISOString()
  }
  
  const result = await financeStore.createGoal(goalData)
  
  if (result.success) {
    toast.success('Goal created successfully!')
    cancelCreate()
  } else {
    createError.value = result.error
  }
}

const cancelCreate = () => {
  showCreateModal.value = false
  newGoal.value = {
    goal_name: '',
    goal_type: '',
    target_amount: 0,
    target_date: '',
    priority: 'medium'
  }
  createError.value = ''
}

const updateProgress = (goal) => {
  selectedGoal.value = goal
  newAmount.value = goal.current_amount
  showUpdateModal.value = true
}

const saveProgress = async () => {
  updateError.value = ''
  
  const result = await financeStore.updateGoalProgress(selectedGoal.value.id, newAmount.value)
  
  if (result.success) {
    toast.success('Progress updated successfully!')
    cancelUpdate()
  } else {
    updateError.value = result.error
  }
}

const cancelUpdate = () => {
  showUpdateModal.value = false
  selectedGoal.value = null
  newAmount.value = 0
  updateError.value = ''
}

const editGoal = (goal) => {
  selectedGoal.value = goal
  editGoalData.value = {
    id: goal.id,
    goal_name: goal.goal_name,
    goal_type: goal.goal_type,
    target_amount: goal.target_amount,
    current_amount: goal.current_amount,
    target_date: goal.target_date.split('T')[0], // Format date for input
    priority: goal.priority
  }
  showEditModal.value = true
}

const saveEditGoal = async () => {
  editError.value = ''
  
  const goalData = {
    ...editGoalData.value,
    target_date: new Date(editGoalData.value.target_date).toISOString()
  }
  
  const result = await financeStore.updateGoal(goalData.id, goalData)
  
  if (result.success) {
    toast.success('Goal updated successfully!')
    cancelEdit()
  } else {
    editError.value = result.error
  }
}

const cancelEdit = () => {
  showEditModal.value = false
  selectedGoal.value = null
  editGoalData.value = {
    id: null,
    goal_name: '',
    goal_type: '',
    target_amount: 0,
    current_amount: 0,
    target_date: '',
    priority: 'medium'
  }
  editError.value = ''
}

const deleteGoal = async (goal) => {
  if (confirm(`Are you sure you want to delete "${goal.goal_name}"? This action cannot be undone.`)) {
    const result = await financeStore.deleteGoal(goal.id)
    
    if (result.success) {
      toast.success('Goal deleted successfully!')
    } else {
      toast.error(result.error || 'Failed to delete goal')
    }
  }
}
</script>
