# Vue 前端集成到 Django 模板 - 完整指南

## ✅ 已完成

1. ✅ **Vite 配置已修改**：构建输出到 `static/vue/` 目录
2. ✅ **Django 模板已修改**：`templates/root.html` 已添加 Vue 挂载点
3. ✅ **main.ts 已修改**：支持从 `window.__INITIAL_STATE__` 读取 Django 数据
4. ✅ **构建脚本已创建**：`build-vue-frontend.bat`

---

## 🚀 使用方法

### 开发模式（推荐）

**方式一：同时运行 Django 和 Vite 开发服务器**

```powershell
# 终端 1：启动 Django 后端
cd "E:\Graduation Project\cs001\mediacms"
.\venv\Scripts\Activate.ps1
python manage.py runserver 0.0.0.0:8000
```

```powershell
# 终端 2：启动 Vue 前端开发服务器
cd "E:\Graduation Project\cs001\mediacms\frontend-vue"
npm run dev
```

**访问方式：**
- 访问 `http://localhost:8000`（Django 会通过模板加载 Vue 前端）
- Vite 开发服务器运行在 `http://localhost:8088`（用于热更新）

**工作原理：**
- Django 模板（`root.html`）在开发模式下会加载 `http://localhost:8088/src/main.ts`
- Vite 开发服务器提供热更新支持
- 前端修改会自动刷新

---

### 生产模式

**步骤 1：构建 Vue 前端**

```powershell
# 方式一：使用构建脚本（推荐）
cd "E:\Graduation Project\cs001\mediacms"
.\build-vue-frontend.bat

# 方式二：手动构建
cd frontend-vue
npm run build
```

**步骤 2：收集 Django 静态文件**

```powershell
cd "E:\Graduation Project\cs001\mediacms"
.\venv\Scripts\Activate.ps1
python manage.py collectstatic --noinput
```

**步骤 3：启动 Django 服务器**

```powershell
python manage.py runserver 0.0.0.0:8000
```

**访问方式：**
- 访问 `http://localhost:8000`（Django 会加载编译后的 Vue 静态文件）

---

## 📁 文件结构

构建后的文件结构：

```
mediacms/
├── static/
│   └── vue/                    # Vue 构建输出
│       ├── js/
│       │   ├── main.[hash].js
│       │   ├── element-plus.[hash].js
│       │   └── vue-vendor.[hash].js
│       ├── css/
│       │   └── main.[hash].css
│       └── assets/
│           └── images/
├── frontend-vue/
│   ├── src/
│   ├── dist/                  # Vite 构建输出（不使用）
│   └── vite.config.ts
└── templates/
    └── root.html              # Django 模板入口
```

---

## 🔧 配置说明

### Vite 配置（`frontend-vue/vite.config.ts`）

- **构建输出**：`outDir: '../static/vue'`
- **开发端口**：`port: 8088`
- **文件命名**：使用 hash 确保缓存更新

### Django 模板配置（`templates/root.html`）

**开发模式：**
```django
{% if DEBUG %}
    <script type="module" src="http://localhost:8088/@vite/client"></script>
    <script type="module" src="http://localhost:8088/src/main.ts"></script>
{% endif %}
```

**生产模式：**
```django
{% if not DEBUG %}
    <link rel="stylesheet" href="{% static 'vue/css/main.[hash].css' %}">
    <script type="module" src="{% static 'vue/js/main.[hash].js' %}"></script>
{% endif %}
```

---

## ⚠️ 注意事项

1. **开发模式**：
   - 必须同时运行 Django 和 Vite 开发服务器
   - 访问 `http://localhost:8000`（不是 8088）
   - Vite 开发服务器提供热更新

2. **生产模式**：
   - 必须先构建 Vue 前端：`npm run build`
   - 然后收集静态文件：`python manage.py collectstatic`
   - 构建后的文件会输出到 `static/vue/`

3. **Django 传递的数据**：
   - 用户信息：`window.__INITIAL_STATE__.user`
   - CSRF Token：`window.__INITIAL_STATE__.csrfToken`
   - 配置信息：`window.__INITIAL_STATE__.portalName` 等

4. **兼容性**：
   - 当前模板同时支持 React 和 Vue（React 内容被隐藏）
   - 可以逐步迁移，新旧系统并存

---

## 🎯 下一步

1. **测试开发模式**：
   ```powershell
   # 启动 Django
   python manage.py runserver 0.0.0.0:8000
   
   # 启动 Vue 开发服务器
   cd frontend-vue
   npm run dev
   
   # 访问 http://localhost:8000
   ```

2. **测试生产模式**：
   ```powershell
   # 构建 Vue 前端
   .\build-vue-frontend.bat
   
   # 收集静态文件
   python manage.py collectstatic --noinput
   
   # 启动 Django（设置 DEBUG=False）
   python manage.py runserver 0.0.0.0:8000
   
   # 访问 http://localhost:8000
   ```

3. **验证功能**：
   - ✅ Vue 前端正确加载
   - ✅ 路由正常工作
   - ✅ API 调用正常
   - ✅ 用户认证正常

---

## 📝 常见问题

**Q: 访问 http://localhost:8000 看不到 Vue 前端？**
A: 确保 Vite 开发服务器正在运行（`npm run dev`），并且访问的是 8000 端口。

**Q: 生产模式构建后文件找不到？**
A: 确保运行了 `python manage.py collectstatic`，并且 Django 的 `STATIC_ROOT` 配置正确。

**Q: 如何同时使用 React 和 Vue？**
A: 当前模板同时支持两者，React 内容被隐藏（`display: none`），可以逐步迁移。

---

完成！🎉

