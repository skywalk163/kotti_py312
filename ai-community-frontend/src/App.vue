<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <div class="logo">
          <router-link to="/">AI交流社区</router-link>
        </div>
        <nav class="nav-menu">
          <router-link to="/" class="nav-item">首页</router-link>
          <router-link to="/ideas" class="nav-item">点子广场</router-link>
          <router-link to="/resources" class="nav-item">资源库</router-link>
          <router-link to="/ai-assistant" class="nav-item">AI助手</router-link>
        </nav>
        <div class="user-actions">
          <template v-if="userStore.isLoggedIn">
            <el-dropdown>
              <span class="user-info">
                <el-avatar :size="32" :src="userStore.user?.avatar">
                  {{ userStore.user?.name?.charAt(0) }}
                </el-avatar>
                <span>{{ userStore.user?.name }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="router.push('/profile')">
                    个人中心
                  </el-dropdown-item>
                  <el-dropdown-item @click="router.push('/settings')">
                    设置
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="primary" @click="router.push('/login')">
              登录
            </el-button>
            <el-button @click="router.push('/register')">
              注册
            </el-button>
          </template>
        </div>
      </div>
    </el-header>

    <el-main class="app-main">
      <router-view />
    </el-main>

    <el-footer class="app-footer">
      <div class="footer-content">
        <p>&copy; 2024 AI交流社区 - 点子共享，实践落地</p>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  height: 64px;
  display: flex;
  align-items: center;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo a {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 24px;
}

.nav-item {
  color: #606266;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: #409eff;
}

.user-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.app-main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  background: #f5f7fa;
  text-align: center;
  padding: 20px;
  margin-top: auto;
}

.footer-content {
  color: #909399;
  font-size: 14px;
}
</style>
