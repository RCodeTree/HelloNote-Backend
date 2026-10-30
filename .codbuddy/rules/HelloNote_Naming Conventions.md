# Hello!Note 命名规范文档

> 项目名称：Hello!Note  
> 文档名称：Naming Conventions（命名规范）  
> 适用范围：前端、后端、数据库、API、配置文件、项目目录及开发文档  
> 技术栈：Vue 3 + TypeScript + Vite + Tailwind CSS 3 + Python + FastAPI + SQLAlchemy 2.x + MySQL

---

## 一、文档目的

为了保证 Hello!Note 项目在长期开发过程中具有统一的代码风格和清晰的项目结构，需要建立统一的命名规范。

本规范主要解决以下问题：

1. 不同开发模块之间的命名方式不统一。
2. 文件、目录、变量、函数和类的命名缺乏统一规则。
3. 前端与后端对同一业务概念使用不同名称。
4. 数据库字段、API 参数与程序变量之间缺乏一致性。
5. 配置文件、环境变量和主题变量容易出现命名混乱。
6. 后续 AI 辅助开发时，生成的代码可能不符合项目原有规范。

本规范适用于：

- `HelloNote-Backend/`
- `HelloNote-Frontend/`
- 数据库设计
- API 接口设计
- 环境配置
- 前端主题系统
- 测试代码
- 项目开发文档

**基本原则：统一、清晰、简洁、可读、可维护。**

---

## 二、全局命名规则

### 2.1 命名风格

项目主要使用以下命名风格：

| 命名风格 | 示例 | 主要使用场景 |
|---|---|---|
| PascalCase | `NoteService` | 类、Vue 组件、TypeScript 类型 |
| camelCase | `getNoteList` | JavaScript / TypeScript 变量、函数 |
| snake_case | `get_note_list` | Python 变量、函数、模块 |
| UPPER_SNAKE_CASE | `MAX_NOTE_COUNT` | 常量、环境变量 |
| kebab-case | `note-editor` | URL、CSS 类名、前端文件 |
| lowercase | `notes` | 普通目录、数据库名称等 |

### 2.2 基本要求

1. 命名必须能够表达实际用途。
2. 优先使用具有实际业务含义的英文单词。
3. 避免使用拼音作为变量、函数、类和文件名称。
4. 避免无意义缩写，例如 `a`、`b`、`temp1`、`data2`。
5. 对于行业通用缩写，可以保留，例如 `API`、`HTTP`、`URL`、`JWT`、`AI`。
6. 同一个业务概念在前后端尽量使用相同的英文名称。
7. 不要为了追求简短而牺牲可读性。
8. 不要使用容易产生歧义的单词。

### 2.3 常见缩写

| 缩写 | 完整名称 | 含义 |
|---|---|---|
| API | Application Programming Interface | 应用程序接口 |
| ID | Identifier | 标识符 |
| URL | Uniform Resource Locator | 统一资源定位符 |
| HTTP | Hypertext Transfer Protocol | 超文本传输协议 |
| JWT | JSON Web Token | 身份令牌 |
| DB | Database | 数据库 |
| AI | Artificial Intelligence | 人工智能 |
| RAG | Retrieval-Augmented Generation | 检索增强生成 |
| UI | User Interface | 用户界面 |
| DTO | Data Transfer Object | 数据传输对象 |
| CRUD | Create Read Update Delete | 增删改查 |

不建议自行创造不常见的缩写。

---

## 三、项目目录与文件命名

### 3.1 项目根目录

项目采用前后端独立仓库：

```text
Hello!Note/
├── HelloNote-Backend/
└── HelloNote-Frontend/
```

要求：

- 项目根目录使用 `Hello!Note`。
- 后端仓库使用 `HelloNote-Backend`。
- 前端仓库使用 `HelloNote-Frontend`。
- 两个项目独立维护 Git。
- 不在父目录建立统一 Git 仓库。

### 3.2 普通目录命名

普通目录统一使用小写字母。

推荐：

