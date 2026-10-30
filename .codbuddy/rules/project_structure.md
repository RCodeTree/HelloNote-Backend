下面将 Hello!Note 前端项目和后端项目完全独立规划。两者分别维护自己的 Git 仓库、依赖、配置文件和 README。

这次结构设计重点考虑长期开发和后续扩展，不仅要满足初期笔记 CRUD，还要为用户认证、Pinia 数据管理、AI、RAG、Agent、文件存储等功能预留合理的位置。

设计原则：

1. 职责单一： 每个目录和文件只负责相对明确的工作。
2. 模块化： 按业务功能划分模块，避免所有代码堆积在一起。
3. 低耦合： 页面、组件、API、状态管理和业务逻辑相互独立。
4. 可扩展： 后续增加功能时，尽量在对应模块中扩展。
5. 不过度设计： 预留扩展位置，但不提前实现暂时用不到的功能。

# 一、HelloNote-Frontend 前端项目结构



独立 Git 仓库

&#x20;Vue 3 + TypeScript + Vite + Tailwind CSS 3



## 1.1 前端整体目录结构

建议采用按业务模块组织（Feature-based）+ 公共基础设施分离的结构。

这种方式比单纯按照 `pages/`、`components/`、`api/` 等技术类型堆放所有业务代码更适合长期维护。

```
HelloNote-Frontend/
│
├── public/                          # 公共静态资源
│
├── src/
│   │
│   ├── app/                          # 应用初始化与全局配置
│   │   ├── App.vue                   # 根组件
│   │   ├── main.ts                   # 主运行入口
│   │   ├── router/                   # 路由系统
│   │   │   ├── index.ts              # 路由实例创建
│   │   │   ├── routes.ts             # 路由表
│   │   │   ├── guards.ts             # 路由守卫
│   │   │   └── types.ts              # 路由类型定义
│   │   │
│   │   └── providers/                # 全局插件注册
│   │       └── index.ts              # 统一注册插件
│   │
│   ├── assets/                       # 项目内部静态资源
│   │   ├── images/
│   │   ├── icons/
│   │   └── styles/
│   │       ├── index.css             # 全局样式入口
│   │       ├── variables.css         # CSS 变量
│   │       └── tailwind.css          # Tailwind 指令
│   │
│   ├── components/                   # 全局公共组件
│   │   ├── common/                   # 通用基础组件
│   │   ├── layout/                   # 全局布局组件
│   │   └── feedback/                 # 消息、弹窗、加载状态
│   │
│   ├── layouts/                      # 页面整体布局
│   │   ├── DefaultLayout.vue         # 默认网站布局
│   │   ├── AuthLayout.vue            # 登录注册布局
│   │   └── components/               # 布局内部组件
│   │
│   ├── modules/                      # 业务功能模块
│   │   │
│   │   ├── auth/                     # 用户认证模块
│   │   │   ├── api/
│   │   │   │   └── auth.api.ts
│   │   │   ├── components/
│   │   │   ├── composables/
│   │   │   ├── pages/
│   │   │   │   ├── LoginPage.vue
│   │   │   │   └── RegisterPage.vue
│   │   │   ├── stores/
│   │   │   │   └── auth.store.ts
│   │   │   ├── types/
│   │   │   │   └── auth.types.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── notes/                    # 笔记模块
│   │   │   ├── api/
│   │   │   │   └── notes.api.ts
│   │   │   ├── components/
│   │   │   │   ├── NoteCard.vue
│   │   │   │   ├── NoteEditor.vue
│   │   │   │   ├── NoteList.vue
│   │   │   │   └── NoteToolbar.vue
│   │   │   ├── composables/
│   │   │   │   ├── useNotes.ts
│   │   │   │   └── useNoteEditor.ts
│   │   │   ├── pages/
│   │   │   │   ├── NoteListPage.vue
│   │   │   │   ├── NoteDetailPage.vue
│   │   │   │   └── NoteEditPage.vue
│   │   │   ├── stores/
│   │   │   │   └── notes.store.ts
│   │   │   ├── types/
│   │   │   │   └── notes.types.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── tags/                     # 标签模块
│   │   │   ├── api/
│   │   │   │   └── tags.api.ts
│   │   │   ├── components/
│   │   │   ├── composables/
│   │   │   ├── pages/
│   │   │   ├── stores/
│   │   │   ├── types/
│   │   │   └── index.ts
│   │   │
│   │   ├── search/                   # 搜索模块
│   │   │   ├── api/
│   │   │   ├── components/
│   │   │   ├── composables/
│   │   │   ├── pages/
│   │   │   ├── stores/
│   │   │   ├── types/
│   │   │   └── index.ts
│   │   │
│   │   ├── files/                    # 后续文件管理模块
│   │   │
│   │   ├── ai/                       # 后续 AI 功能模块
│   │   │
│   │   └── agent/                    # 后续 Agent 功能模块
│   │
│   ├── services/                     # 全局基础服务
│   │   ├── http/
│   │   │   ├── client.ts             # Axios 实例
│   │   │   ├── interceptors.ts       # 请求和响应拦截器
│   │   │   └── http.types.ts         # HTTP 类型定义
│   │   │
│   │   └── storage/
│   │       ├── local-storage.ts      # LocalStorage 封装
│   │       └── session-storage.ts    # SessionStorage 封装
│   │
│   ├── stores/                       # 全局状态管理
│   │   └── app.store.ts              # 全局应用状态
│   │
│   ├── composables/                  # 全局组合式函数
│   │   ├── useLoading.ts
│   │   └── useConfirm.ts
│   │
│   ├── directives/                   # 自定义指令
│   │
│   ├── constants/                    # 全局常量
│   │
│   ├── types/                        # 全局 TypeScript 类型
│   │
│   └── utils/                        # 通用工具函数
│
├── .env                              # 本地环境变量，不提交
├── .env.example                      # 环境变量示例
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── eslint.config.js
├── prettier.config.js
└── README.md
```

