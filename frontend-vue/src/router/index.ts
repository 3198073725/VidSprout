import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/Home.vue') },
    { path: '/login', name: 'login', component: () => import('../views/Login.vue') },
    { path: '/register', name: 'register', component: () => import('../views/Register.vue') },
    
    // 媒体管理
    { path: '/media/:token', name: 'media-detail', component: () => import('../views/MediaDetail.vue'), props: true },
    { path: '/media/:token/edit', name: 'media-edit', component: () => import('../views/MediaEdit.vue'), props: true, meta: { requiresAuth: true } },
    { path: '/media/:token/video/edit', name: 'video-edit', component: () => import('../views/VideoEdit.vue'), props: true, meta: { requiresAuth: true } },
    { path: '/media/:token/chapters/edit', name: 'chapters-edit', component: () => import('../views/ChaptersEdit.vue'), props: true, meta: { requiresAuth: true } },
    { path: '/media/:token/publish', name: 'media-publish', component: () => import('../views/MediaPublish.vue'), props: true, meta: { requiresAuth: true } },
    { path: '/media/:token/subtitle/add', name: 'subtitle-add', component: () => import('../views/SubtitleAdd.vue'), props: true, meta: { requiresAuth: true } },
    { path: '/media/:token/subtitle/:subtitleId/edit', name: 'subtitle-edit', component: () => import('../views/SubtitleEdit.vue'), props: true, meta: { requiresAuth: true } },
    { path: '/upload', name: 'upload', component: () => import('../views/Upload.vue'), meta: { requiresAuth: true } },
    { path: '/screen-record', name: 'screen-record', component: () => import('../views/ScreenRecord.vue'), meta: { requiresAuth: true } },
    
    // 媒体列表
    { path: '/latest', name: 'latest', component: () => import('../views/Latest.vue') },
    { path: '/featured', name: 'featured', component: () => import('../views/Featured.vue') },
    { path: '/recommended', name: 'recommended', component: () => import('../views/Recommended.vue') },
    
    // 分类和标签
    { path: '/tags', name: 'tags', component: () => import('../views/Tags.vue') },
    { path: '/categories', name: 'categories', component: () => import('../views/Categories.vue') },
    { path: '/search', name: 'search', component: () => import('../views/Search.vue') },
    
    // 用户相关
    { path: '/history', name: 'history', component: () => import('../views/History.vue'), meta: { requiresAuth: true } },
    { path: '/liked', name: 'liked', component: () => import('../views/Liked.vue'), meta: { requiresAuth: true } },
    { path: '/me', name: 'me', component: () => import('../views/Me.vue'), meta: { requiresAuth: true } },
    { path: '/user/:username', name: 'user-profile', component: () => import('../views/UserProfile.vue'), props: true },
    { path: '/user/:username/edit', name: 'user-edit', component: () => import('../views/UserEdit.vue'), props: true, meta: { requiresAuth: true } },
    { path: '/user/:username/about', name: 'user-about', component: () => import('../views/UserAbout.vue'), props: true },
    { path: '/user/:username/playlists', name: 'user-playlists', component: () => import('../views/UserPlaylists.vue'), props: true },
    { path: '/user/:username/shared-by-me', name: 'user-shared-by-me', component: () => import('../views/UserSharedByMe.vue'), props: true, meta: { requiresAuth: true } },
    { path: '/user/:username/shared-with-me', name: 'user-shared-with-me', component: () => import('../views/UserSharedWithMe.vue'), props: true, meta: { requiresAuth: true } },
    
    // 播放列表
    { path: '/playlists', name: 'playlists', component: () => import('../views/Playlists.vue'), meta: { requiresAuth: true } },
    { path: '/playlists/:token', name: 'playlist-detail', component: () => import('../views/PlaylistDetail.vue'), props: true },
    
    // 密码管理
    { path: '/password-change', name: 'password-change', component: () => import('../views/PasswordChange.vue'), meta: { requiresAuth: true } },
    { path: '/password-reset', name: 'password-reset', component: () => import('../views/PasswordReset.vue') },
    { path: '/password-reset/done', name: 'password-reset-done', component: () => import('../views/PasswordResetDone.vue') },
    { path: '/password-reset/confirm/:token', name: 'password-reset-confirm', component: () => import('../views/PasswordResetConfirm.vue'), props: true },
    { path: '/password-reset/complete', name: 'password-reset-complete', component: () => import('../views/PasswordResetComplete.vue') },
    { path: '/password-set', name: 'password-set', component: () => import('../views/PasswordSet.vue') },
    
    // 邮箱管理
    { path: '/email', name: 'email-manage', component: () => import('../views/EmailManage.vue'), meta: { requiresAuth: true } },
    { path: '/email/confirm/:key', name: 'email-confirm', component: () => import('../views/EmailConfirm.vue'), props: true },
    { path: '/email/verification-sent', name: 'verification-sent', component: () => import('../views/VerificationSent.vue') },
    { path: '/email/verify-required', name: 'email-verify-required', component: () => import('../views/EmailVerifyRequired.vue') },
    
    // 用户状态页面
    { path: '/user/needs-approval', name: 'user-needs-approval', component: () => import('../views/UserNeedsApproval.vue'), meta: { requiresAuth: true } },
    { path: '/account/inactive', name: 'account-inactive', component: () => import('../views/AccountInactive.vue') },
    { path: '/signup/closed', name: 'signup-closed', component: () => import('../views/SignupClosed.vue') },
    
    // 社区功能
    { path: '/members', name: 'members', component: () => import('../views/Members.vue') },
    
    // 管理后台
    { path: '/admin/media', name: 'admin-media', component: () => import('../views/admin/ManageMedia.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/comments', name: 'admin-comments', component: () => import('../views/admin/ManageComments.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/users', name: 'admin-users', component: () => import('../views/admin/ManageUsers.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/tasks', name: 'admin-tasks', component: () => import('../views/admin/ManageTasks.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    
    // 嵌入播放器
    { path: '/embed', name: 'embed', component: () => import('../views/Embed.vue') },
    
    // 认证相关（删除重复的login和register路由）
    { path: '/login-selector', name: 'login-selector', component: () => import('../views/CustomLoginSelector.vue') },
    { path: '/logout', name: 'logout', component: () => import('../views/Logout.vue') },
    { path: '/auth-debug', name: 'auth-debug', component: () => import('../views/AuthDebug.vue') },
    
    // 频道管理
    { path: '/channel/:id/edit', name: 'channel-edit', component: () => import('../views/ChannelEdit.vue'), props: true, meta: { requiresAuth: true } },
    
    // 静态页面
    { path: '/about', name: 'about', component: () => import('../views/About.vue') },
    { path: '/terms', name: 'terms', component: () => import('../views/Terms.vue') },
    { path: '/contact', name: 'contact', component: () => import('../views/Contact.vue') },
    { path: '/page/:slug', name: 'page', component: () => import('../views/Page.vue'), props: true },
    
    // 404错误页面 - 必须放在最后
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFound.vue') },
  ],
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  
  // 如果认证状态未初始化，先初始化
  if (!auth.isInitialized) {
    await auth.initializeAuth()
  }
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }
  
  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    next({ name: 'home' })
    return
  }
  
  next()
})

export default router