```text
components/
services/
repositories/
models/
schemas/
utils/
assets/
styles/
tests/
```

不推荐：

```text
Components/
Services/
MyUtils/
NoteModels/
```

### 3.3 前端文件命名

前端普通 `.ts`、`.js`、`.css` 文件优先使用 `kebab-case`。

例如：

```text
src/
├── services/
│   ├── http/
│   │   ├── http-client.ts
│   │   └── http-interceptors.ts
├── composables/
│   ├── use-theme.ts
│   └── use-loading.ts
└── assets/
    └── styles/
        ├── variables.css
        ├── themes.css
        └── glass.css
```

Vue 单文件组件使用 `PascalCase`：

```text
NoteCard.vue
NoteEditor.vue
NoteList.vue
ThemeSwitcher.vue
DefaultLayout.vue
```

推荐使用：

- 普通 TypeScript 文件：`kebab-case.ts`
- Vue 组件：`PascalCase.vue`
- CSS 文件：`kebab-case.css`
- 测试文件：`原文件名.spec.ts` 或 `原文件名.test.ts`

### 3.4 后端文件命名

Python 模块和文件统一使用 `snake_case`。

例如：

```text
app/
├── api/
│   └── v1/
│       └── endpoints/
│           ├── auth.py
│           ├── notes.py
│           └── search.py
├── services/
│   ├── auth_service.py
│   ├── note_service.py
│   └── search_service.py
├── repositories/
│   ├── note_repository.py
│   └── user_repository.py
└── models/
    ├── note.py
    └── user.py
```

文件名称应当体现所属职责。

例如：

- `note_service.py`：笔记业务逻辑。
- `note_repository.py`：笔记数据访问。
- `note.py`：笔记数据库模型。
- `note.py`（schemas 目录下）：笔记请求和响应结构。

不同目录中可以存在相同文件名，因为它们负责不同层次的内容。

### 3.5 README 和配置文件

约定：

| 文件 | 命名 |
|---|---|
| 项目说明 | `README.md` |
| 项目忽略规则 | `.gitignore` |
| 环境变量示例 | `.env.example` |
| Python 依赖配置 | `pyproject.toml` |
| Python 锁定文件 | `uv.lock` |
| 前端依赖配置 | `package.json` |
| 前端锁定文件 | `package-lock.json` |
| Vite 配置 | `vite.config.ts` |
| Tailwind 配置 | `tailwind.config.js` |
| Alembic 配置 | `alembic.ini` |

不要为了区分文件随意添加无意义后缀。

---

## 四、前端命名规范

前端采用 Vue 3 + TypeScript + Vite。

### 4.1 Vue 组件命名

Vue 组件使用 `PascalCase`。

例如：

```text
NoteCard.vue
NoteEditor.vue
NoteList.vue
NoteToolbar.vue
ThemeSwitcher.vue
SearchInput.vue
UserAvatar.vue
```

组件命名要求：

1. 组件名称应表达实际 UI 功能。
2. 避免使用 `Component1.vue` 等无意义名称。
3. 避免组件名称与 HTML 原生标签产生冲突。
4. 公共组件和业务组件应区分存放位置。
5. 页面组件以 `Page` 结尾。

示例：

```text
components/
├── common/
│   ├── BaseButton.vue
│   ├── BaseInput.vue
│   └── BaseModal.vue
└── layout/
    ├── AppHeader.vue
    ├── AppSidebar.vue
    └── AppFooter.vue

modules/
└── notes/
    └── pages/
        ├── NoteListPage.vue
        ├── NoteDetailPage.vue
        └── NoteEditPage.vue
```

### 4.2 变量命名

TypeScript 和 JavaScript 统一使用 `camelCase`。

```ts
const noteTitle = "Hello World";
const noteContent = "My first note";
const currentUser = {};
const isLoading = false;
const totalNotes = 10;
```

布尔变量建议使用：

- `is`
- `has`
- `can`
- `should`

例如：