这是目标结构。初期可以先创建 `app/`、`modules/notes/`、`services/`、`components/` 等必要部分，其他模块在真正开发时再创建。

## 1.2 前端各部分职责

### ① app —— 应用入口与初始化

负责整个 Vue 应用的启动和全局初始化。

| 文件           | 职责              |
| ------------ | --------------- |
| `main.ts`    | 创建 Vue 应用、挂载应用  |
| `App.vue`    | 根组件             |
| `router/`    | 路由创建、路由表、路由守卫   |
| `providers/` | 注册 Pinia、UI 插件等 |

建议 `main.ts` 尽量保持简洁：

```
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles/index.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
```

后续如果插件越来越多，可以将注册逻辑统一放进 `providers/`。

原则：main.ts 只负责启动，不负责实现业务功能。

### ② router —— 路由管理

路由负责管理页面之间的跳转，不负责实现页面业务。

```
router/
├── index.ts
├── routes.ts
├── guards.ts
└── types.ts
```

职责划分：

| 文件          | 职责                  |
| ----------- | ------------------- |
| `index.ts`  | 创建和导出 Vue Router 实例 |
| `routes.ts` | 定义路由路径、页面组件、布局      |
| `guards.ts` | 登录状态验证、权限判断         |
| `types.ts`  | 路由相关类型              |

例如：

```
{
  path: '/notes',
  component: () => import('@/modules/notes/pages/NoteListPage.vue'),
  meta: {
    requiresAuth: true
  }
}
```

这样页面组件放在业务模块内，路由只负责引用，不需要把所有页面放在 `router/` 中。

### ③ modules —— 业务模块

这是前端最重要的组织部分。

每个模块尽可能独立管理自己的：

- API。
- 页面。
- 组件。
- Pinia Store。
- Composables。
- TypeScript 类型。

