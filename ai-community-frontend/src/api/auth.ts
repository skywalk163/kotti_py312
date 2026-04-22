import request from './request'
import type { LoginForm, RegisterForm, User, ApiResponse } from '@/types'

export function login(data: LoginForm) {
  return request.post<ApiResponse<{ token: string; user: User }>>('/auth/login', data)
}

export function register(data: RegisterForm) {
  return request.post<ApiResponse>('/auth/register', data)
}

export function getCurrentUser() {
  return request.get<ApiResponse<User>>('/auth/me')
}

export function logout() {
  return request.post<ApiResponse>('/auth/logout')
}

export function updateProfile(data: Partial<User>) {
  return request.put<ApiResponse<User>>('/auth/profile', data)
}

export function changePassword(data: { oldPassword: string; newPassword: string }) {
  return request.post<ApiResponse>('/auth/change-password', data)
}