```ts
const isLoading = false;
const isDeleted = false;
const hasPermission = true;
const canEdit = true;
```

避免：

```ts
const loading = false;
const flag = true;
const status = false;
```

当变量含义不够明确时，应当补充完整名称。

### 4.3 函数命名

函数使用 `camelCase`，并且优先使用动词开头。

| 前缀 | 含义 | 示例 |
|---|---|---|
| get | 获取数据 | `getNoteById()` |
| fetch | 请求外部数据 | `fetchNoteList()` |
| create | 创建数据 | `createNote()` |
| update | 更新数据 | `updateNote()` |
| delete | 删除数据 | `deleteNote()` |
| handle | 处理事件 | `handleSave()` |
| validate | 校验数据 | `validateNote()` |
| format | 格式化数据 | `formatDate()` |
| reset | 重置状态 | `resetForm()` |
| toggle | 切换状态 | `toggleTheme()` |
| initialize | 初始化 | `initializeTheme()` |

推荐：

```ts
function getNoteById(noteId: number) {}

function handleSave() {}

function validateNoteTitle(title: string) {}

function toggleTheme() {}
```

不推荐：

```ts
function note() {}

function doSomething() {}

function process() {}
```

### 4.4 TypeScript 类型与接口

类型和接口统一使用 `PascalCase`。

推荐：

```ts
interface Note {
  id: number;
  title: string;
  content: string;
}

interface CreateNoteRequest {
  title: string;
  content: string;
}

interface UpdateNoteRequest {
  title?: string;
  content?: string;
}

type ThemeMode = "light" | "dark" | "system";
```

接口命名建议：

| 类型 | 命名方式 | 示例 |
|---|---|---|
| 业务实体 | 业务名称 | `Note` |
| 请求参数 | 名称 + Request | `CreateNoteRequest` |
| 响应数据 | 名称 + Response | `NoteResponse` |
| 枚举联合类型 | 业务名称 + Mode/Status | `ThemeMode` |
| 组件属性 | 名称 + Props | `NoteCardProps` |
| 组件事件 | 名称 + Emits | `NoteEditorEmits` |

不建议使用 `I` 作为所有接口的统一前缀，例如 `INote`。直接使用 `Note` 即可。

### 4.5 Composables 命名

Vue Composables 统一使用 `use` 开头。

```text
use-theme.ts
use-loading.ts
use-confirm.ts
use-notes.ts
use-note-editor.ts
use-pagination.ts
```

示例：

```ts
export function useTheme() {}

export function useNoteEditor() {}

export function useLoading() {}
```

### 4.6 Pinia Store 命名

Store 文件采用 `业务名称.store.ts`。

例如：

```text
stores/
├── app.store.ts
modules/
├── auth/
│   └── stores/
│       └── auth.store.ts
└── notes/
    └── stores/
        └── notes.store.ts
```

Store 实例建议使用 `useXxxStore`：

```ts
export const useThemeStore = defineStore("theme", {});

export const useAuthStore = defineStore("auth", {});

export const useNotesStore = defineStore("notes", {});
```

Store ID 使用简洁的小写名称。

### 4.7 API 文件命名

前端业务 API 文件采用：

```text
业务名称.api.ts
```

例如：

```text
modules/
├── auth/
│   └── api/
│       └── auth.api.ts
├── notes/
│   └── api/
│       └── notes.api.ts
└── tags/
    └── api/
        └── tags.api.ts
```

API 函数建议：

```ts
export function getNoteList() {}

export function getNoteDetail(noteId: number) {}

export function createNote(data: CreateNoteRequest) {}

export function updateNote(
  noteId: number,
  data: UpdateNoteRequest
) {}

export function deleteNote(noteId: number) {}
```

### 4.8 CSS 类名

普通 CSS 类名使用 `kebab-case`。

```css
.note-card {}
.note-title {}
.note-content {}
.note-toolbar {}
.theme-switcher {}
.glass-panel {}
```

建议采用组件作用域：

