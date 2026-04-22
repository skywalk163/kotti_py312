<template>
  <div class="idea-detail-view">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else-if="idea">
      <el-card class="detail-card">
        <div class="idea-header">
          <h1>{{ idea.title }}</h1>
          <div class="idea-badges">
            <el-tag>{{ categoryOptions[idea.category] }}</el-tag>
            <el-tag type="info">{{ difficultyOptions[idea.difficulty] }}</el-tag>
            <el-tag :type="getStatusType(idea.status)">
              {{ statusOptions[idea.status] }}
            </el-tag>
          </div>
        </div>

        <div class="idea-meta">
          <div class="author-info">
            <el-avatar :size="40" :src="idea.author.avatar">
              {{ idea.author.name.charAt(0) }}
            </el-avatar>
            <div class="author-details">
              <div class="author-name">{{ idea.author.name }}</div>
              <div class="publish-time">{{ formatTime(idea.createdAt) }}</div>
            </div>
          </div>

          <div class="idea-actions">
            <el-button @click="handleLike">
              <el-icon><Star /></el-icon>
              {{ idea.likesCount }}
            </el-button>
            <el-button @click="handleFollow">
              <el-icon><User /></el-icon>
              {{ idea.followersCount }}
            </el-button>
            <el-button @click="handleShare">
              <el-icon><Share /></el-icon>
              分享
            </el-button>
          </div>
        </div>
      </el-card>

      <el-row :gutter="20">
        <el-col :span="16">
          <el-card class="content-card">
            <div class="section">
              <h3>详细描述</h3>
              <div class="content-text">{{ idea.description }}</div>
            </div>

            <div v-if="idea.tags.length > 0" class="section">
              <h3>标签</h3>
              <div class="tags-container">
                <el-tag
                  v-for="tag in idea.tags"
                  :key="tag"
                  size="small"
                  type="info"
                  effect="plain"
                >
                  {{ tag }}
                </el-tag>
              </div>
            </div>

            <div v-if="idea.neededResources" class="section">
              <h3>所需资源</h3>
              <div class="content-text">{{ idea.neededResources }}</div>
            </div>

            <div v-if="idea.expectedOutcome" class="section">
              <h3>预期成果</h3>
              <div class="content-text">{{ idea.expectedOutcome }}</div>
            </div>

            <div v-if="idea.estimatedDays > 0" class="section">
              <h3>预计时间</h3>
              <div class="content-text">{{ idea.estimatedDays }} 天</div>
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="stats-card">
            <template #header>
              <span>统计信息</span>
            </template>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ idea.viewsCount }}</div>
                <div class="stat-label">浏览</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ idea.likesCount }}</div>
                <div class="stat-label">点赞</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ idea.followersCount }}</div>
                <div class="stat-label">关注</div>
              </div>
            </div>
          </el-card>

          <el-card class="ai-card">
            <template #header>
              <span>AI分析</span>
            </template>
            <el-button type="primary" @click="handleAIAnalyze" :loading="aiLoading">
              <el-icon><MagicStick /></el-icon>
              获取AI建议
            </el-button>
            <div v-if="aiSuggestions" class="ai-suggestions">
              <div class="suggestions-text">{{ aiSuggestions }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-empty v-else description="点子不存在" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useIdeaStore } from '@/stores/idea'
import { useAIStore } from '@/stores/ai'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const ideaStore = useIdeaStore()
const aiStore = useAIStore()

const loading = ref(true)
const aiLoading = ref(false)
const aiSuggestions = ref('')

const idea = ref(ideaStore.currentIdea)

const categoryOptions = {
  tool: '工具/应用',
  research: '研究/实验',
  startup: '创业/商业',
  learning: '学习/教育',
  creative: '创意/艺术',
  other: '其他'
}

const difficultyOptions = {
  beginner: '入门级',
  intermediate: '中级',
  advanced: '高级',
  expert: '专家级'
}

const statusOptions = {
  draft: '草稿',
  brainstorming: '构思中',
  recruiting: '招募中',
  in_progress: '进行中',
  completed: '已完成',
  archived: '已归档'
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    draft: 'info',
    brainstorming: 'warning',
    recruiting: 'danger',
    in_progress: 'primary',
    completed: 'success',
    archived: 'info'
  }
  return typeMap[status] || 'info'
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN')
}

const handleLike = async () => {
  if (idea.value) {
    await ideaStore.likeIdea(idea.value.id)
  }
}

const handleFollow = async () => {
  if (idea.value) {
    await ideaStore.followIdea(idea.value.id)
  }
}

const handleShare = () => {
  ElMessage.info('分享功能开发中...')
}

const handleAIAnalyze = async () => {
  if (!idea.value) return

  aiLoading.value = true
  try {
    const response = await aiStore.optimizeIdea({
      title: idea.value.title,
      category: categoryOptions[idea.value.category],
      description: idea.value.description,
      needed_resources: idea.value.neededResources,
      expected_outcome: idea.value.expectedOutcome
    })

    if (response.success && response.content) {
      aiSuggestions.value = response.content
    } else {
      ElMessage.error(response.error || 'AI分析失败')
    }
  } catch (error) {
    console.error('AI分析失败:', error)
  } finally {
    aiLoading.value = false
  }
}

onMounted(async () => {
  const id = Number(route.params.id)
  if (id) {
    await ideaStore.fetchIdeaById(id)
    idea.value = ideaStore.currentIdea
    loading.value = false
  }
})
</script>

<style scoped>
.idea-detail-view {
  padding: 20px 0;
}

.loading-container {
  padding: 20px;
}

.detail-card {
  margin-bottom: 20px;
}

.idea-header {
  margin-bottom: 20px;
}

.idea-header h1 {
  margin: 0 0 16px 0;
  font-size: 28px;
  color: #303133;
}

.idea-badges {
  display: flex;
  gap: 8px;
}

.idea-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-details {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 500;
  color: #303133;
}

.publish-time {
  font-size: 13px;
  color: #909399;
}

.idea-actions {
  display: flex;
  gap: 8px;
}

.content-card {
  margin-bottom: 20px;
}

.section {
  margin-bottom: 24px;
}

.section h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  color: #303133;
}

.content-text {
  color: #606266;
  line-height: 1.8;
  white-space: pre-wrap;
}

.tags-container {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.stats-card,
.ai-card {
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

.ai-suggestions {
  margin-top: 16px;
  padding: 12px;
  background: #f0f9ff;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.suggestions-text {
  color: #606266;
  line-height: 1.6;
  white-space: pre-wrap;
}
</style>
