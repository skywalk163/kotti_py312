<template>
  <div class="home-view">
    <el-row :gutter="20">
      <el-col :span="16">
        <!-- 欢迎横幅 -->
        <el-card class="welcome-banner">
          <h1>欢迎来到AI交流社区</h1>
          <p>点子共享，实践落地 - 让AI创意成为现实</p>
          <div class="action-buttons">
            <el-button type="primary" size="large" @click="handleCreateIdea">
              <el-icon><Edit /></el-icon>
              发布点子
            </el-button>
            <el-button size="large" @click="handleBrowseIdeas">
              <el-icon><Search /></el-icon>
              浏览点子
            </el-button>
          </div>
        </el-card>

        <!-- 热门点子 -->
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>🔥 热门点子</span>
              <el-link type="primary" @click="$router.push('/ideas')">查看更多</el-link>
            </div>
          </template>
          <div v-loading="loading" class="ideas-list">
            <div v-for="idea in hotIdeas" :key="idea.id" class="idea-item">
              <router-link :to="`/ideas/${idea.id}`" class="idea-title">
                {{ idea.title }}
              </router-link>
              <div class="idea-meta">
                <el-tag size="small">{{ getCategoryLabel(idea.category) }}</el-tag>
                <el-tag size="small" type="info">{{ getDifficultyLabel(idea.difficulty) }}</el-tag>
                <span class="meta-item">
                  <el-icon><User /></el-icon>
                  {{ idea.author.name }}
                </span>
                <span class="meta-item">
                  <el-icon><View /></el-icon>
                  {{ idea.viewsCount }}
                </span>
                <span class="meta-item">
                  <el-icon><Star /></el-icon>
                  {{ idea.likesCount }}
                </span>
              </div>
              <p class="idea-description">{{ idea.description }}</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <!-- 统计信息 -->
        <el-card class="stats-card">
          <template #header>
            <span>📊 社区统计</span>
          </template>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">{{ stats.ideasCount }}</div>
              <div class="stat-label">点子总数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.resourcesCount }}</div>
              <div class="stat-label">资源总数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.usersCount }}</div>
              <div class="stat-label">用户总数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.matchesCount }}</div>
              <div class="stat-label">成功匹配</div>
            </div>
          </div>
        </el-card>

        <!-- 最新资源 -->
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>🆕 最新资源</span>
              <el-link type="primary" @click="$router.push('/resources')">查看更多</el-link>
            </div>
          </template>
          <div v-loading="loading" class="resources-list">
            <div v-for="resource in latestResources" :key="resource.id" class="resource-item">
              <router-link :to="`/resources/${resource.id}`" class="resource-title">
                {{ resource.title }}
              </router-link>
              <div class="resource-meta">
                <el-tag size="small">{{ getResourceCategoryLabel(resource.category) }}</el-tag>
                <span class="meta-item">
                  <el-icon><User /></el-icon>
                  {{ resource.author.name }}
                </span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- AI助手入口 -->
        <el-card class="ai-assistant-card">
          <div class="ai-assistant-content">
            <el-icon class="ai-icon" :size="48"><ChatDotRound /></el-icon>
            <h3>AI助手</h3>
            <p>让AI帮你完善点子、生成标签、匹配资源</p>
            <el-button type="primary" @click="$router.push('/ai-assistant')">
              开始对话
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useIdeaStore } from '@/stores/idea'
import type { Idea } from '@/types'

const router = useRouter()
const ideaStore = useIdeaStore()

const loading = ref(false)
const hotIdeas = ref<Idea[]>([])
const latestResources = ref<any[]>([])
const stats = ref({
  ideasCount: 0,
  resourcesCount: 0,
  usersCount: 0,
  matchesCount: 0
})

const handleCreateIdea = () => {
  router.push('/ideas/create')
}

const handleBrowseIdeas = () => {
  router.push('/ideas')
}

const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    tool: '工具/应用',
    research: '研究/实验',
    startup: '创业/商业',
    learning: '学习/教育',
    creative: '创意/艺术',
    other: '其他'
  }
  return labels[category] || category
}

const getDifficultyLabel = (difficulty: string) => {
  const labels: Record<string, string> = {
    beginner: '入门级',
    intermediate: '中级',
    advanced: '高级',
    expert: '专家级'
  }
  return labels[difficulty] || difficulty
}

const getResourceCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    model: '模型/权重',
    dataset: '数据集',
    tool: '工具/框架',
    api: 'API服务',
    compute: '算力资源',
    funding: '资金支持',
    mentor: '导师/指导',
    other: '其他'
  }
  return labels[category] || category
}

onMounted(async () => {
  loading.value = true
  try {
    // 获取热门点子
    await ideaStore.fetchIdeas({ page: 1, pageSize: 5 })
    hotIdeas.value = ideaStore.ideas.slice(0, 5)

    // 模拟统计数据
    stats.value = {
      ideasCount: 128,
      resourcesCount: 256,
      usersCount: 1024,
      matchesCount: 89
    }

    // 模拟最新资源
    latestResources.value = [
      { id: 1, title: 'GPT-4 API访问权限', category: 'api', author: { name: '张三' } },
      { id: 2, title: '大规模中文数据集', category: 'dataset', author: { name: '李四' } },
      { id: 3, title: 'AI模型训练算力', category: 'compute', author: { name: '王五' } }
    ]
  } catch (error) {
    console.error('Failed to load home data:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-view {
  padding: 20px 0;
}

.welcome-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-bottom: 20px;
}

.welcome-banner h1 {
  margin: 0 0 10px 0;
  font-size: 32px;
}

.welcome-banner p {
  margin: 0 0 20px 0;
  font-size: 16px;
  opacity: 0.9;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.section-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ideas-list,
.resources-list {
  min-height: 200px;
}

.idea-item,
.resource-item {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.idea-item:last-child,
.resource-item:last-child {
  border-bottom: none;
}

.idea-title,
.resource-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  text-decoration: none;
  display: block;
  margin-bottom: 8px;
}

.idea-title:hover,
.resource-title:hover {
  color: #409eff;
}

.idea-meta,
.resource-meta {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
}

.idea-description {
  margin: 8px 0 0 0;
  font-size: 14px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.stats-card {
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.ai-assistant-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.ai-assistant-content {
  text-align: center;
  padding: 20px 0;
}

.ai-icon {
  margin-bottom: 12px;
}

.ai-assistant-content h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
}

.ai-assistant-content p {
  margin: 0 0 16px 0;
  font-size: 14px;
  opacity: 0.9;
}
</style>
