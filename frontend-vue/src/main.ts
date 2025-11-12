import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// MediaCMS 样式
import './styles/variables.css'
import './styles/base.css'
import './styles/mediacms/index.css'
import './assets/theme.css'
  
// 扩展 Window 接口类型
declare global {
  interface Window {
    __INITIAL_STATE__?: {
      portalName?: string
      frontendHost?: string
      useRoundedCorners?: boolean
      loadFromCdn?: boolean
      user?: {
        id: number
        username: string
        email: string
        isStaff: boolean
        isSuperuser: boolean
      } | null
      csrfToken?: string
    }
    gtag?: (command: string, action: string, options?: Record<string, unknown>) => void
    registration?: ServiceWorkerRegistration
  }
  
  var process: {
    env: {
      NODE_ENV: 'development' | 'production' | 'test'
    }
  }
  
  type NodeJSTimeout = number
  
  interface PerformanceEntry {
    initiatorType?: string
  }
  
  interface ServiceWorkerRegistration {
    sync?: {
      register: (tag: string) => Promise<void>
    }
  }
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 挂载应用
app.mount('#app')
