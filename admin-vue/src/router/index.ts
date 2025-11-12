import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/layouts/AdminLayout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard/index.vue'),
        meta: { title: '仪表板', icon: 'DataAnalysis' }
      },
      {
        path: 'media',
        name: 'Media',
        redirect: '/media/list',
        meta: { title: '媒体管理', icon: 'VideoPlay' },
        children: [
          {
            path: 'list',
            name: 'MediaList',
            component: () => import('@/views/Media/List.vue'),
            meta: { title: '媒体列表' }
          },
          {
            path: 'detail/:token',
            name: 'MediaDetail',
            component: () => import('@/views/Media/Detail.vue'),
            meta: { title: '媒体详情', hidden: true }
          },
          {
            path: 'analytics',
            name: 'MediaAnalytics',
            component: () => import('@/views/Media/Analytics.vue'),
            meta: { title: '数据分析' }
          }
        ]
      },
      {
        path: 'users',
        name: 'Users',
        redirect: '/users/list',
        meta: { title: '用户管理', icon: 'User' },
        children: [
          {
            path: 'list',
            name: 'UserList',
            component: () => import('@/views/User/List.vue'),
            meta: { title: '用户列表' }
          },
          {
            path: 'detail/:id',
            name: 'UserDetail',
            component: () => import('@/views/User/Detail.vue'),
            meta: { title: '用户详情', hidden: true }
          }
        ]
      },
      {
        path: 'content',
        name: 'Content',
        redirect: '/content/comments',
        meta: { title: '内容管理', icon: 'ChatDotRound' },
        children: [
          {
            path: 'comments',
            name: 'Comments',
            component: () => import('@/views/Content/Comments.vue'),
            meta: { title: '评论管理' }
          },
          {
            path: 'reports',
            name: 'Reports',
            component: () => import('@/views/Content/Reports.vue'),
            meta: { title: '举报管理' }
          }
        ]
      },
      {
        path: 'system',
        name: 'System',
        redirect: '/system/settings',
        meta: { title: '系统管理', icon: 'Setting' },
        children: [
          {
            path: 'settings',
            name: 'Settings',
            component: () => import('@/views/System/Settings.vue'),
            meta: { title: '系统设置' }
          },
          {
            path: 'monitoring',
            name: 'Monitoring',
            component: () => import('@/views/System/Monitoring.vue'),
            meta: { title: '系统监控' }
          }
        ]
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/404.vue'),
    meta: { title: '404', hidden: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

  if (requiresAuth && !authStore.token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && authStore.token) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

// 设置页面标题
router.afterEach((to) => {
  document.title = `${to.meta.title || ''} - MediaCMS 管理后台`
})

export default router

