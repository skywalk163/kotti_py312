import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Idea, IdeaFormData, PaginatedResponse } from '@/types'
import * as ideaApi from '@/api/ideas'

export const useIdeaStore = defineStore('idea', () => {
  // State
  const ideas = ref<Idea[]>([])
  const currentIdea = ref<Idea | null>(null)
  const loading = ref(false)
  const pagination = ref({
    page: 1,
    pageSize: 20,
    total: 0,
    totalPages: 0
  })

  // Actions
  async function fetchIdeas(params: {
    page?: number
    pageSize?: number
    category?: string
    status?: string
    search?: string
  } = {}) {
    loading.value = true
    try {
      const response = await ideaApi.getIdeas(params)
      if (response.success && response.data) {
        ideas.value = response.data
        if (response.pagination) {
          pagination.value = response.pagination
        }
      }
    } catch (error) {
      console.error('Failed to fetch ideas:', error)
    } finally {
      loading.value = false
    }
  }

  async function fetchIdeaById(id: number) {
    loading.value = true
    try {
      const response = await ideaApi.getIdeaById(id)
      if (response.success && response.data) {
        currentIdea.value = response.data
      }
    } catch (error) {
      console.error('Failed to fetch idea:', error)
    } finally {
      loading.value = false
    }
  }

  async function createIdea(ideaData: IdeaFormData) {
    loading.value = true
    try {
      const response = await ideaApi.createIdea(ideaData)
      if (response.success && response.data) {
        return { success: true, data: response.data }
      }
      return { success: false, error: response.error }
    } catch (error: any) {
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  async function updateIdea(id: number, ideaData: Partial<IdeaFormData>) {
    loading.value = true
    try {
      const response = await ideaApi.updateIdea(id, ideaData)
      if (response.success && response.data) {
        currentIdea.value = response.data
        return { success: true }
      }
      return { success: false, error: response.error }
    } catch (error: any) {
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  async function deleteIdea(id: number) {
    loading.value = true
    try {
      const response = await ideaApi.deleteIdea(id)
      if (response.success) {
        ideas.value = ideas.value.filter(idea => idea.id !== id)
        return { success: true }
      }
      return { success: false, error: response.error }
    } catch (error: any) {
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  async function likeIdea(id: number) {
    try {
      const response = await ideaApi.likeIdea(id)
      if (response.success && currentIdea.value?.id === id) {
        currentIdea.value.likesCount++
      }
      return response.success
    } catch (error) {
      console.error('Failed to like idea:', error)
      return false
    }
  }

  async function followIdea(id: number) {
    try {
      const response = await ideaApi.followIdea(id)
      if (response.success && currentIdea.value?.id === id) {
        currentIdea.value.followersCount++
      }
      return response.success
    } catch (error) {
      console.error('Failed to follow idea:', error)
      return false
    }
  }

  return {
    ideas,
    currentIdea,
    loading,
    pagination,
    fetchIdeas,
    fetchIdeaById,
    createIdea,
    updateIdea,
    deleteIdea,
    likeIdea,
    followIdea
  }
})
