/**
 * G4F客户端封装
 * 用于在浏览器端直接调用AI模型，无需服务器支持
 */

import type { AIResponse, ChatMessage } from '@/types'

export interface G4FChatOptions {
  model?: string
  systemPrompt?: string
  conversationId?: string
  temperature?: number
  maxTokens?: number
}

export interface G4FModelInfo {
  id: string
  name: string
  provider: string
  description: string
}

// 可用的模型列表
export const AVAILABLE_MODELS: G4FModelInfo[] = [
  {
    id: 'gpt-4o',
    name: 'GPT-4o',
    provider: 'OpenAI',
    description: '最新的GPT-4 Omni模型，支持多模态'
  },
  {
    id: 'gpt-4-turbo',
    name: 'GPT-4 Turbo',
    provider: 'OpenAI',
    description: '高性能GPT-4模型'
  },
  {
    id: 'gpt-3.5-turbo',
    name: 'GPT-3.5 Turbo',
    provider: 'OpenAI',
    description: '快速响应的GPT-3.5模型'
  },
  {
    id: 'claude-3-opus',
    name: 'Claude 3 Opus',
    provider: 'Anthropic',
    description: '最强大的Claude模型'
  },
  {
    id: 'claude-3-sonnet',
    name: 'Claude 3 Sonnet',
    provider: 'Anthropic',
    description: '平衡性能和速度的Claude模型'
  },
  {
    id: 'deepseek-chat',
    name: 'DeepSeek Chat',
    provider: 'DeepSeek',
    description: 'DeepSeek对话模型'
  }
]

export class G4FClient {
  private client: any = null
  private conversationHistory: Record<string, ChatMessage[]> = {}
  private isInitialized = false

  /**
   * 初始化G4F客户端
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) {
      return
    }

    try {
      // 动态导入g4f客户端
      const g4fModule = await import('https://g4f.dev/dist/js/client.js')
      this.client = new g4fModule.Client()
      this.isInitialized = true
      console.log('G4F客户端初始化成功')
    } catch (error) {
      console.error('G4F客户端初始化失败:', error)
      throw new Error('无法加载G4F客户端，请检查网络连接')
    }
  }

  /**
   * 发送聊天消息
   */
  async chat(
    message: string,
    options: G4FChatOptions = {}
  ): Promise<AIResponse> {
    if (!this.isInitialized) {
      await this.initialize()
    }

    const {
      model = 'gpt-4o',
      systemPrompt = '',
      conversationId = 'default',
      temperature = 0.7,
      maxTokens
    } = options

    try {
      // 构建消息历史
      const messages: any[] = []

      if (systemPrompt) {
        messages.push({ role: 'system', content: systemPrompt })
      }

      // 添加历史消息
      if (this.conversationHistory[conversationId]) {
        messages.push(...this.conversationHistory[conversationId])
      }

      // 添加当前消息
      messages.push({ role: 'user', content: message })

      // 调用G4F API
      const result = await this.client.chat.completions.create({
        model,
        messages,
        temperature,
        ...(maxTokens && { max_tokens: maxTokens })
      })

      // 提取响应内容
      const content = result.choices[0].message.content

      // 保存到历史记录
      if (!this.conversationHistory[conversationId]) {
        this.conversationHistory[conversationId] = []
      }

      this.conversationHistory[conversationId].push(
        {
          id: Date.now().toString(),
          role: 'user',
          content: message,
          timestamp: new Date().toISOString()
        },
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content,
          timestamp: new Date().toISOString()
        }
      )

      return {
        success: true,
        content,
        model,
        usage: result.usage || {
          promptTokens: 0,
          completionTokens: 0,
          totalTokens: 0
        }
      }
    } catch (error: any) {
      console.error('G4F聊天失败:', error)
      return {
        success: false,
        error: error.message || 'AI响应失败，请稍后重试'
      }
    }
  }

  /**
   * 优化点子描述
   */
  async optimizeIdea(ideaData: {
    title: string
    category: string
    description: string
    needed_resources?: string
    expected_outcome?: string
  }): Promise<AIResponse> {
    const prompt = `请帮我优化以下 AI 点子的描述，使其更加清晰、专业、有吸引力：

标题：${ideaData.title}
分类：${ideaData.category}
当前描述：${ideaData.description}
需要的资源：${ideaData.needed_resources || '未填写'}
预期成果：${ideaData.expected_outcome || '未填写'}

请从以下几个方面进行优化：
1. 点子背景和动机
2. 核心创新点
3. 技术可行性分析
4. 预期价值和影响
5. 实施建议

请用中文回复，格式清晰。`

    return this.chat(prompt, {
      systemPrompt: '你是一位 AI 产品专家和技术顾问，擅长帮助用户完善和优化 AI 项目点子。',
      conversationId: `idea-${Date.now()}`
    })
  }

  /**
   * 生成标签建议
   */
  async suggestTags(content: string, contentType: 'idea' | 'resource' = 'idea'): Promise<AIResponse> {
    const prompt = `请根据以下内容，生成 5-10 个合适的标签：

类型：${contentType === 'idea' ? '点子' : '资源'}
内容：${content}

要求：
1. 标签要准确反映内容主题
2. 包含技术领域标签（如：NLP、CV、LLM等）
3. 包含应用场景标签（如：智能客服、图像生成等）
4. 标签简洁，每个 2-8 个字
5. 只输出标签，用逗号分隔`

    return this.chat(prompt, {
      systemPrompt: '你是一位标签分类专家，擅长为内容生成准确的分类标签。',
      conversationId: `tags-${Date.now()}`
    })
  }

  /**
   * 分析点子和资源的匹配度
   */
  async analyzeMatch(idea: any, resource: any): Promise<AIResponse> {
    const prompt = `分析以下点子和资源的匹配度：

点子：
- 标题：${idea.title}
- 描述：${idea.description}
- 需要的资源：${idea.needed_resources || '未填写'}

资源：
- 标题：${resource.title}
- 描述：${resource.description}
- 分类：${resource.category}

请分析：
1. 匹配度评分（0-100分）
2. 匹配理由
3. 使用建议`

    return this.chat(prompt, {
      systemPrompt: '你是一位项目匹配专家，擅长分析点子和资源的契合度。',
      conversationId: `match-${Date.now()}`
    })
  }

  /**
   * 清除对话历史
   */
  clearHistory(conversationId = 'default'): void {
    delete this.conversationHistory[conversationId]
  }

  /**
   * 获取对话历史
   */
  getHistory(conversationId = 'default'): ChatMessage[] {
    return this.conversationHistory[conversationId] || []
  }

  /**
   * 检查是否已初始化
   */
  isReady(): boolean {
    return this.isInitialized
  }
}

// 导出单例实例
export const g4fClient = new G4FClient()
