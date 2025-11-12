import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { visualizer } from 'rollup-plugin-visualizer'
import compression from 'vite-plugin-compression'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    // 自动导入组件
    Components({
      resolvers: [ElementPlusResolver()],
      dts: true,
      dirs: ['src/components'],
      extensions: ['vue'],
      deep: true
    }),
    // 自动导入API
    AutoImport({
      imports: ['vue', 'vue-router', 'pinia'],
      dts: true,
      dirs: ['src/composables', 'src/stores'],
      resolvers: [ElementPlusResolver()]
    }),
    // 压缩
    compression({
      algorithm: 'gzip',
      ext: '.gz',
      threshold: 10240, // 10KB
      deleteOriginFile: false
    }),
    // 打包分析
    visualizer({
      open: false,
      gzipSize: true,
      brotliSize: true
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    // 输出到 Django static 目录
    outDir: '../static/vue',
    emptyOutDir: true,
    // 代码分割配置
    rollupOptions: {
      input: {
        main: './src/main.ts'
      },
      output: {
        manualChunks: {
          // 第三方库分割
          'element-plus': ['element-plus'],
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'utils': ['axios', 'sortablejs', 'hls.js'],
          // 按页面分割
          'admin': [
            './src/views/admin/ManageUsers.vue',
            './src/views/admin/ManageMedia.vue',
            './src/views/admin/ManageComments.vue'
          ],
          'media': [
            './src/views/MediaDetail.vue',
            './src/components/CommentSection.vue'
          ],
          'search': [
            './src/views/Search.vue',
            './src/components/SearchSuggestions.vue'
          ]
        },
        // 优化chunk文件名 - 符合 Django 静态文件结构
        entryFileNames: 'js/[name].[hash].js',
        chunkFileNames: 'js/[name].[hash].js',
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name?.split('.') || []
          const ext = info[info.length - 1]
          if (/\.(png|jpe?g|svg|gif|webp|ico)$/.test(assetInfo.name || '')) {
            return 'assets/images/[name].[hash][extname]'
          } else if (/\.css$/.test(assetInfo.name || '')) {
            return 'css/[name].[hash][extname]'
          }
          return 'assets/[name].[hash][extname]'
        }
      }
    },
    // 启用代码压缩
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },
    // 启用CSS代码分割
    cssCodeSplit: true,
    // 启用sourcemap
    sourcemap: process.env.NODE_ENV !== 'production'
  },
  server: {
    port: 8088, // 开发模式端口（与 React 一致）
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      // 媒体文件代理
      '^/media/(encoded|original|userlogos|thumbnails|hls)': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/admin': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/accounts': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/fu': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    }
  },
  // 优化依赖预构建
  optimizeDeps: {
    include: [
      'vue',
      'vue-router',
      'pinia',
      'element-plus',
      'axios',
      'hls.js',
      'sortablejs'
    ]
  }
})