例如笔记模块：

```
modules/notes/
├── api/
│   └── notes.api.ts
├── components/
│   ├── NoteCard.vue
│   ├── NoteEditor.vue
│   └── NoteList.vue
├── composables/
│   ├── useNotes.ts
│   └── useNoteEditor.ts
├── pages/
│   ├── NoteListPage.vue
│   ├── NoteDetailPage.vue
│   └── NoteEditPage.vue
├── stores/
│   └── notes.store.ts
├── types/
│   └── notes.types.ts
└── index.ts
```

每个部分的作用：

| 目录             | 职责             |
| -------------- | -------------- |
| `api/`         | 当前模块的后端接口请求    |
| `components/`  | 当前模块专属组件       |
| `composables/` | 复用的组合式业务逻辑     |
| `pages/`       | 当前模块对应的页面      |
| `stores/`      | 当前模块的 Pinia 状态 |
| `types/`       | 当前模块的数据类型      |
| `index.ts`     | 对外导出模块需要公开的内容  |

例如，笔记模块中的 `NoteCard.vue` 不应该直接负责请求后端、管理全局状态和实现复杂业务逻辑。

它主要负责展示一张笔记卡片，并通过 `props` 接收数据，通过 `emits` 向外通知用户操作。

### ④ services —— 基础服务

这里放置多个业务模块都可能使用的底层服务。

```
services/
├── http/
│   ├── client.ts
│   ├── interceptors.ts
│   └── http.types.ts
│
└── storage/
    ├── local-storage.ts
    └── session-storage.ts
```

其中：

- `client.ts`：统一创建 Axios 实例。
- `interceptors.ts`：统一处理请求头、响应数据、错误。
- `local-storage.ts`：封装浏览器 LocalStorage。
- `session-storage.ts`：封装 SessionStorage。

重要：业务模块不应该各自创建 Axios 实例。

统一使用 `services/http/client.ts`，这样以后修改 API 地址、请求超时时间、错误处理方式时，只需要调整公共服务。

### ⑤ stores —— Pinia 状态管理

Pinia 负责管理需要在多个组件或页面之间共享的状态。

这里建议采用两种方式：

- 全局状态：放在 `src/stores/`。
- 业务状态：放在对应的 `modules/业务模块/stores/`。

例如：

```
src/
├── stores/
│   └── app.store.ts
│
└── modules/
    ├── auth/
    │   └── stores/
    │       └── auth.store.ts
    │
    └── notes/
        └── stores/
            └── notes.store.ts
```

| Store            | 管理内容        |
| ---------------- | ----------- |
| `app.store.ts`   | 全局应用状态、主题等  |
| `auth.store.ts`  | 用户登录状态、用户信息 |
| `notes.store.ts` | 笔记列表、当前笔记等  |

这里要特别区分：

Pinia 状态管理不等于数据持久化。

Pinia 主要负责运行期间的状态管理。如果希望刷新页面后仍然保留某些数据，需要结合：

- 后端 MySQL：持久保存笔记等业务数据。
- LocalStorage：保存适合留在浏览器中的少量状态。
- SessionStorage：保存当前浏览器标签页会话内的数据。

不要将所有笔记内容都只保存到 Pinia 或 LocalStorage 中。

### ⑥ components —— 公共组件

这里存放多个业务模块都能使用的组件。

```
components/
├── common/
│   ├── BaseButton.vue
│   ├── BaseInput.vue
│   ├── BaseDialog.vue
│   └── BasePagination.vue
│
├── layout/
│   ├── AppHeader.vue
│   ├── AppSidebar.vue
│   └── AppFooter.vue
│
└── feedback/
    ├── LoadingSpinner.vue
    ├── EmptyState.vue
    └── ErrorMessage.vue
```

例如：

- `BaseButton.vue`：通用按钮。
- `BaseInput.vue`：通用输入框。
- `BaseDialog.vue`：通用弹窗。
- `AppSidebar.vue`：全局侧边栏。

