# 提示词管理系统 - 项目文档

## 1. 项目概览

本项目是一个功能完整的全栈Web应用，旨在提供一个高效、直观的提示词（Prompts）和模块（Modules）管理平台。它采用前后端分离的架构，后端使用轻量级的 Python Flask 框架，前端则基于现代化的 Vue.js 3 构建。

### 1.1. 技术栈

- **后端**:
  - **Python 3**: 主要编程语言。
  - **Flask**: 轻量级 Web 框架，用于构建 RESTful API。
  - **SQLite**: 文件型数据库，用于数据持久化存储，无需额外配置。
  - **Flask-CORS**: 处理跨域资源共享。

- **前端**:
  - **Vue.js 3**: 渐进式 JavaScript 框架，使用组合式 API (`<script setup>`)。
  - **TypeScript**: 为 JavaScript 添加静态类型，增强代码的可维护性。
  - **Vite**: 新一代前端构建工具，提供极速的开发服务器和打包体验。
  - **Pinia**: Vue 的官方状态管理库，用于集中管理应用状态。
  - **Tailwind CSS**: 一个功能类优先的 CSS 框架，用于快速构建美观的界面。
  - **Fetch API**: 用于与后端进行 HTTP 通信。

### 1.2. 核心功能

- **提示词管理**: 对提示词进行创建、读取、更新和删除（CRUD）操作。
- **模块管理**: 对可复用的功能模块进行 CRUD 操作。
- **响应式布局**: 界面在桌面和移动设备上均有良好表现。
- **动态数据交互**: 前端数据与后端实时同步，无需刷新页面。
- **清晰的状态管理**: 通过 Pinia 统一管理应用状态，如加载中、错误信息等。

## 2. 快速启动指南

### 2.1. 环境要求
- Python 3.7+
- Node.js 16+ (及 npm)

### 2.2. 后端启动
在项目根目录下运行以下命令：

```bash
# 使用推荐的启动脚本（它会自动检查并安装依赖）
python start_backend.py
```
后端服务将在 `http://localhost:5000` 启动。数据库文件 `prompts.db` 会在根目录自动创建。

### 2.3. 前端启动
打开一个新的终端，进入前端项目目录：

```bash
# 进入前端目录
cd prompt-management-app

# 安装依赖 (仅首次需要)
npm install

# 启动开发服务器
npm run dev
```
前端开发服务器将在 `http://localhost:5173` (或另一个可用端口) 启动。

## 3. 项目结构解析

```
/
├── app.py                    # ✅ Flask 后端主应用，包含所有 API 路由
├── start_backend.py          # 🐍 后端启动脚本，简化启动流程
├── requirements.txt          # 📦 Python 依赖包列表
├── prompts.db                # 🗃️ SQLite 数据库文件 (自动生成)
├── README.md                 # 📄 简版说明文档
├── Claude.md                 # 📖 详细项目文档 (本文档)
└── prompt-management-app/    # 🎨 Vue.js 前端应用
    ├── public/               # 静态资源目录
    ├── src/
    │   ├── assets/           # 样式、图片等资源
    │   ├── components/       # 🧩 可复用的 Vue 组件
    │   │   ├── Modal.vue
    │   │   ├── ModuleForm.vue
    │   │   └── PromptForm.vue
    │   ├── layouts/          # 🏗️ 布局组件
    │   │   └── DefaultLayout.vue
    │   ├── router/           # 🚦 路由配置
    │   │   └── index.ts
    │   ├── services/         # 📡 API 服务层
    │   │   └── api.ts
    │   ├── stores/           # 🗄️ Pinia 状态管理
    │   │   └── index.ts
    │   ├── views/            # 📄 页面级组件
    │   │   ├── HomeView.vue
    │   │   ├── ModuleListView.vue
    │   │   └── PromptListView.vue
    │   ├── App.vue           # 根组件
    │   └── main.ts           # 应用入口文件
    ├── index.html            # 主 HTML 文件
    ├── package.json          # Node.js 项目配置与依赖
    └── ... (配置文件如 vite.config.ts, tsconfig.json 等)
```

## 4. 后端 API 文档 (Flask)

后端 API 设计遵循 RESTful 原则，所有数据交换均使用 JSON 格式。

### 4.1. 通用错误处理

- **`400 Bad Request`**: 请求格式错误、缺少必要参数或参数值无效。
- **`404 Not Found`**: 请求的资源不存在。
- **`500 Internal Server Error`**: 服务器内部发生未知错误。

### 4.2. 提示词 API (`/api/prompts`)

