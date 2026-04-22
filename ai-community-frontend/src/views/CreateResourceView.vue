<template>
  <div class="create-resource-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>发布资源</h2>
          <el-button @click="$router.back()">取消</el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="resourceForm"
        :rules="formRules"
        label-width="120px"
      >
        <el-form-item label="资源标题" prop="title">
          <el-input
            v-model="resourceForm.title"
            placeholder="请输入资源标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="资源分类" prop="category">
          <el-select v-model="resourceForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="(label, key) in categoryOptions"
              :key="key"
              :label="label"
              :value="key"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="访问方式" prop="accessType">
          <el-radio-group v-model="resourceForm.accessType">
            <el-radio
              v-for="(label, key) in accessTypeOptions"
              :key="key"
              :label="key"
            >
              {{ label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="详细描述" prop="description">
          <el-input
            v-model="resourceForm.description"
            type="textarea"
            :rows="6"
            placeholder="请详细描述你的资源..."
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="资源链接" prop="url">
          <el-input
            v-model="resourceForm.url"
            placeholder="请输入资源链接（可选）"
          />
        </el-form-item>

        <el-form-item label="使用说明" prop="usageGuide">
          <el-input
            v-model="resourceForm.usageGuide"
            type="textarea"
            :rows="4"
            placeholder="提供使用说明和指南..."
          />
        </el-form-item>

        <el-form-item label="限制条件" prop="limitations">
          <el-input
            v-model="resourceForm.limitations"
            type="textarea"
            :rows="3"
            placeholder="描述使用限制和注意事项..."
          />
        </el-form-item>

        <el-form-item label="标签" prop="tags">
          <div class="tags-wrapper">
            <el-tag
              v-for="tag in resourceForm.tags"
              :key="tag"
              closable
              @close="handleRemoveTag(tag)"
              style="margin-right: 8px; margin-bottom: 8px"
            >
              {{ tag }}
            </el-tag>
            <el-input
              v-if="inputVisible"
              ref="inputRef"
              v-model="inputValue"
              size="small"
              style="width: 100px"
              @keyup.enter="handleInputConfirm"
              @blur="handleInputConfirm"
            />
            <el-button
              v-else
              size="small"
              @click="showInput"
            >
              + 添加标签
            </el-button>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            发布资源
          </el-button>
          <el-button @click="handleSaveDraft">保存草稿</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import type { ResourceFormData } from '@/types'

const router = useRouter()

const formRef = ref<FormInstance>()
const loading = ref(false)
const inputVisible = ref(false)
const inputValue = ref('')
const inputRef = ref()

const resourceForm = reactive<ResourceFormData>({
  title: '',
  category: 'other',
  accessType: 'free',
  description: '',
  tags: [],
  url: '',
  usageGuide: '',
  limitations: ''
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

const accessTypeOptions = {
  free: '免费开放',
  freemium: '部分免费',
  paid: '付费',
  application: '申请制',
  invite: '邀请制'
}

const formRules: FormRules = {
  title: [
    { required: true, message: '请输入资源标题', trigger: 'blur' },
    { min: 5, max: 100, message: '标题长度在5到100个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择资源分类', trigger: 'change' }
  ],
  accessType: [
    { required: true, message: '请选择访问方式', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入详细描述', trigger: 'blur' },
    { min: 20, message: '描述至少需要20个字符', trigger: 'blur' }
  ]
}

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value && !resourceForm.tags.includes(inputValue.value)) {
    resourceForm.tags.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

const handleRemoveTag = (tag: string) => {
  const index = resourceForm.tags.indexOf(tag)
  if (index > -1) {
    resourceForm.tags.splice(index, 1)
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      // TODO: 调用API创建资源
      await new Promise(resolve => setTimeout(resolve, 1000))
      ElMessage.success('资源发布成功')
      router.push('/resources')
    } catch (error) {
      ElMessage.error('发布失败')
    } finally {
      loading.value = false
    }
  })
}

const handleSaveDraft = () => {
  ElMessage.info('草稿保存功能开发中...')
}
</script>

<style scoped>
.create-resource-view {
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}

.tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
</style>