如果一个组件只在笔记模块中使用，就放在 `modules/notes/components/`，不要全部堆到公共组件目录。

### ⑦ layouts —— 页面布局

布局负责页面的整体框架。

例如：

- `DefaultLayout.vue`：普通网站布局。
- `AuthLayout.vue`：登录、注册页面布局。

布局可以组合 Header、Sidebar、Footer 等组件，但不负责具体的笔记业务。

## 1.3 前端一次完整请求的流程

以用户打开笔记列表为例：

```
用户访问 /notes
      │
      ▼
Vue Router
      │
      ▼
NoteListPage.vue
      │
      ▼
useNotes.ts
      │
      ▼
notes.store.ts
      │
      ▼
notes.api.ts
      │
      ▼
services/http/client.ts
      │
      ▼
FastAPI 后端
      │
      ▼
返回 JSON 数据
      │
      ▼
Pinia 更新状态
      │
      ▼
NoteListPage.vue
      │
      ▼
NoteList.vue / NoteCard.vue
      │
      ▼
页面展示笔记
```

推荐的依赖方向：

```
页面 Pages
   │
   ▼
组合式函数 Composables
   │
   ▼
Pinia Store
   │
   ▼
业务 API
   │
   ▼
公共 HTTP 服务
```

并不是所有简单页面都必须经过全部层级。简单功能可以直接由页面调用 Store，避免为了分层而增加无意义的代码。

## 1.4 前端关键文件说明

| 文件                                      | 核心作用     |
| --------------------------------------- | -------- |
| `main.ts`                               | Vue 项目启动 |
| `App.vue`                               | 应用根组件    |
| `router/index.ts`                       | 路由实例     |
| `router/routes.ts`                      | 页面路由配置   |
| `router/guards.ts`                      | 路由权限检查   |
| `services/http/client.ts`               | Axios 实例 |
| `services/http/interceptors.ts`         | 请求响应拦截   |
| `modules/notes/api/notes.api.ts`        | 笔记 API   |
| `modules/notes/stores/notes.store.ts`   | 笔记状态     |
| `modules/notes/pages/NoteListPage.vue`  | 笔记列表页面   |
| `modules/notes/components/NoteCard.vue` | 笔记卡片组件   |
| `assets/styles/index.css`               | 全局样式入口   |

# 二、HelloNote-Backend 后端项目结构



独立 Git 仓库

&#x20;Python + FastAPI + Pydantic + SQLAlchemy 2.x + MySQL



## 2.1 后端整体目录结构

后端建议采用分层架构 + 按业务模块组织 API、Schema、Service、Repository 的方式。

与前端一样，既要保证职责清晰，也要避免后续所有业务代码都挤在同一个目录中。

