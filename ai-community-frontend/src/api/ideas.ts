import request from './request'
import type { Idea, IdeaFormData, PaginatedResponse, ApiResponse } from '@/types'

export function getIdeas(params: {
  page?: number
  pageSize?: number
  category?: string
  status?: string
  search?: string
}) {
  return request.get<PaginatedResponse<Idea>>('/ideas', { params })
}

export function getIdeaById(id: number) {
  return request.get<ApiResponse<Idea>>(`/ideas/${id}`)
}

export function createIdea(data: IdeaFormData) {
  return request.post<ApiResponse<Idea>>('/ideas', data)
}

export function updateIdea(id: number, data: Partial<IdeaFormData>) {
  return request.put<ApiResponse<Idea>>(`/ideas/${id}`, data)
}

export function deleteIdea(id: number) {
  return request.delete<ApiResponse>(`/ideas/${id}`)
}

export function likeIdea(id: number) {
  return request.post<ApiResponse>(`/ideas/${id}/like`)
}

export function followIdea(id: number) {
  return request.post<ApiResponse>(`/ideas/${id}/follow`)
}

export function unFollowIdea(id: number) {
  return request.delete<ApiResponse>(`/ideas/${id}/follow`)
}