```css
.note-editor {}
.note-editor__toolbar {}
.note-editor__content {}
.note-editor__footer {}
```

其中：

- `note-editor`：组件主体。
- `note-editor__toolbar`：组件内部区域。
- `note-editor--readonly`：组件修饰状态。

避免使用：

```css
.red {}
.big-text {}
.box1 {}
.test-style {}
```

### 4.9 CSS Variables 命名

统一使用 `--` 开头，采用 `kebab-case`。

主题颜色必须使用语义化命名。

推荐：

```css
--bg-primary;
--bg-secondary;
--bg-card;

--text-primary;
--text-secondary;
--text-muted;

--border-default;

--accent-primary;

--glass-bg;
--glass-border;

--shadow-card;
--shadow-floating;
```

不推荐：

```css
--white;
--black;
--gray1;
--color1;
--dark-background;
```

原因：主题切换时，`--bg-primary` 可以在 Light 和 Dark 下使用不同颜色，而 `--white` 无法清晰表达组件的实际用途。

### 4.10 Tailwind CSS 类名

优先使用语义化主题颜色：

```html
<div class="bg-page text-text-primary">
  <div class="bg-card border border-border rounded-retro">
    Hello!Note
  </div>
</div>
```

不建议在业务页面大量直接使用：

```html
<div class="bg-white text-black dark:bg-black dark:text-white">
```

对于主题色，优先使用 CSS Variables 映射后的 Tailwind 颜色。

---

## 五、后端命名规范

后端采用 Python + FastAPI + SQLAlchemy 2.x。

### 5.1 Python 变量命名

统一使用 `snake_case`。

```python
note_title = "Hello World"
note_content = "My first note"
current_user = None
is_deleted = False
total_notes = 10
```

布尔变量建议使用：

```python
is_active = True
is_deleted = False
has_permission = True
```

### 5.2 Python 函数命名

统一使用 `snake_case`。

```python
def get_note_by_id():
    pass


def create_note():
    pass


def update_note():
    pass


def delete_note():
    pass


def validate_note_title():
    pass
```

函数名称应体现实际业务动作。

### 5.3 Python 类命名

统一使用 `PascalCase`。

```python
class NoteService:
    pass


class NoteRepository:
    pass


class Note:
    pass


class CreateNoteRequest:
    pass


class UpdateNoteRequest:
    pass
```

### 5.4 常量命名

使用 `UPPER_SNAKE_CASE`。

```python
MAX_NOTE_COUNT = 1000

DEFAULT_PAGE_SIZE = 20

MAX_UPLOAD_SIZE = 10 * 1024 * 1024

DEFAULT_TIMEZONE = "UTC"
```

### 5.5 FastAPI 路由命名

路由模块使用 `snake_case` 文件名称：

```text
endpoints/
├── auth.py
├── notes.py
├── tags.py
├── search.py
└── files.py
```

路由函数采用 `snake_case`：

```python
@router.get("/notes")
def get_notes():
    pass


@router.get("/notes/{note_id}")
def get_note_detail(note_id: int):
    pass


@router.post("/notes")
def create_note():
    pass
```

路由函数建议以实际业务动作命名，而不是全部使用 `read`、`write` 等模糊名称。

### 5.6 Service 命名

Service 类使用 `PascalCase`，方法使用 `snake_case`。

```python
class NoteService:

    def get_note_list(self):
        pass

    def get_note_detail(self, note_id: int):
        pass

    def create_note(self):
        pass

    def update_note(self):
        pass

    def delete_note(self):
        pass
```

文件：

```text
note_service.py
auth_service.py
tag_service.py
search_service.py
```

### 5.7 Repository 命名

Repository 类负责数据访问。

```python
class NoteRepository:

    def get_by_id(self, note_id: int):
        pass

    def get_list(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
```

文件：

```text
note_repository.py
user_repository.py
tag_repository.py
```

### 5.8 Pydantic Schema 命名

Schema 使用 `PascalCase`。

建议：

```python
class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
```

统一建议：