```
HelloNote-Backend/
│
├── app/
│   │
│   ├── main.py                       # FastAPI 应用入口
│   │
│   ├── core/                         # 核心配置与公共基础能力
│   │   ├── config.py                 # 环境配置
│   │   ├── security.py               # 安全认证相关
│   │   ├── logging.py                # 日志配置
│   │   ├── exceptions.py             # 全局异常定义
│   │   └── exception_handlers.py     # 全局异常处理
│   │
│   ├── api/                          # API 接口层
│   │   ├── deps.py                   # 通用依赖注入
│   │   └── v1/
│   │       ├── router.py             # V1 路由统一注册
│   │       └── endpoints/
│   │           ├── auth.py           # 用户认证接口
│   │           ├── notes.py          # 笔记接口
│   │           ├── tags.py           # 标签接口
│   │           ├── search.py         # 搜索接口
│   │           ├── files.py          # 文件接口
│   │           └── ai.py             # AI 接口
│   │
│   ├── schemas/                      # 请求和响应数据结构
│   │   ├── common.py                 # 通用响应结构
│   │   ├── auth.py                   # 认证 Schema
│   │   ├── note.py                   # 笔记 Schema
│   │   ├── tag.py                    # 标签 Schema
│   │   ├── file.py                   # 文件 Schema
│   │   └── ai.py                     # AI Schema
│   │
│   ├── models/                       # SQLAlchemy 数据库模型
│   │   ├── base.py                   # ORM 基础模型
│   │   ├── user.py                   # 用户模型
│   │   ├── note.py                   # 笔记模型
│   │   ├── tag.py                    # 标签模型
│   │   └── attachment.py             # 附件模型
│   │
│   ├── repositories/                 # 数据访问层
│   │   ├── user_repository.py
│   │   ├── note_repository.py
│   │   ├── tag_repository.py
│   │   └── attachment_repository.py
│   │
│   ├── services/                     # 业务逻辑层
│   │   ├── auth_service.py
│   │   ├── note_service.py
│   │   ├── tag_service.py
│   │   ├── search_service.py
│   │   └── file_service.py
│   │
│   ├── db/                           # 数据库基础设施
│   │   ├── database.py               # Engine 创建
│   │   ├── session.py                # Session 管理
│   │   └── base.py                   # 模型统一导入
│   │
│   ├── integrations/                 # 外部服务集成
│   │   ├── storage/                  # 文件存储适配
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   └── s3.py
│   │   │
│   │   └── ai/                       # AI 模型服务适配
│   │       ├── base.py
│   │       └── providers/
│   │
│   ├── ai/                           # AI 业务能力
│   │   ├── summarizer.py
│   │   ├── title_generator.py
│   │   ├── embeddings.py
│   │   └── rag/
│   │       ├── chunker.py
│   │       ├── retriever.py
│   │       └── pipeline.py
│   │
│   ├── agent/                        # Agent 自动化能力
│   │   ├── service.py
│   │   ├── tools/
│   │   │   ├── note_tools.py
│   │   │   └── search_tools.py
│   │   └── prompts/
│   │
│   └── utils/                        # 通用工具
│       ├── datetime.py
│       └── file.py
│
├── migrations/                       # Alembic 迁移文件
│   └── versions/
│
├── tests/                            # 自动化测试
│   ├── conftest.py
│   ├── unit/                          # 单元测试
│   ├── integration/                   # 集成测试
│   └── api/                           # API 测试
│
├── scripts/                          # 开发和维护脚本
│
├── .env                              # 本地环境变量，不提交
├── .env.example                      # 环境变量示例
├── .gitignore
├── alembic.ini                       # Alembic 配置
├── pyproject.toml                    # Python 项目配置与依赖
└── README.md
```

这里的 `integrations/`、`ai/`、`agent/` 等是后续扩展位置，初期不必创建所有文件。

## 2.2 后端各层职责

### ① main.py —— 应用启动入口

负责创建 FastAPI 应用和注册全局功能。

主要工作：

- 创建 FastAPI 实例。
- 注册 API 路由。
- 注册 CORS。
- 注册全局异常处理器。
- 配置应用生命周期。
- 初始化必要的基础资源。

不建议在 `main.py` 中直接写笔记 CRUD、数据库查询等业务代码。

### ② api —— API 接口层

负责接收前端 HTTP 请求，并将请求交给对应的 Service。

```
api/
├── deps.py
└── v1/
    ├── router.py
    └── endpoints/
        ├── auth.py
        ├── notes.py
        ├── tags.py
        └── search.py
```

| 文件          | 职责                  |
| ----------- | ------------------- |
| `deps.py`   | 定义通用依赖，例如数据库会话、当前用户 |
| `router.py` | 注册各业务路由             |
| `notes.py`  | 笔记 HTTP 接口          |
| `auth.py`   | 用户认证 HTTP 接口        |
| `tags.py`   | 标签 HTTP 接口          |
| `search.py` | 搜索 HTTP 接口          |

例如，笔记接口：

