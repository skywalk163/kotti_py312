# AI交流社区前端

基于Vue3 + TypeScript + Element Plus构建的AI资源互助平台前端应用。

## 功能特性

- 🚀 **Vue3 + TypeScript**: 使用最新的Vue3 Composition API和TypeScript
- 🎨 **Element Plus**: 基于Element Plus UI组件库
- 🤖 **G4F集成**: 浏览器端直接调用AI模型，零服务器成本
- 🔐 **用户认证**: 完整的用户注册、登录、权限管理
- 💡 **点子广场**: 发布、浏览、搜索AI点子
- 📦 **资源库**: 分享和管理AI相关资源
- 🤝 **智能匹配**: AI驱动的点子-资源匹配系统
- 💬 **AI助手**: 多模型AI对话助手

## 技术栈

- **框架**: Vue 3.4+
- **语言**: TypeScript 5.3+
- **构建工具**: Vite 5.0+
- **UI组件**: Element Plus 2.5+
- **状态管理**: Pinia 2.1+
- **路由**: Vue Router 4.2+
- **HTTP客户端**: Axios 1.6+
- **AI集成**: G4F (浏览器端)

## 项目结构

```
ai-community-frontend/
├── src/
│   ├── api/              # API接口
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia状态管理
│   ├── types/            # TypeScript类型定义
│   ├── utils/            # 工具函数
│   ├── views/            # 页面组件
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── public/               # 公共静态资源
├── index.html            # HTML模板
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript配置
├── vite.config.ts        # Vite配置
└── README.md             # 项目说明
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 核心功能说明

### 1. G4F AI集成

项目集成了G4F (GPT4Free)客户端，可以在浏览器端直接调用AI模型：

```typescript
import { g4fClient } from '@/utils/g4f-client'

// 初始化客户端
await g4fClient.initialize()

// 发送消息
const response = await g4fClient.chat('你好', {
  model: 'gpt-4o',
  systemPrompt: '你是一个AI助手'
})
```

**支持的模型:**
- GPT-4o
- GPT-4 Turbo
- GPT-3.5 Turbo
- Claude 3 Opus
- Claude 3 Sonnet
- DeepSeek Chat

### 2. 用户认证系统

完整的用户认证流程：

```typescript
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 登录
await userStore.login({
  email: 'user@example.com',
  password: 'password'
})

// 注册
await userStore.register({
  name: '张三',
  email: 'user@example.com',
  password: 'password',
  confirmPassword: 'password'
})
```

### 3. 点子发布与AI优化

发布点子时可以使用AI优化描述和生成标签：

```typescript
import { useAIStore } from '@/stores/ai'

const aiStore = useAIStore()

// AI优化点子描述
const response = await aiStore.optimizeIdea({
  title: '我的AI点子',
  category: 'tool',
  description: '这是一个很棒的点子...'
})

// 生成标签
const tags = await aiStore.suggestTags('点子描述内容', 'idea')
```

### 4. 智能匹配系统

AI驱动的点子-资源匹配：

```typescript
const matchResult = await aiStore.analyzeMatch(idea, resource)
```

## API接口

前端通过Axios与后端Kotti CMS进行通信：

```typescript
// API基础配置
baseURL: '/api'  // 开发环境代理到 http://localhost:5000

// 认证
POST /api/auth/login
POST /api/auth/register
GET  /api/auth/me

// 点子
GET    /api/ideas
POST   /api/ideas
GET    /api/ideas/:id
PUT    /api/ideas/:id
DELETE /api/ideas/:id

// 资源
GET    /api/resources
POST   /api/resources
GET    /api/resources/:id
```

## 环境变量

创建 `.env.development` 文件：

```env
VITE_API_BASE_URL=http://localhost:5000
VITE_APP_TITLE=AI交流社区
```

创建 `.env.production` 文件：

```env
VITE_API_BASE_URL=https://api.example.com
VITE_APP_TITLE=AI交流社区
```

## 部署

### Docker部署

```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Nginx配置

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 开发指南

### 添加新页面

1. 在 `src/views/` 创建新组件
2. 在 `src/router/index.ts` 添加路由
3. 在导航菜单中添加链接

### 添加新的API接口

1. 在 `src/types/` 定义类型
2. 在 `src/api/` 创建API函数
3. 在对应的store中调用API

### 状态管理

使用Pinia进行状态管理：

```typescript
// stores/example.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useExampleStore = defineStore('example', () => {
  const count = ref(0)

  function increment() {
    count.value++
  }

  return { count, increment }
})
```

## 浏览器兼容性

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- 项目地址: https://github.com/yourusername/ai-community-frontend
- 问题反馈: https://github.com/yourusername/ai-community-frontend/issues