#### **GET /api/prompts**
- **描述**: 获取所有提示词列表，按创建时间降序排列。
- **请求**: 无
- **成功响应 (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "title": "创意写作助手",
      "content": "帮我写一个故事...",
      "category": "写作",
      "tags": "创意,故事",
      "created_at": "...",
      "updated_at": "..."
    }
  ]
  ```

#### **POST /api/prompts**
- **描述**: 创建一个新的提示词。
- **请求体 (JSON)**:
  - `title` 或 `name` (string, required): 提示词标题。
  - `content` (string, required): 提示词内容。
  - `category` (string, optional): 分类。
  - `tags` (string or array, optional): 标签。可以是逗号分隔的字符串，也可以是字符串数组。
- **成功响应 (201 Created)**:
  ```json
  {
    "id": 2,
    "message": "提示词创建成功"
  }
  ```

#### **PUT /api/prompts/<int:prompt_id>**
- **描述**: 更新一个已存在的提示词。只更新请求体中提供的字段。
- **请求体 (JSON)**: 与 POST 请求类似，但所有字段都是可选的。
- **成功响应 (200 OK)**:
  ```json
  {
    "message": "提示词更新成功"
  }
  ```

#### **DELETE /api/prompts/<int:prompt_id>**
- **描述**: 删除一个指定的提示词。
- **请求**: 无
- **成功响应 (200 OK)**:
  ```json
  {
    "message": "提示词删除成功"
  }
  ```

### 4.3. 模块 API (`/api/modules`)

模块 API 的结构与提示词 API 非常相似，提供完整的 CRUD 功能。

#### **GET /api/modules**
- **描述**: 获取所有模块列表。

#### **POST /api/modules**
- **描述**: 创建一个新模块。
- **请求体 (JSON)**:
  - `name` (string, required): 模块名称。
  - `description` (string, optional): 模块描述。
  - `status` (string, optional): 状态 (`active`, `inactive`, `pending`)。

#### **PUT /api/modules/<int:module_id>**
- **描述**: 更新一个已存在的模块。

#### **DELETE /api/modules/<int:module_id>**
- **描述**: 删除一个指定的模块。

## 5. 前端组件文档 (Vue.js)

### 5.1. 核心服务与状态

#### **`services/api.ts`**
- **职责**: 封装了与后端 API 的所有通信。它提供了一系列异步函数，如 `promptApi.getAll()` 和 `moduleApi.create()`。
- **实现**: 使用 `fetch` API，并包含一个统一的请求处理函数 `apiRequest`，该函数负责设置请求头、处理 JSON 数据和捕获网络错误。
- **接口**: 定义了 `Prompt` 和 `Module` 的 TypeScript 接口，确保了类型安全。

#### **`stores/index.ts` (Pinia Store)**
- **职责**: 作为整个应用的中央状态管理器。
- **State**:
  - `prompts`, `modules`: 存储从后端获取的数据列表。
  - `loading`: 一个布尔值，表示当前是否有 API 请求正在进行中。
  - `error`: 存储 API 请求失败时的错误信息。
- **Actions**:
  - `fetchPrompts`, `fetchModules`: 从后端获取最新数据并更新 state。
  - `addPrompt`, `updatePrompt`, `deletePrompt`: 执行 CRUD 操作，并在成功后自动刷新列表数据。这些 action 会处理 `loading` 和 `error` 状态。
- **Getters**:
  - `isLoading`, `errorMessage`: 计算属性，供组件方便地访问 `loading` 和 `error` 状态。

### 5.2. 视图组件 (Views)

#### **`views/PromptListView.vue`**
- **功能**: "我的提示词" 页面。负责展示提示词列表，并提供添加、编辑和删除的入口。
- **逻辑**:
  - 在组件挂载时 (`onMounted`) 调用 `mainStore.fetchPrompts()` 来加载初始数据。
  - 列表数据 `prompts` 通过 `computed` 属性从 store 中获取，实现响应式更新。
  - 管理模态框（Modal）的显示状态 (`isModalOpen`) 和当前正在编辑的提示词 (`editingPrompt`)。
  - "删除" 和 "提交" 操作会调用 store 中对应的 action。

#### **`views/ModuleListView.vue`**
- **功能**: "模块管理" 页面。功能和逻辑与 `PromptListView.vue` 类似，但用于管理模块。
- **特色**:
  - 根据模块的 `status` 字段显示不同颜色的状态标签。
  - 包含更丰富的空状态提示，引导用户创建第一个模块。

### 5.3. 可复用组件 (Components)

#### **`components/Modal.vue`**
- **功能**: 一个通用的模态框（对话框）组件。
- **Props**:
  - `show` (boolean): 控制模态框的显示与隐藏。
- **Events**:
  - `close`: 当用户点击遮罩层或关闭按钮时触发。
- **Slots**:
  - `#header`: 用于定义模态框的标题。
  - (default slot): 用于放置模态框的主体内容，如表单。

#### **`components/PromptForm.vue`**
- **功能**: 用于创建和编辑提示词的表单。
- **Props**:
  - `prompt`: 一个可选的 `Prompt` 对象。如果传入，表单将进入编辑模式并填充数据。
- **Events**:
  - `submit`: 当用户提交表单时触发，将表单数据作为参数传递出去。
  - `close`: 当用户点击取消按钮时触发。
- **逻辑**:
  - 使用 `watch` 监听 `prompt` prop 的变化，以正确填充或重置表单。

#### **`components/ModuleForm.vue`**
- **功能**: 用于创建和编辑模块的表单。其结构和逻辑与 `PromptForm.vue` 几乎一致。

## 6. 数据库结构 (SQLite)

数据库由两个核心表组成，在首次启动后端时会自动创建。

### 6.1. `prompts` 表

| 字段名 | 类型 | 约束 | 描述 |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | 唯一标识符 |
| `title` | TEXT | NOT NULL | 提示词标题 |
| `content` | TEXT | NOT NULL | 提示词内容 |
| `category` | TEXT | | 分类 |
| `tags` | TEXT | | 标签 (逗号分隔) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 最后更新时间 |

### 6.2. `modules` 表

| 字段名 | 类型 | 约束 | 描述 |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | 唯一标识符 |
| `name` | TEXT | NOT NULL | 模块名称 |
| `description` | TEXT | | 模块描述 |
| `status` | TEXT | DEFAULT 'active' | 状态 ('active', 'inactive', 'pending') |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 最后更新时间 |

---
*文档生成完毕。* 