```
@router.post("/notes")def create_note(    note_data: NoteCreate,    db: Session = Depends(get_db)):    return note_service.create_note(db, note_data)
```

这里仅展示接口层的职责。后续可以逐步引入异步接口或统一响应规范，但不要让接口层承担数据库细节和复杂业务规则。

### ③ schemas —— 数据校验层

使用 Pydantic 定义接口接收和返回的数据结构。

例如：

```
schemas/
├── note.py
├── auth.py
└── tag.py
```

笔记 Schema 可以进一步区分：

| Schema             | 用途         |
| ------------------ | ---------- |
| `NoteCreate`       | 创建笔记时接收的数据 |
| `NoteUpdate`       | 修改笔记时接收的数据 |
| `NoteResponse`     | 返回给前端的笔记数据 |
| `NoteListResponse` | 返回笔记列表的数据  |

为什么不直接使用数据库 Model 作为 API 返回对象？

因为数据库字段与前端真正需要的字段并不一定相同。

Schema 可以单独控制：

- 哪些字段允许用户提交。
- 哪些字段允许返回。
- 字段的数据类型。
- 必填和可选规则。
- 字段格式和长度限制。

这样能够避免数据库结构和 API 结构相互绑定。

### ④ models —— 数据库模型层

使用 SQLAlchemy 2.x 定义数据库表结构。

例如：

```
models/
├── base.py
├── user.py
├── note.py
├── tag.py
└── attachment.py
```

主要负责：

- 定义数据库表。
- 定义字段类型。
- 定义主键和外键。
- 定义表之间的关联关系。
- 定义必要的数据库约束。

注意：

`models/` 不负责接收 HTTP 请求，也不应该承担复杂的业务逻辑。

### ⑤ repositories —— 数据访问层

Repository 负责与数据库进行交互。

例如：

```
repositories/
├── note_repository.py
├── user_repository.py
└── tag_repository.py
```

以笔记为例：

```
class NoteRepository:    def get_by_id(self, db, note_id):        ...    def get_all(self, db):        ...    def create(self, db, note):        ...    def update(self, db, note):        ...    def delete(self, db, note):        ...
```

Repository 主要负责：

- 查询数据库。
- 添加数据。
- 修改数据。
- 删除数据。
- 处理数据库查询条件。

它不应该负责判断用户是否有权修改某篇笔记等业务规则，这些应该由 Service 处理。

### ⑥ services —— 业务逻辑层

Service 是后端核心业务所在的位置。

例如：

```
services/
├── auth_service.py
├── note_service.py
├── tag_service.py
├── search_service.py
└── file_service.py
```

以创建笔记为例，Service 可以负责：

1. 检查创建笔记所需的数据。
2. 根据当前用户确定笔记归属。
3. 调用 Repository 保存笔记。
4. 处理业务异常。
5. 返回业务处理结果。

简单来说：

- API 负责接收请求。
- Schema 负责校验数据。
- Service 负责业务判断。
- Repository 负责数据库操作。
- Model 负责描述数据库表。

这是整个后端需要重点掌握的分层关系。

### ⑦ db —— 数据库基础设施

负责数据库连接、Engine 和 Session 管理。

```
db/
├── database.py
├── session.py
└── base.py
```

| 文件            | 职责                      |
| ------------- | ----------------------- |
| `database.py` | 创建 SQLAlchemy Engine    |
| `session.py`  | 创建和管理数据库 Session        |
| `base.py`     | 汇总 ORM 模型，方便 Alembic 识别 |

数据库配置、连接池和会话生命周期都应统一管理。

### ⑧ core —— 核心配置

存放多个模块都会使用的基础功能。

```
core/
├── config.py
├── security.py
├── logging.py
├── exceptions.py
└── exception_handlers.py
```

