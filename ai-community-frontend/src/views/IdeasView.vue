<template>
  <div class="ideas-view">
    <div class="page-header">
      <h1>点子广场</h1>
      <el-button type="primary" @click="$router.push('/ideas/create')">
        <el-icon><Plus /></el-icon>
        发布点子
      </el-button>
    </div>

    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-select v-model="filters.category" placeholder="全部分类" clearable @change="handleFilter">
            <el-option label="全部分类" value="" />
            <el-option
              v-for="(label, key) in categoryOptions"
              :key="key"
              :label="label"
              :value="key"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filters.status" placeholder="全部状态" clearable @change="handleFilter">
            <el-option label="全部状态" value="" />
            <el-option
              v-for="(label, key) in statusOptions"
              :key="key"
              :label="label"
              :value="key"
            />
          </el-select>
        </el-col>
        <el-col :span="12">
          <el-input
            v-model="filters.search"
            placeholder="搜索点子..."
            clearable
            @clear="handleFilter"
            @keyup.enter="handleFilter"
          >
            <template #append>
              <el-button :icon="Search" @click="handleFilter" />
            </template>
          </el-input>
        </el-col>
      </el-row>
    </el-card>

    <div v-loading="ideaStore.loading" class="ideas-list">
      <el-empty v-if="ideaStore.ideas.length === 0 && !ideaStore.loading" description="暂无点子" />

      <el-card
        v-for="idea in ideaStore.ideas"
        :key="idea.id"
        class="idea-card"
        shadow="hover"
      >
        <div class="idea-header">
          <router-link :to="`/ideas/${idea.id}`" class="idea-title">
            {{ idea.title }}
          </router-link>
          <div class="idea-badges">
            <el-tag size="small">{{ categoryOptions[idea.category] }}</el-tag>
            <el-tag size="small" type="info">{{ difficultyOptions[idea.difficulty] }}</el-tag>
            <el-tag size="small" :type="getStatusType(idea.status)">
              {{ statusOptions[idea.status] }}
            </el-tag>
          </div>
        </div>

        <p class="idea-description">{{ idea.description }}</p>

        <div v-if="idea.tags.length > 0" class="idea-tags">
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

        <div class="idea-footer">
          <div class="idea-author">
            <el-avatar :size="24" :src="idea.author.avatar">
              {{ idea.author.name.charAt(0) }}
            </el-avatar>
            <span>{{ idea.author.name }}</span>
          </div>

          <div class="idea-stats">
            <span class="stat-item">
              <el-icon><View /></el-icon>
              {{ idea.viewsCount }}
            </span>
            <span class="stat-item">
              <el-icon><Star /></el-icon>
              {{ idea.likesCount }}
            </span>
            <span class="stat-item">
              <el-icon><User /></el-icon>
              {{ idea.followersCount }}
            </span>
            <span class="stat-item">
              {{ formatTime(idea.createdAt) }}
            </span>
          </div>
        </div>
      </el-card>
    </div>

    <div v-if="ideaStore.pagination.totalPages > 1" class="pagination">
      <el-pagination
        v-model:current-page="ideaStore.pagination.page"
        v-model:page-size="ideaStore.pagination.pageSize"
        :total="ideaStore.pagination.total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { useIdeaStore } from '@/stores/idea'

const ideaStore = useIdeaStore()

const filters = reactive({
  category: '',
  status: '',
  search: ''
})

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
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  return date.toLocaleDateString()
}

const handleFilter = () => {
  ideaStore.fetchIdeas({
    page: 1,
    category: filters.category || undefined,
    status: filters.status || undefined,
    search: filters.search || undefined
  })
}

const handlePageChange = () => {
  ideaStore.fetchIdeas({
    page: ideaStore.pagination.page,
    pageSize: ideaStore.pagination.pageSize,
    category: filters.category || undefined,
    status: filters.status || undefined,
    search: filters.search || undefined
  })
}

onMounted(() => {
  ideaStore.fetchIdeas()
})
</script>

<style scoped>
.ideas-view {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
}

.filter-card {
  margin-bottom: 20px;
}

.ideas-list {
  min-height: 400px;
}

.idea-card {
  margin-bottom: 16px;
}

.idea-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.idea-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  text-decoration: none;
  flex: 1;
  margin-right: 16px;
}

.idea-title:hover {
  color: #409eff;
}

.idea-badges {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.idea-description {
  margin: 0 0 12px 0;
  color: #606266;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.idea-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.idea-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.idea-author {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.idea-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>
