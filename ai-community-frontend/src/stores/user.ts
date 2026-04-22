import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginForm, RegisterForm } from '@/types'
import * as authApi from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)

  // Getters
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  // Actions
  async function login(loginForm: LoginForm) {
    loading.value = true
    try {
      const response = await authApi.login(loginForm)
      if (response.success && response.data) {
        token.value = response.data.token
        user.value = response.data.user
        localStorage.setItem('token', response.data.token)
        return { success: true }
      }
      return { success: false, error: response.error }
    } catch (error: any) {
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  async function register(registerForm: RegisterForm) {
    loading.value = true
    try {
      const response = await authApi.register(registerForm)
      if (response.success) {
        return { success: true }
      }
      return { success: false, error: response.error }
    } catch (error: any) {
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return

    loading.value = true
    try {
      const response = await authApi.getCurrentUser()
      if (response.success && response.data) {
        user.value = response.data
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  // Initialize
  if (token.value) {
    fetchUser()
  }

  return {
    user,
    token,
    loading,
    isLoggedIn,
    login,
    register,
    fetchUser,
    logout
  }
})