| 类型 | 命名 |
|---|---|
| 创建请求 | `XxxCreate` |
| 更新请求 | `XxxUpdate` |
| 查询参数 | `XxxQuery` |
| 响应数据 | `XxxResponse` |
| 分页响应 | `XxxPageResponse` |

不要将 SQLAlchemy Model 和 Pydantic Schema 混为一谈。

### 5.9 SQLAlchemy Model 命名

Model 类使用 `PascalCase`，表名使用小写复数 `snake_case`。

例如：

```python
class Note(Base):
    __tablename__ = "notes"


class User(Base):
    __tablename__ = "users"


class Attachment(Base):
    __tablename__ = "attachments"
```

### 5.10 Python 模块导入

优先使用明确的绝对导入。

```python
from app.services.note_service import NoteService
from app.repositories.note_repository import NoteRepository
from app.models.note import Note
```

避免使用难以理解的多层相对导入。

---

## 六、数据库命名规范

数据库使用 MySQL。

### 6.1 数据库名称

使用小写 `snake_case`。

例如：

```text
hello_note
hellonote_dev
hellonote_test
```

建议开发、测试环境使用不同数据库。

### 6.2 数据表命名

统一使用小写复数 `snake_case`。

推荐：

```text
users
notes
tags
attachments
note_tags
refresh_tokens
```

要求：

1. 表名使用复数。
2. 单词之间使用下划线。
3. 避免使用 MySQL 保留关键字。
4. 关联表使用双方业务名称。
5. 表名应体现实际业务内容。

### 6.3 字段命名

统一使用 `snake_case`。

```text
id
user_id
title
content
created_at
updated_at
deleted_at
is_deleted
```

常见字段：

| 字段 | 含义 |
|---|---|
| `id` | 主键 |
| `user_id` | 用户 ID |
| `created_at` | 创建时间 |
| `updated_at` | 更新时间 |
| `deleted_at` | 删除时间 |
| `is_deleted` | 是否删除 |
| `is_active` | 是否启用 |
| `sort_order` | 排序值 |

### 6.4 主键与外键

统一建议：

- 主键使用 `id`。
- 外键使用 `关联表单数名称_id`。

例如：

```text
users.id
notes.user_id
attachments.note_id
note_tags.note_id
note_tags.tag_id
```

### 6.5 索引命名

建议统一使用：

```text
idx_表名_字段名
```

例如：

```text
idx_notes_user_id
idx_notes_created_at
idx_attachments_note_id
```

唯一索引：

```text
uk_表名_字段名
```

例如：

```text
uk_users_email
```

外键约束：

```text
fk_当前表_关联表
```

例如：

```text
fk_notes_users
```

### 6.6 数据库字段类型

命名之外，还需要保持字段语义统一。

例如：

```text
created_at
updated_at
deleted_at
```

时间字段统一使用明确的时间语义，不要使用：

```text
time1
time2
date
```

除非它们在具体业务中有明确且独立的含义。

---

## 七、API 命名规范

### 7.1 URL 路径

API 路径统一使用：

- 小写字母。
- 复数资源名称。
- `kebab-case` 仅在多词资源确有必要时使用。
- RESTful 资源风格。

推荐：

```http
GET    /api/v1/notes
GET    /api/v1/notes/{note_id}
POST   /api/v1/notes
PUT    /api/v1/notes/{note_id}
PATCH  /api/v1/notes/{note_id}
DELETE /api/v1/notes/{note_id}
```

### 7.2 API 版本

统一使用：

```text
/api/v1/
```

未来接口发生较大变化时，可以引入：

```text
/api/v2/
```

不要将版本号混入业务资源名称。

### 7.3 HTTP 方法

| 方法 | 用途 |
|---|---|
| GET | 查询资源 |
| POST | 创建资源或执行特定操作 |
| PUT | 整体更新资源 |
| PATCH | 部分更新资源 |
| DELETE | 删除资源 |

### 7.4 查询参数

