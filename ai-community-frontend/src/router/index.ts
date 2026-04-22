import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/ideas',
    name: 'Ideas',
    component: () => import('@/views/IdeasView.vue'),
    meta: { title: '点子广场' }
  },
  {
    path: '/ideas/:id',
    name: 'IdeaDetail',
    component: () => import('@/views/IdeaDetailView.vue'),
    meta: { title: '点子详情' }
  },
  {
    path: '/ideas/create',
    name: 'CreateIdea',
    component: () => import('@/views/CreateIdeaView.vue'),
    meta: { title: '发布点子', requiresAuth: true }
  },
  {
    path: '/resources',
    name: 'Resources',
    component: () => import('@/views/ResourcesView.vue'),
    meta: { title: '资源库' }
  },
  {
    path: '/resources/:id',
    name: 'ResourceDetail',
    component: () => import('@/views/ResourceDetailView.vue'),
    meta: { title: '资源详情' }
  },
  {
    path: '/resources/create',
    name: 'CreateResource',
    component: () => import('@/views/CreateResourceView.vue'),
    meta: { title: '发布资源', requiresAuth: true }
  },
  {
    path: '/ai-assistant',
    name: 'AIAssistant',
    component: () => import('@/views/AIAssistantView.vue'),
    meta: { title: 'AI助手' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { title: '个人中心', requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: { title: '设置', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: '页面不存在' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title as string} - AI交流社区`

  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
      return
    }
  }

  next()
})

export default router
