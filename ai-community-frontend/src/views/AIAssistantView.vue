<template>
  <div class="ai-assistant-view">
    <el-row :gutter="20">
      <!-- 左侧对话列表 -->
      <el-col :span="6">
        <el-card class="conversations-card">
          <template #header>
            <div class="card-header">
              <span>对话历史</span>
              <el-button
                type="primary"
                size="small"
                @click="handleNewConversation"
              >
                <el-icon><Plus /></el-icon>
                新对话
              </el-button>
            </div>
          </template>

          <div class="conversations-list">
            <div
              v-for="conversation in aiStore.conversations"
              :key="conversation.id"
              :class="[
                'conversation-item',
                { active: conversation.id === aiStore.currentConversationId }
              ]"
              @click="aiStore.selectConversation(conversation.id)"
            >
              <div class="conversation-title">{{ conversation.title }}</div>
              <div class="conversation-time">
                {{ formatTime(conversation.updatedAt) }}
              </div>
              <el-button
                type="danger"
                size="small"
                text
                @click.stop="handleDeleteConversation(conversation.id)"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧对话区域 -->
      <el-col :span="18">
        <el-card class="chat-card">
          <template #header>
            <div class="card-header">
              <div class="model-selector">
                <el-select
                  v-model="aiStore.selectedModel"
                  placeholder="选择模型"
                  @change="handleModelChange"
                >
                  <el-option
                    v-for="model in aiStore.availableModels"
                    :key="model.id"
                    :label="model.name"
                    :value="model.id"
                  >
                    <div class="model-option">
                      <span>{{ model.name }}</span>
                      <span class="model-provider">{{ model.provider }}</span>
                    </div>
                  </el-option>
                </el-select>
              </div>
              <div class="chat-actions">
                <el-button size="small" @click="handleClearHistory">
                  <el-icon><Delete /></el-icon>
                  清空对话
                </el-button>
              </div>
            </div>
          </template>

          <div class="chat-container">
            <!-- 消息列表 -->
            <div class="messages" ref="messagesContainer">
              <div v-if="!aiStore.currentConversation || aiStore.currentConversation.messages.length === 0"
                   class="empty-state">
                <el-icon :size="64"><ChatDotRound /></el-icon>
                <h3>开始新的对话</h3>
                <p>我可以帮你优化点子、生成标签、分析匹配度等</p>
              </div>

              <div
                v-for="message in aiStore.currentConversation?.messages"
                :key="message.id"
                :class="['message', message.role]"
              >
                <div class="message-avatar">
                  <el-avatar v-if="message.role === 'user'" :size="32">
                    {{ userStore.user?.name?.charAt(0) }}
                  </el-avatar>
                  <el-icon v-else :size="32"><ChatDotRound /></el-icon>
                </div>
                <div class="message-content">
                  <div class="message-text">{{ message.content }}</div>
                  <div class="message-time">{{ formatTime(message.timestamp) }}</div>
                </div>
              </div>

              <!-- 加载状态 -->
              <div v-if="aiStore.loading" class="message assistant">
                <div class="message-avatar">
                  <el-icon :size="32"><ChatDotRound /></el-icon>
                </div>
                <div class="message-content">
                  <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 输入区域 -->
            <div class="input-area">
              <el-input
                v-model="inputMessage"
                type="textarea"
                :rows="3"
                placeholder="输入你的问题或需求..."
                @keydown.enter.ctrl="handleSendMessage"
                :disabled="aiStore.loading"
              />
              <div class="input-actions">
                <span class="hint">按 Ctrl + Enter 发送</span>
                <el-button
                  type="primary"
                  :loading="aiStore.loading"
                  @click="handleSendMessage"
                >
                  发送
                  <el-icon><Position /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useAIStore } from '@/stores/ai'
import { useUserStore } from '@/stores/user'
import { ElMessageBox } from 'element-plus'

const aiStore = useAIStore()
const userStore = useUserStore()

const inputMessage = ref('')
const messagesContainer = ref<HTMLElement>()

const handleNewConversation = () => {
  aiStore.createConversation()
}

const handleDeleteConversation = async (id: string) => {
  try {
    await ElMessageBox.confirm('确定要删除这个对话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    aiStore.deleteConversation(id)
  } catch {
    // 用户取消
  }
}

const handleSendMessage = async () => {
  if (!inputMessage.value.trim() || aiStore.loading) return

  const message = inputMessage.value
  inputMessage.value = ''

  await aiStore.sendMessage(message)

  await nextTick()
  scrollToBottom()
}

const handleModelChange = (modelId: string) => {
  aiStore.selectModel(modelId)
}

const handleClearHistory = async () => {
  try {
    await ElMessageBox.confirm('确定要清空当前对话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    if (aiStore.currentConversationId) {
      aiStore.deleteConversation(aiStore.currentConversationId)
      aiStore.createConversation()
    }
  } catch {
    // 用户取消
  }
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

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 监听消息变化，自动滚动到底部
watch(() => aiStore.currentConversation?.messages.length, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

onMounted(async () => {
  await aiStore.initialize()
})
</script>

<style scoped>
.ai-assistant-view {
  height: calc(100vh - 200px);
}

.conversations-card,
.chat-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.conversations-list {
  max-height: calc(100vh - 320px);
  overflow-y: auto;
}

.conversation-item {
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 8px;
  border: 1px solid transparent;
}

.conversation-item:hover {
  background: #f5f7fa;
}

.conversation-item.active {
  background: #ecf5ff;
  border-color: #409eff;
}

.conversation-title {
  font-weight: 500;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-time {
  font-size: 12px;
  color: #909399;
}

.model-selector {
  width: 200px;
}

.model-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.model-provider {
  font-size: 12px;
  color: #909399;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 320px);
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 16px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

.empty-state h3 {
  margin: 16px 0 8px 0;
}

.empty-state p {
  margin: 0;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
}

.message-text {
  background: white;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.message.user .message-text {
  background: #409eff;
  color: white;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.message.user .message-time {
  text-align: right;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #409eff;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.input-area {
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.hint {
  font-size: 12px;
  color: #909399;
}
</style>