查询参数统一使用 `snake_case`，与后端 Python 命名保持一致。

例如：

```http
GET /api/v1/notes?page=1&page_size=20&sort_by=created_at
```

常见参数：

```text
page
page_size
keyword
sort_by
sort_order
tag_id
created_after
created_before
```

### 7.5 请求与响应字段

建议 API JSON 字段统一使用 `snake_case`，与 Python 后端和数据库字段保持一致。

请求示例：

```json
{
  "title": "My First Note",
  "content": "Hello!Note",
  "tag_ids": [1, 2]
}
```

响应示例：

```json
{
  "id": 1,
  "title": "My First Note",
  "content": "Hello!Note",
  "created_at": "2026-10-30T10:00:00Z",
  "updated_at": "2026-10-30T10:00:00Z"
}
```

前端 TypeScript 可以直接使用相同字段名称，减少数据转换。

---

## 八、环境变量与配置命名规范

### 8.1 环境变量

统一使用 `UPPER_SNAKE_CASE`。

推荐：

```env
APP_NAME=HelloNote
APP_ENV=development
APP_DEBUG=true

API_V1_PREFIX=/api/v1

DATABASE_URL=mysql+pymysql://user:password@localhost:3306/hello_note

SECRET_KEY=your-secret-key

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

STORAGE_TYPE=local
UPLOAD_MAX_SIZE=10485760
```

### 8.2 环境分类

建议区分：

```text
.env
.env.example
```

如果未来需要不同环境文件，可以使用：

```text
.env.development
.env.test
.env.production
```

真实密钥和密码不得提交到 Git。

### 8.3 配置类命名

Python 配置类使用 `PascalCase`：

```python
class Settings:
    pass
```

配置实例：

```python
settings = Settings()
```

配置字段使用 `snake_case`：

```python
app_name
database_url
secret_key
access_token_expire_minutes
```

### 8.4 前端环境变量

Vite 环境变量必须使用 `VITE_` 前缀：

```env
VITE_APP_TITLE=Hello!Note
VITE_API_BASE_URL=http://localhost:8000
```

注意：`VITE_` 变量会暴露给浏览器，不允许存储数据库密码、私钥和其他服务端机密。

---

## 九、主题与视觉系统命名规范

Hello!Note 使用 Retro Glassmorphism 风格，并支持 Light、Dark 和 System 三种主题模式。

### 9.1 主题模式名称

统一使用：

```ts
type ThemeMode = "light" | "dark" | "system";
```

不要使用：

```text
white
black
night
day
auto
```

### 9.2 主题状态命名

```ts
themeMode
resolvedTheme
isDark
isLight
```

含义：

| 名称 | 说明 |
|---|---|
| `themeMode` | 用户设置的主题模式 |
| `resolvedTheme` | 实际生效的主题 |
| `isDark` | 是否为深色主题 |
| `isLight` | 是否为浅色主题 |

### 9.3 CSS 主题属性

统一使用：

```html
<html data-theme="light">
```

或：

```html
<html data-theme="dark">
```

不建议同时混用 `data-theme`、`theme-mode`、`dark-mode` 等多套属性。

### 9.4 CSS 变量命名

按照语义划分：

```css
/* Background */
--bg-primary;
--bg-secondary;
--bg-card;
--bg-elevated;

/* Text */
--text-primary;
--text-secondary;
--text-muted;

/* Border */
--border-default;
--border-strong;

/* Accent */
--accent-primary;
--accent-danger;
--accent-olive;

/* Glass */
--glass-bg;
--glass-border;
--glass-blur;

/* Shadow */
--shadow-card;
--shadow-floating;

/* Typography */
--font-display;
--font-body;
--font-mono;

/* Radius */
--radius-sm;
--radius-md;
--radius-lg;
--radius-xl;
```

### 9.5 玻璃组件命名

统一使用 `glass-` 前缀：

```text
glass-panel
glass-card
glass-header
glass-modal
glass-dropdown
glass-toolbar
```

如果使用 Vue 组件：