| 文件                      | 职责               |
| ----------------------- | ---------------- |
| `config.py`             | 读取环境变量和项目配置      |
| `security.py`           | 密码哈希、Token 等安全功能 |
| `logging.py`            | 日志配置             |
| `exceptions.py`         | 定义项目业务异常         |
| `exception_handlers.py` | 统一处理异常并返回响应      |

### ⑨ integrations —— 外部服务集成

这是为了后续扩展云存储和 AI 服务而预留的目录。

它与 `services/` 的区别是：

- `services/` 处理项目自身的业务规则。
- `integrations/` 负责与外部系统通信。

例如文件上传：

```
业务 Service
     │
     ▼
文件存储接口
     │
     ├── Local Storage
     │
     └── S3 Storage
```

未来切换云存储时，尽量只需要更换存储实现，而不必大规模修改笔记业务代码。

### ⑩ ai —— AI 业务模块

后续负责：

- 笔记总结。
- 标题生成。
- 关键词提取。
- Embedding。
- RAG 检索。

需要注意 AI 业务逻辑与 AI 模型供应商调用的区别：

- `ai/`：负责项目中的 AI 业务流程。
- `integrations/ai/`：负责接入具体的模型服务。

这样未来更换模型供应商时，不必重写所有 AI 业务逻辑。

### ⑪ agent —— Agent 自动化模块

未来负责：

- Agent 任务处理。
- 工具注册。
- 工具调用。
- 提示词管理。
- 多步骤任务编排。

Agent 应该通过已有 Service 执行业务操作，而不是直接访问数据库。

### ⑫ tests —— 测试模块

测试代码独立于业务代码，按照测试类型进行组织。

```
tests/
├── conftest.py
├── unit/
├── integration/
└── api/
```

| 目录             | 测试内容              |
| -------------- | ----------------- |
| `unit/`        | Service、工具函数等单元测试 |
| `integration/` | 数据库及外部服务集成测试      |
| `api/`         | FastAPI 接口测试      |
| `conftest.py`  | 公共测试配置和 Fixtures  |

## 2.3 后端一次完整请求的流程

以创建笔记为例：

```
前端发送 POST 请求
       │
       ▼
API /notes
       │
       ▼
Pydantic NoteCreate
       │
       ▼
NoteService
       │
       ├── 业务规则检查
       │
       └── 权限检查
       │
       ▼
NoteRepository
       │
       ▼
SQLAlchemy Model
       │
       ▼
MySQL
       │
       ▼
返回数据库结果
       │
       ▼
Service 处理结果
       │
       ▼
NoteResponse
       │
       ▼
API 返回 JSON
       │
       ▼
前端接收数据
```

推荐的依赖方向：

```
API
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
Model / Database
```

Schemas 负责定义 API 的输入输出，不是数据库访问层，也不应代替 Model。

# 三、前后端职责边界

前后端独立不代表没有联系。两边需要通过明确的 API 规范进行通信。

| 功能      | 前端负责            | 后端负责           |
| ------- | --------------- | -------------- |
| 页面展示    | Vue 页面和组件       | 不负责            |
| 页面跳转    | Vue Router      | 不负责            |
| 浏览器状态   | Pinia           | 不负责            |
| 浏览器本地缓存 | LocalStorage 封装 | 不负责            |
| 请求发送    | Axios           | 不负责            |
| 数据校验    | 前端表单校验          | Pydantic 服务端校验 |
| 用户认证    | 登录页面、Token 使用   | 身份验证、权限检查      |
| 笔记业务    | 用户操作和展示         | 业务规则处理         |
| 数据持久化   | 发起请求、展示结果       | MySQL          |
| 文件上传    | 文件选择、上传进度       | 文件校验、实际存储      |
| AI 展示   | 展示 AI 结果        | 模型调用和业务处理      |
| RAG     | 展示问答结果和来源       | 文本处理、检索和生成     |
| Agent   | 提供交互界面          | 工具调用与任务执行      |

# 四、两套项目的核心解耦原则

这是开发过程中需要长期遵守的约定。

## 4.1 前端原则

