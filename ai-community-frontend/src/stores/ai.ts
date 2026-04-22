import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatConversation, ChatMessage, AIResponse } from '@/types'
import { g4fClient, AVAILABLE_MODELS } from '@/utils/g4f-client'

export const useAIStore = defineStore('ai', () => {
  // State
  const conversations = ref<ChatConversation[]>([])
  const currentConversationId = ref<string | null>(null)
  const loading = ref(false)
  const selectedModel = ref('gpt-4o')
  const isInitialized = ref(false)

  // Getters
  const currentConversation = ref<ChatConversation | null>(null)

  // Actions
  async function initialize() {
    if (isInitialized.value) return

    loading.value = true
    try {
      await g4fClient.initialize()
      isInitialized.value = true

      // 从本地存储加载对话历史
      const saved = localStorage.getItem('ai-conversations')
      if (saved) {
        conversations.value = JSON.parse(saved)
      }

      // 如果没有对话，创建一个默认对话
      if (conversations.value.length === 0) {
        createConversation('新对话')
      } else {
        currentConversationId.value = conversations.value[0].id
        updateCurrentConversation()
      }
    } catch (error) {
      console.error('AI助手初始化失败:', error)
    } finally {
      loading.value = false
    }
  }

  function createConversation(title: string = '新对话') {
    const conversation: ChatConversation = {
      id: Date.now().toString(),
      title,
      messages: [],
      model: selectedModel.value,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }

    conversations.value.unshift(conversation)
    currentConversationId.value = conversation.id
    updateCurrentConversation()
    saveConversations()

    return conversation
  }

  function deleteConversation(id: string) {
    const index = conversations.value.findIndex(c => c.id === id)
    if (index > -1) {
      conversations.value.splice(index, 1)
      g4fClient.clearHistory(id)

      if (currentConversationId.value === id) {
        currentConversationId.value = conversations.value[0]?.id || null
        updateCurrentConversation()
      }

      saveConversations()
    }
  }

  function updateCurrentConversation() {
    if (currentConversationId.value) {
      currentConversation.value = conversations.value.find(
        c => c.id === currentConversationId.value
      ) || null
    } else {
      currentConversation.value = null
    }
  }

  async function sendMessage(message: string, systemPrompt: string = ''): Promise<AIResponse> {
    if (!currentConversationId.value) {
      createConversation()
    }

    loading.value = true

    // 添加用户消息
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    }

    if (currentConversation.value) {
      currentConversation.value.messages.push(userMessage)
      currentConversation.value.updatedAt = new Date().toISOString()

      // 更新对话标题（使用第一条消息）
      if (currentConversation.value.messages.length === 1) {
        currentConversation.value.title = message.slice(0, 30) + (message.length > 30 ? '...' : '')
      }
    }

    try {
      // 调用G4F客户端
      const response = await g4fClient.chat(message, {
        model: selectedModel.value,
        systemPrompt,
        conversationId: currentConversationId.value!
      })

      if (response.success && response.content) {
        // 添加AI响应
        const assistantMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: response.content,
          timestamp: new Date().toISOString()
        }

        if (currentConversation.value) {
          currentConversation.value.messages.push(assistantMessage)
        }

        saveConversations()
      }

      return response
    } catch (error: any) {
      return {
        success: false,
        error: error.message || '发送消息失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function optimizeIdea(ideaData: any): Promise<AIResponse> {
    loading.value = true
    try {
      return await g4fClient.optimizeIdea(ideaData)
    } finally {
      loading.value = false
    }
  }

  async function suggestTags(content: string, contentType: 'idea' | 'resource' = 'idea'): Promise<AIResponse> {
    loading.value = true
    try {
      return await g4fClient.suggestTags(content, contentType)
    } finally {
      loading.value = false
    }
  }

  async function analyzeMatch(idea: any, resource: any): Promise<AIResponse> {
    loading.value = true
    try {
      return await g4fClient.analyzeMatch(idea, resource)
    } finally {
      loading.value = false
    }
  }

  function selectConversation(id: string) {
    currentConversationId.value = id
    updateCurrentConversation()
  }

  function selectModel(modelId: string) {
    selectedModel.value = modelId
    if (currentConversation.value) {
      currentConversation.value.model = modelId
      saveConversations()
    }
  }

  function saveConversations() {
    localStorage.setItem('ai-conversations', JSON.stringify(conversations.value))
  }

  function clearAllConversations() {
    conversations.value.forEach(c => {
      g4fClient.clearHistory(c.id)
    })
    conversations.value = []
    currentConversationId.value = null
    currentConversation.value = null
    localStorage.removeItem('ai-conversations')
  }

  return {
    conversations,
    currentConversation,
    currentConversationId,
    loading,
    selectedModel,
    isInitialized,
    availableModels: AVAILABLE_MODELS,
    initialize,
    createConversation,
    deleteConversation,
    sendMessage,
    optimizeIdea,
    suggestTags,
    analyzeMatch,
    selectConversation,
    selectModel,
    clearAllConversations
  }
})