```text
GlassPanel.vue
GlassModal.vue
GlassDropdown.vue
```

---

## 十、测试代码命名规范

### 10.1 前端测试

推荐：

```text
NoteCard.spec.ts
NoteEditor.spec.ts
theme.store.spec.ts
notes.api.spec.ts
```

测试名称应当描述测试行为。

例如：

```ts
describe("NoteCard", () => {
  it("should display the note title", () => {});
});
```

### 10.2 后端测试

Python 测试文件统一使用：

```text
test_模块名称.py
```

例如：

```text
tests/
├── unit/
│   ├── test_note_service.py
│   └── test_auth_service.py
├── integration/
│   └── test_note_repository.py
└── api/
    └── test_notes.py
```

测试函数：

```python
def test_create_note():
    pass


def test_get_note_by_id():
    pass


def test_delete_note():
    pass
```

测试名称应清楚说明预期行为。

---

## 十一、Git 分支与提交信息命名

### 11.1 分支名称

建议使用：

```text
main
dev
feature/功能名称
fix/问题名称
docs/文档名称
refactor/重构内容
```

示例：

```text
feature/note-editor
feature/theme-switcher
feature/user-auth
fix/note-save-error
docs/api-design
refactor/note-service
```

分支名称统一使用小写字母和 `kebab-case`。

### 11.2 Commit 信息

采用 Conventional Commits 风格：

```text
<type>: <description>
```

或者：

```text
<type>(<scope>): <description>
```

常见类型：

| 类型 | 含义 |
|---|---|
| `feat` | 新增功能 |
| `fix` | 修复问题 |
| `docs` | 文档修改 |
| `style` | 不影响逻辑的格式调整 |
| `refactor` | 代码重构 |
| `perf` | 性能优化 |
| `test` | 测试修改 |
| `build` | 构建配置 |
| `ci` | 持续集成 |
| `chore` | 日常维护 |
| `revert` | 撤销提交 |

示例：

```text
feat: 添加笔记创建功能
feat(theme): 添加深色主题
fix: 修复笔记保存失败的问题
docs: 更新项目命名规范
refactor(note): 优化笔记服务层
test: 添加笔记接口测试
chore: 更新项目依赖
```

前端和后端分别提交、分别推送。

---

## 十二、业务名称统一对照表

为了保证前后端命名一致，以下业务概念应当统一使用相同的英文名称。

| 中文名称 | 统一英文名称 | 说明 |
|---|---|---|
| 用户 | User | 用户实体 |
| 笔记 | Note | 笔记实体 |
| 标签 | Tag | 笔记标签 |
| 附件 | Attachment | 笔记附件 |
| 收藏 | Favorite | 收藏功能 |
| 分类 | Category | 笔记分类 |
| 搜索 | Search | 搜索功能 |
| 评论 | Comment | 评论功能 |
| 文件 | File | 文件资源 |
| 会话 | Session | 会话 |
| 访问令牌 | AccessToken | 访问令牌 |
| 刷新令牌 | RefreshToken | 刷新令牌 |
| 主题 | Theme | 主题设置 |
| 摘要 | Summary | AI 摘要 |
| 向量 | Embedding | 向量表示 |
| 检索 | Retrieval | 检索操作 |
| 智能体 | Agent | AI 智能体 |

要求：

1. 同一业务概念不要在不同模块中随意使用多个英文名称。
2. 如果业务含义发生变化，应当明确区分。
3. 新增业务名称时，应同步更新本表。

---

## 十三、命名规范反例

| 不推荐 | 推荐 | 原因 |
|---|---|---|
| `Note_Service.py` | `note_service.py` | Python 文件使用 snake_case |
| `noteCard.vue` | `NoteCard.vue` | Vue 组件使用 PascalCase |
| `get_note_list()`（前端） | `getNoteList()` | TS 函数使用 camelCase |
| `noteTitle`（后端） | `note_title` | Python 变量使用 snake_case |
| `my_notes_table` | `notes` | 避免不必要的业务重复 |
| `color1` | `--text-primary` | 语义不明确 |
| `isDarkMode`（CSS） | `data-theme="dark"` | 统一主题属性 |
| `temp` | `noteContent` | 变量应表达业务含义 |
| `doUpdate()` | `updateNote()` | 函数应表达实际动作 |
| `IUser` | `User` | 不强制使用 I 前缀 |