| 原则            | 具体要求                  |
| ------------- | --------------------- |
| 页面与组件分离       | 页面负责组合，组件负责展示和交互      |
| 页面与 API 分离    | 页面不直接编写 Axios 请求      |
| API 与 HTTP 分离 | 业务 API 不重复创建 Axios 实例 |
| 路由与页面分离       | Router 只负责路由配置        |
| 状态与页面分离       | 共享状态统一由 Pinia 管理      |
| 业务模块独立        | 笔记、认证、标签分别组织          |
| 公共组件独立        | 多模块共用的组件放在公共目录        |

## 4.2 后端原则

| 原则                      | 具体要求                 |
| ----------------------- | -------------------- |
| API 与业务分离               | API 不实现复杂业务逻辑        |
| Schema 与 Model 分离       | 不直接把数据库模型当作所有接口的数据结构 |
| Service 与 Repository 分离 | 业务判断不写在数据库访问层        |
| 数据库配置统一                 | 不在各业务模块重复创建数据库连接     |
| 异常处理统一                  | 使用统一异常机制             |
| 外部服务解耦                  | 使用接口或适配层隔离第三方服务      |
| Agent 与业务分离             | Agent 调用已有 Service   |

# 五、推荐的实际创建顺序

虽然上面给出了完整结构，但不建议你一开始就创建所有目录和文件。

否则容易出现大量空目录，反而增加理解成本。

建议按下面的顺序创建。

## 5.1 前端第一阶段

先创建：

```
src/
├── app/
│   ├── App.vue
│   ├── main.ts
│   └── router/
│       ├── index.ts
│       └── routes.ts
│
├── assets/
│   └── styles/
│       └── index.css
│
├── components/
│   └── common/
│
├── layouts/
│   └── DefaultLayout.vue
│
├── modules/
│   └── notes/
│       ├── api/
│       ├── components/
│       ├── pages/
│       ├── stores/
│       └── types/
│
├── services/
│   └── http/
│       └── client.ts
│
├── stores/
│
├── types/
│
└── utils/
```

第一阶段先把笔记列表页面和后端接口请求跑通。

## 5.2 后端第一阶段

先创建：

```
app/
├── main.py
│
├── core/
│   └── config.py
│
├── api/
│   └── v1/
│       ├── router.py
│       └── endpoints/
│           └── notes.py
│
├── schemas/
│   └── note.py
│
├── models/
│   └── note.py
│
├── repositories/
│   └── note_repository.py
│
├── services/
│   └── note_service.py
│
└── db/
    ├── database.py
    └── session.py

tests/
```

初期先完成：

1. FastAPI 启动。
2. 创建笔记 Schema。
3. 创建笔记 Model。
4. 实现笔记 Repository。
5. 实现笔记 Service。
6. 创建笔记 API。
7. 接入 MySQL。
8. 实现笔记 CRUD。

# 六、最终架构总结

Hello!Note 前端

Vue 3 + TypeScript

app — 应用启动、路由、插件

modules — 笔记、认证、标签、搜索等业务模块

components / layouts — 公共组件和页面布局

stores — Pinia 状态管理

services — HTTP 和浏览器存储服务

composables / utils — 可复用逻辑和工具

REST API / JSON

Hello!Note 后端

FastAPI + Python

api — HTTP 接口

schemas — 数据校验和响应结构

services — 业务逻辑

repositories — 数据访问

models / db — ORM 模型和数据库连接

core — 配置、安全、异常和日志

integrations / ai / agent — 外部服务与未来扩展

MySQL 数据库

用户、笔记、标签、附件元数据

我的建议： 这套结构可以作为 Hello!Note 的长期目标架构。开发时优先落实前端的 `app / modules / services / stores`，以及后端的 `api / schemas / services / repositories / models / db`。先把笔记 CRUD 的完整调用链跑通，再逐步增加其他模块，不要为了目录完整而提前实现所有功能。