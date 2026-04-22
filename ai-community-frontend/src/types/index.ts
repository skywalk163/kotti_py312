// 用户相关类型
export interface User {
  id: number
  name: string
  email: string
  avatar?: string
  bio?: string
  createdAt: string
  reputation: number
}

export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm {
  name: string
  email: string
  password: string
  confirmPassword: string
}

// 点子相关类型
export interface Idea {
  id: number
  title: string
  description: string
  category: IdeaCategory
  difficulty: DifficultyLevel
  status: IdeaStatus
  tags: string[]
  neededResources: string
  expectedOutcome: string
  estimatedDays: number
  author: User
  followersCount: number
  likesCount: number
  viewsCount: number
  createdAt: string
  updatedAt: string
  aiSuggestions?: string
}

export type IdeaCategory = 'tool' | 'research' | 'startup' | 'learning' | 'creative' | 'other'
export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced' | 'expert'
export type IdeaStatus = 'draft' | 'brainstorming' | 'recruiting' | 'in_progress' | 'completed' | 'archived'

export interface IdeaFormData {
  title: string
  category: IdeaCategory
  difficulty: DifficultyLevel
  description: string
  tags: string[]
  neededResources: string
  expectedOutcome: string
  estimatedDays: number
}

// 资源相关类型
export interface Resource {
  id: number
  title: string
  description: string
  category: ResourceCategory
  accessType: AccessType
  tags: string[]
  url: string
  usageGuide: string
  limitations: string
  availability: string
  author: User
  referencesCount: number
  likesCount: number
  viewsCount: number
  createdAt: string
  updatedAt: string
}

export type ResourceCategory = 'model' | 'dataset' | 'tool' | 'api' | 'compute' | 'funding' | 'mentor' | 'other'
export type AccessType = 'free' | 'freemium' | 'paid' | 'application' | 'invite'

export interface ResourceFormData {
  title: string
  category: ResourceCategory
  accessType: AccessType
  description: string
  tags: string[]
  url: string
  usageGuide: string
  limitations: string
}

// AI助手相关类型
export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
}

export interface ChatConversation {
  id: string
  title: string
  messages: ChatMessage[]
  model: string
  createdAt: string
  updatedAt: string
}

export interface AIResponse {
  success: boolean
  content?: string
  error?: string
  model?: string
  usage?: {
    promptTokens: number
    completionTokens: number
    totalTokens: number
  }
}

// API响应类型
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  success: boolean
  data: T[]
  pagination: {
    page: number
    pageSize: number
    total: number
    totalPages: number
  }
}

// 匹配相关类型
export interface MatchResult {
  idea: Idea
  resource: Resource
  score: number
  reasons: string[]
  suggestions: string[]
}