---

## 十四、AI 辅助开发命名约束

Hello!Note 后续会使用 AI 编程工具辅助开发，因此需要将命名规范纳入项目级开发规则。

AI 生成、修改和重构代码时，必须遵守以下要求：

1. 开始修改前先检查当前项目目录和已有文件。
2. 优先遵循已有项目结构，不随意创建重复目录。
3. 不得自行改变已经确定的命名风格。
4. 新增 Vue 组件使用 `PascalCase`。
5. 新增前端变量和函数使用 `camelCase`。
6. 新增 Python 文件、函数和变量使用 `snake_case`。
7. 新增 Python 类使用 `PascalCase`。
8. 新增常量和环境变量使用 `UPPER_SNAKE_CASE`。
9. 数据库表使用小写复数 `snake_case`。
10. API JSON 字段与后端保持 `snake_case`。
11. CSS 类名使用 `kebab-case`。
12. CSS Variables 必须使用语义化名称。
13. 不允许随意改变已有 API、数据库字段或公共类型的命名。
14. 如果确实需要调整公共命名，必须检查前后端调用关系和数据库兼容性。
15. 新增业务术语时，应更新统一业务名称对照表。
16. 不要为了遵守命名规则而无意义地重命名已有稳定代码。

如果现有代码与本规范冲突，应先分析影响范围，再进行必要的调整，不要直接批量重命名。

---

## 十五、最终规范速查表

| 对象 | 命名规范 | 示例 |
|---|---|---|
| 普通目录 | lowercase | `services` |
| 前端普通文件 | kebab-case | `note-api.ts` |
| Vue 组件 | PascalCase | `NoteCard.vue` |
| 前端变量 | camelCase | `noteTitle` |
| 前端函数 | camelCase | `createNote()` |
| 前端类型 | PascalCase | `NoteResponse` |
| Pinia Store | use + PascalCase | `useNoteStore` |
| Composable | use + kebab-case 文件名 | `use-theme.ts` |
| CSS 类名 | kebab-case | `note-card` |
| CSS Variables | --kebab-case | `--bg-primary` |
| Python 文件 | snake_case | `note_service.py` |
| Python 变量 | snake_case | `note_title` |
| Python 函数 | snake_case | `get_note_by_id()` |
| Python 类 | PascalCase | `NoteService` |
| Python 常量 | UPPER_SNAKE_CASE | `MAX_NOTE_COUNT` |
| 数据库表 | 小写复数 snake_case | `notes` |
| 数据库字段 | snake_case | `created_at` |
| API 路径 | 小写复数资源 | `/api/v1/notes` |
| JSON 字段 | snake_case | `created_at` |
| 环境变量 | UPPER_SNAKE_CASE | `DATABASE_URL` |
| Git 分支 | 小写 kebab-case | `feature/note-editor` |
| Commit | Conventional Commits | `feat: 添加笔记功能` |

---

## 十六、规范维护原则

本规范不是一次性文档，而是 Hello!Note 项目的长期开发约定。

后续维护时遵循：

1. 新增技术栈时，补充对应命名规范。
2. 新增业务模块时，补充统一业务名称。
3. 如果发现现有规则不合理，可以修订，但需要保持整体一致。
4. 不随意改变已稳定的公共接口和数据库命名。
5. 所有新开发代码默认遵守最新版本的命名规范。
6. 前端和后端分别维护时，也必须遵守相同的业务概念命名。

**最终目标：让任何开发者或 AI 工具进入 Hello!Note 项目后，都能够快速理解文件用途、代码职责和业务含义，并按照统一规则继续开发。**