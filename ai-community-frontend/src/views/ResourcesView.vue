<template>
  <div class="resources-view">
    <div class="page-header">
      <h1>资源库</h1>
      <el-button type="primary" @click="$router.push('/resources/create')">
        <el-icon><Plus /></el-icon>
        发布资源
      </el-button>
    </div>

    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="8">
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
        <el-col :span="16">
          <el-input
            v-model="filters.search"
            placeholder="搜索资源..."
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

    <div v-loading="loading" class="resources-list">
      <el-empty v-if="resources.length === 0 && !loading" description="暂无资源" />

      <el-card
        v-for="resource in resources"
        :key="resource.id"
        class="resource-card"
        shadow="hover"
      >
        <div class="resource-header">
          <router-link :to="`/resources/${resource.id}`" class="resource-title">
            {{ resource.title }}
          </router-link>
          <el-tag size="small">{{ categoryOptions[resource.category] }}</el-tag>
        </div>

        <p class="resource-description">{{ resource.description }}</p>

        <div class="resource-footer">
          <div class="resource-author">
            <el-avatar :size="24" :src="resource.author.avatar">
              {{ resource.author.name.charAt(0) }}
            </el-avatar>
            <span>{{ resource.author.name }}</span>
          </div>

          <div class="resource-stats">
            <span class="stat-item">
              <el-icon><View /></el-icon>
              {{ resource.viewsCount }}
            </span>
            <span class="stat-item">
              <el-icon><Star /></el-icon>
              {{ resource.likesCount }}
            </span>
            <span class="stat-item">
              {{ formatTime(resource.createdAt) }}
            </span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'

const loading = ref(false)
const resources = ref<any[]>([])

const filters = reactive({
  category: '',
  search: ''
})

const categoryOptions = {
  model: '模型/权重',
  dataset: '数据集',
  tool: '工具/框架',
  api: 'API服务',
  compute: '算力资源',
  funding: '资金支持',
  mentor: '导师/指导',
  other: '其他'
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return date.toLocaleDateString()
}

const handleFilter = () => {
  // 实现筛选逻辑
  console.log('Filter:', filters)
}

onMounted(() => {
  // 模拟数据
  resources.value = [
    {
      id: 1,
      title: 'GPT-4 API访问权限',
      description: '提供GPT-4 API访问权限，可用于开发和测试AI应用。',
      category: 'api',
      author: { name: '张三', avatar: '' },
      viewsCount: 128,
      likesCount: 32,
      createdAt: new Date(Date.now() - 86400000).toISOString()
    },
    {
      id: 2,
      title: '大规模中文数据集',
      description: '包含100万条高质量的中文文本数据，适用于NLP任务训练。',
      category: 'dataset',
      author: { name: '李四', avatar: '' },
      viewsCount: 256,
      likesCount: 64,
      createdAt: new Date(Date.now() - 172800000).toISOString()
    }
  ]
})
</script>

<style scoped>
.resources-view {
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

.resources-list {
  min-height: 400px;
}

.resource-card {
  margin-bottom: 16px;
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.resource-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  text-decoration: none;
  flex: 1;
  margin-right: 16px;
}

.resource-title:hover {
  color: #409eff;
}

.resource-description {
  margin: 0 0 12px 0;
  color: #606266;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.resource-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.resource-author {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.resource-stats {
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
</style>
