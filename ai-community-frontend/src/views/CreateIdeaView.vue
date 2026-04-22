<template>
  <div class="create-idea-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>发布点子</h2>
          <el-button @click="$router.back()">取消</el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="ideaForm"
        :rules="formRules"
        label-width="120px"
      >
        <el-form-item label="点子标题" prop="title">
          <el-input
            v-model="ideaForm.title"
            placeholder="请输入点子标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="点子分类" prop="category">
          <el-select v-model="ideaForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="(label, key) in categoryOptions"
              :key="key"
              :label="label"
              :value="key"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="难度等级" prop="difficulty">
          <el-radio-group v-model="ideaForm.difficulty">
            <el-radio
              v-for="(label, key) in difficultyOptions"
              :key="key"
              :label="key"
            >
              {{ label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="详细描述" prop="description">
          <div class="description-wrapper">
            <el-input
              v-model="ideaForm.description"
              type="textarea"
              :rows="8"
              placeholder="请详细描述你的点子..."
              maxlength="2000"
              show-word-limit
            />
            <el-button
              type="primary"
              text
              :loading="aiStore.loading"
              @click="handleOptimizeDescription"
              class="ai-optimize-btn"
            >
              <el-icon><MagicStick /></el-icon>
              AI优化
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="标签" prop="tags">
          <div class="tags-wrapper">
            <el-tag
              v-for="tag in ideaForm.tags"
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
            <el-button
              type="primary"
              text
              size="small"
              :loading="aiStore.loading"
              @click="handleGenerateTags"
              style="margin-left: 8px"
            >
              <el-icon><MagicStick /></el-icon>
              AI生成
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="所需资源" prop="neededResources">
          <el-input
            v-model="ideaForm.neededResources"
            type="textarea"
            :rows="4"
            placeholder="描述你需要什么资源来实现这个点子..."
          />
        </el-form-item>

        <el-form-item label="预期成果" prop="expectedOutcome">
          <el-input
            v-model="ideaForm.expectedOutcome"
            type="textarea"
            :rows="4"
            placeholder="描述你期望达成什么成果..."
          />
        </el-form-item>

        <el-form-item label="预计时间" prop="estimatedDays">
          <el-input-number
            v-model="ideaForm.estimatedDays"
            :min="0"
            :max="365"
            placeholder="天数"
          />
          <span style="margin-left: 8px; color: #909399">天</span>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="ideaStore.loading" @click="handleSubmit">
            发布点子
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
import { useIdeaStore } from '@/stores/idea'
import { useAIStore } from '@/stores/ai'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import type { IdeaFormData } from '@/types'

const router = useRouter()
const ideaStore = useIdeaStore()
const aiStore = useAIStore()

const formRef = ref<FormInstance>()
const inputVisible = ref(false)
const inputValue = ref('')
const inputRef = ref()

const ideaForm = reactive<IdeaFormData>({
  title: '',
  category: 'other',
  difficulty: 'beginner',
  description: '',
  tags: [],
  neededResources: '',
  expectedOutcome: '',
  estimatedDays: 0
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

const formRules: FormRules = {
  title: [
    { required: true, message: '请输入点子标题', trigger: 'blur' },
    { min: 5, max: 100, message: '标题长度在5到100个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择点子分类', trigger: 'change' }
  ],
  difficulty: [
    { required: true, message: '请选择难度等级', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入详细描述', trigger: 'blur' },
    { min: 20, message: '描述至少需要20个字符', trigger: 'blur' }
  ]
}

const handleOptimizeDescription = async () => {
  if (!ideaForm.title || !ideaForm.description) {
    ElMessage.warning('请先填写标题和描述')
    return
  }

  try {
    const response = await aiStore.optimizeIdea({
      title: ideaForm.title,
      category: categoryOptions[ideaForm.category],
      description: ideaForm.description,
      needed_resources: ideaForm.neededResources,
      expected_outcome: ideaForm.expectedOutcome
    })

    if (response.success && response.content) {
      await ElMessageBox.alert(response.content, 'AI优化建议', {
        confirmButtonText: '采用建议',
        cancelButtonText: '取消',
        type: 'info',
        dangerouslyUseHTMLString: true,
        showClose: true,
        closeOnClickModal: true,
        closeOnPressEscape: true
      }).then(() => {
        ideaForm.description = response.content!
        ElMessage.success('已采用AI优化建议')
      }).catch(() => {
        // 用户取消
      })
    } else {
      ElMessage.error(response.error || 'AI优化失败')
    }
  } catch (error) {
    console.error('AI优化失败:', error)
  }
}

const handleGenerateTags = async () => {
  if (!ideaForm.description) {
    ElMessage.warning('请先填写描述')
    return
  }

  try {
    const response = await aiStore.suggestTags(ideaForm.description, 'idea')

    if (response.success && response.content) {
      const tags = response.content.split(/[,，]/).map(tag => tag.trim()).filter(tag => tag)
      ideaForm.tags = [...new Set([...ideaForm.tags, ...tags])]
      ElMessage.success(`已生成 ${tags.length} 个标签`)
    } else {
      ElMessage.error(response.error || '标签生成失败')
    }
  } catch (error) {
    console.error('标签生成失败:', error)
  }
}

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value && !ideaForm.tags.includes(inputValue.value)) {
    ideaForm.tags.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

const handleRemoveTag = (tag: string) => {
  const index = ideaForm.tags.indexOf(tag)
  if (index > -1) {
    ideaForm.tags.splice(index, 1)
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    const result = await ideaStore.createIdea(ideaForm)
    if (result.success) {
      ElMessage.success('点子发布成功')
      router.push(`/ideas/${result.data?.id}`)
    } else {
      ElMessage.error(result.error || '发布失败')
    }
  })
}

const handleSaveDraft = async () => {
  ElMessage.info('草稿保存功能开发中...')
}
</script>

<style scoped>
.create-idea-view {
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

.description-wrapper {
  width: 100%;
  position: relative;
}

.ai-optimize-btn {
  position: absolute;
  top: 8px;
  right: 8px;
}

.tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
</style>
