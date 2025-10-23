import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAIStore = defineStore('ai', () => {
  const isLoading = ref(false)
  const chatHistory = ref([])

  const getFinancialAdvice = async (query) => {
    // Add user message immediately
    chatHistory.value.push({
      type: 'user',
      message: query,
      timestamp: new Date()
    })
    
    isLoading.value = true
    try {
      const response = await axios.post('/api/ai/advice', { query })
      const aiResponse = response.data
      
      // Add AI response to chat history
      chatHistory.value.push({
        type: 'ai',
        message: aiResponse.response,
        recommendations: aiResponse.recommendations,
        confidence: aiResponse.confidence,
        timestamp: new Date()
      })
      
      return { success: true, data: aiResponse }
    } catch (error) {
      console.error('AI advice error:', error)
      // Add error message to chat
      chatHistory.value.push({
        type: 'ai',
        message: 'I apologize, but I encountered an error processing your request. Please try again or contact support if the issue persists.',
        timestamp: new Date()
      })
      
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to get AI advice' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const clearChatHistory = () => {
    chatHistory.value = []
  }

  return {
    isLoading,
    chatHistory,
    getFinancialAdvice,
    clearChatHistory
  }
})
