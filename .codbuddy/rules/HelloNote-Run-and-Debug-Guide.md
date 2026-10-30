# Hello!Note 运行与调试配置指南

> 本文用于 Hello!Note 的本地开发环境。后端使用 **uv + Uvicorn + FastAPI**，前端使用 **pnpm + Vue 3 + Vite**。前后端仍然是两个独立 Git 仓库，分别安装依赖、运行和调试。

## 1. 本地开发环境约定

### 1.1 项目目录

```text
Hello!Note/
├── HelloNote-Backend/       # 后端独立 Git 仓库
│   ├── .venv/               # uv 创建的 Python 虚拟环境
│   ├── .env                 # 后端本地环境变量，不提交 Git
│   ├── .env.example         # 环境变量示例，可以提交 Git
│   ├── pyproject.toml       # Python 项目和依赖声明
│   └── uv.lock              # Python 依赖锁定文件，可以提交 Git
│
└── HelloNote-Frontend/      # 前端独立 Git 仓库
    ├── node_modules/        # pnpm 安装的依赖，不提交 Git
    ├── .env.development.local
    ├── .env.example
    ├── package.json         # 前端项目和脚本配置
    └── pnpm-lock.yaml       # 前端依赖锁定文件，可以提交 Git
```

父目录 `Hello!Note/` 不初始化 Git；后端和前端分别管理各自的代码、配置和提交记录。

### 1.2 本地端口约定

| 服务 | 地址 | 用途 |
|---|---|---|
| Vue / Vite | `http://127.0.0.1:5173` | 前端开发页面 |
| FastAPI / Uvicorn | `http://127.0.0.1:8000` | 后端 API |
| FastAPI Swagger | `http://127.0.0.1:8000/docs` | 在线接口调试 |
| FastAPI ReDoc | `http://127.0.0.1:8000/redoc` | 接口文档 |
| MySQL | `127.0.0.1:3306` | 本地数据库 |

开发时尽量统一使用 `127.0.0.1`，不要在部分配置里使用 `localhost`、另一些配置里使用 `127.0.0.1`，避免浏览器将它们视为不同来源而产生跨域问题。

## 2. 开发环境准备

### 2.1 后端环境

建议使用 Python 3.12，并使用 uv 管理 Python 版本、虚拟环境和依赖。

确认工具可用：

```bash
python --version
uv --version
```

如果本机还没有 Python 3.12，可以让 uv 安装：

```bash
uv python install 3.12
```

进入后端仓库：

```bash
cd HelloNote-Backend
```

如果项目还没有 `pyproject.toml`，先初始化一次：

```bash
uv init --bare --name hellonote-backend
```

如果已经存在 `pyproject.toml`，不要重复执行初始化命令。

将项目 Python 版本固定为 3.12：

```bash
uv python pin 3.12
```

这会生成或更新 `.python-version`。该文件应纳入 Git，让项目成员使用一致的 Python 主版本。

### 2.2 前端环境

Vite 当前版本要求 Node.js 至少为 `20.19+` 或 `22.12+`。建议选用满足该要求的 Node.js LTS 版本，并在项目开发期间尽量保持一致。

确认 Node.js 和 npm：

```bash
node --version
npm --version
```

安装 pnpm：

```bash
npm install --global pnpm@latest
```

确认 pnpm 可用：

```bash
pnpm --version
```

进入前端仓库：

```bash
cd HelloNote-Frontend
```

如果 Vue 3 + TypeScript + Vite 项目尚未创建，并且当前目录为空，可以执行：

```bash
pnpm create vite . --template vue-ts
```

如果已经存在 `package.json`，不要重新创建项目，直接安装依赖即可。

## 3. 后端运行配置：uv + Uvicorn

### 3.1 安装项目依赖

在 `HelloNote-Backend/` 目录执行：

```bash
# 运行依赖
uv add fastapi "uvicorn[standard]" sqlalchemy pymysql pydantic-settings python-dotenv

# 开发和测试依赖
uv add --dev pytest httpx ruff

# 创建或同步虚拟环境
uv sync
```

依赖用途：

| 依赖 | 用途 |
|---|---|
| `fastapi` | 后端 Web API 框架 |
| `uvicorn[standard]` | ASGI 服务运行器；standard 扩展包含常用运行和热重载依赖 |
| `sqlalchemy` | ORM 和数据库访问 |
| `pymysql` | SQLAlchemy 连接 MySQL 的同步驱动 |
| `pydantic-settings` | 管理应用配置和环境变量 |
| `python-dotenv` | 为读取 `.env` 文件提供支持 |
| `pytest` | 自动化测试 |
| `httpx` | 测试 FastAPI 接口 |
| `ruff` | Python 代码检查和格式化工具 |

依赖安装后，uv 会在后端仓库中维护 `.venv/`、`pyproject.toml` 和 `uv.lock`。不要手动修改 `uv.lock`。

### 3.2 最小应用入口

确保后端至少存在以下结构：

```text
HelloNote-Backend/
├── app/
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
└── uv.lock
```

`app/main.py` 初期可以先使用下面的最小入口，后续再注册正式的 API 路由和异常处理：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Hello!Note API",
    version="0.1.0",
)

# 开发阶段允许本地前端访问。
# 即使使用 Vite 代理，也保留明确的来源白名单，方便以后直接联调。
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health", tags=["system"])
def health_check():
    return {
        "status": "ok",
        "service": "HelloNote-Backend",
    }
```

这里的 `health_check` 只是用于检查后端是否成功启动。正式业务接口仍放在规划好的 `app/api/v1/endpoints/` 中，并由总路由统一注册。

### 3.3 本地开发运行命令

在 `HelloNote-Backend/` 项目根目录执行：

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --reload-dir app
```

参数说明：

| 参数 | 含义 |
|---|---|
| `uv run` | 使用当前项目的 uv 环境运行命令 |
| `uvicorn` | 启动 Uvicorn 服务 |
| `app.main:app` | 从 `app/main.py` 导入名为 `app` 的 FastAPI 实例 |
| `--reload` | Python 代码变更后自动重启服务 |
| `--host 127.0.0.1` | 只监听本机 |
| `--port 8000` | 使用 8000 端口 |
| `--reload-dir app` | 只监视后端 app 目录，减少无关文件变化触发重载 |

启动成功后检查：

```text
http://127.0.0.1:8000/api/v1/health
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

也可以直接在终端测试健康检查接口：

```bash
curl http://127.0.0.1:8000/api/v1/health
```

开发时推荐始终通过 `uv run` 执行命令，不需要每次手动激活 `.venv`。如需让 IDE 识别依赖，则把 IDE 的 Python 解释器指向项目的 `.venv`。

### 3.4 后端环境变量

后端仓库根目录建立 `.env.example`：

```dotenv
APP_ENV=development

# 数据库尚未接入时，可以先不填写；接入 SQLAlchemy 后再配置。
DATABASE_URL=mysql+pymysql://hellonote_user:replace_this_password@127.0.0.1:3306/hello_note?charset=utf8mb4

# 示例占位值。正式使用时应生成随机密钥，不要使用此占位值。
SECRET_KEY=replace-with-a-long-random-secret
```

复制为本地 `.env`，再填写本机真实配置：

```bash
# macOS / Linux / Git Bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

注意：

- `.env` 存放本机真实配置，不提交 Git。
- `.env.example` 只放变量名称和安全的示例值，应提交 Git。
- 数据库尚未接入时，不必为了启动一个简单健康检查接口而提前强制连接 MySQL。
- `SECRET_KEY`、数据库密码和第三方 API Key 不得硬编码在 Python 源码中。

### 3.5 后端常用命令

| 目的 | 命令 |
|---|---|
| 同步依赖 | `uv sync` |
| 添加运行依赖 | `uv add 包名` |
| 添加开发依赖 | `uv add --dev 包名` |
| 查看依赖树 | `uv tree` |
| 启动开发服务 | `uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --reload-dir app` |
| 执行测试 | `uv run pytest` |
| 代码检查 | `uv run ruff check .` |
| 代码格式化 | `uv run ruff format .` |

## 4. 前端运行配置：pnpm + Vite

### 4.1 安装依赖

在 `HelloNote-Frontend/` 目录执行：

```bash
pnpm install
```

`pnpm install` 会根据 `package.json` 和 `pnpm-lock.yaml` 安装依赖。正常情况下应保留并提交 `pnpm-lock.yaml`，这样其他环境可以安装相同版本的依赖。

### 4.2 package.json 脚本配置

检查 `package.json` 中包含下面这些脚本。若已有其他脚本，请合并，不要直接覆盖整个文件：

```json
{
  "scripts": {
    "dev": "vite --host 127.0.0.1",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview --host 127.0.0.1"
  }
}
```

项目完整的 `package.json` 还需要保留原有的 `dependencies`、`devDependencies` 等字段。

建议在 `package.json` 中设置 `packageManager` 字段，填写本机 `pnpm --version` 输出的完整版本号，例如格式为 `pnpm@实际版本号`。这样可以明确项目预期使用的包管理器版本。不要把示例占位文字直接作为版本号。

### 4.3 Vite 开发服务器和后端代理

修改前端根目录的 `vite.config.ts`，将开发服务器配置为：

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
```

如果原有 `vite.config.ts` 已经配置了其他插件或别名，请保留原配置，只合并 `server` 部分。

代理配置的作用：

1. 浏览器访问前端：`http://127.0.0.1:5173`。
2. 前端请求：`/api/v1/health`。
3. Vite 将 `/api` 开头的请求转发到：`http://127.0.0.1:8000`。
4. FastAPI 返回响应，Vite 将响应传回浏览器。

因此，前端 API 地址优先使用相对路径，不要在开发环境的每个 API 请求里写死 `http://127.0.0.1:8000`。

### 4.4 前端环境变量

前端根目录建立 `.env.example`：

```dotenv
VITE_API_BASE_URL=/api/v1
```

本地开发可以使用 `.env.development.local`：

```dotenv
VITE_API_BASE_URL=/api/v1
```

Axios 公共请求实例可以读取该变量：

```typescript
const baseURL = import.meta.env.VITE_API_BASE_URL || '/api/v1'
```

注意：

- Vite 只会将符合规则的前端环境变量暴露给客户端；默认使用 `VITE_` 前缀。
- 所有 `VITE_` 变量最终都可能被浏览器访问，不能放数据库密码、私钥或第三方服务 Secret。
- `.env.development.local` 等本地文件加入 `.gitignore`。
- 不同环境的 API 地址可以通过不同的 `.env` 文件管理。

### 4.5 前端启动与构建

在 `HelloNote-Frontend/` 目录执行：

```bash
# 启动 Vite 开发服务器
pnpm run dev

# 检查 TypeScript 并构建生产文件
pnpm run build

# 本地预览构建结果
pnpm run preview
```

启动后访问：

```text
http://127.0.0.1:5173
```

常用命令：

| 目的 | 命令 |
|---|---|
| 安装依赖 | `pnpm install` |
| 严格按照锁文件安装 | `pnpm install --frozen-lockfile` |
| 添加运行依赖 | `pnpm add 包名` |
| 添加开发依赖 | `pnpm add -D 包名` |
| 删除依赖 | `pnpm remove 包名` |
| 启动开发服务器 | `pnpm run dev` |
| 构建项目 | `pnpm run build` |
| 预览构建结果 | `pnpm run preview` |
| 查看依赖 | `pnpm list` |

## 5. 前后端联调流程

### 5.1 启动顺序

建议使用两个独立终端窗口：

**终端 A：启动后端**

```bash
cd HelloNote-Backend
uv sync
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --reload-dir app
```

**终端 B：启动前端**

```bash
cd HelloNote-Frontend
pnpm install
pnpm run dev
```

打开浏览器访问前端页面。后端和 MySQL 需要分别启动；如果当前阶段还没有使用数据库，可以先只启动前后端。

### 5.2 请求路径约定

```text
浏览器
  |
  | GET /api/v1/health
  v
Vite :5173
  |
  | proxy: /api -> http://127.0.0.1:8000
  v
FastAPI / Uvicorn :8000
  |
  v
返回 JSON
```

前端 Axios 实例的 `baseURL` 使用 `/api/v1`。例如：

```typescript
// 请求最终路径为 /api/v1/health
httpClient.get('/health')
```

这里假设 `httpClient` 已经将 `baseURL` 设置为 `/api/v1`。如果项目后续决定直接跨端口访问后端，则再调整 CORS 来源配置和 API Base URL，不需要现在同时维护两套请求方式。

### 5.3 验证联调

后端启动后，先确认下面的地址能够返回 JSON：

```text
http://127.0.0.1:8000/api/v1/health
```

再从浏览器访问前端页面，并在浏览器开发者工具的 Network 面板中查看请求：

```text
http://127.0.0.1:5173/api/v1/health
```

浏览器地址栏显示的是 Vite 地址；真正的请求会由 Vite 转发给后端。

## 6. 调试器配置

### 6.1 VS Code 后端断点调试（可选）

如果使用 VS Code，可以在 `HelloNote-Backend/` 仓库内创建：

```text
.vscode/
└── launch.json
```

配置如下：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "HelloNote Backend: Debug Uvicorn",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--log-level",
        "debug"
      ],
      "cwd": "${workspaceFolder}",
      "envFile": "${workspaceFolder}/.env",
      "justMyCode": true
    }
  ]
}
```

使用步骤：

1. 在 VS Code 中单独打开 `HelloNote-Backend/` 文件夹。
2. 安装并启用 Python、Python Debugger 扩展。
3. 通过 `Python: Select Interpreter` 选择仓库中的 `.venv` 解释器。
4. 在代码行号左侧设置断点。
5. 打开 Run and Debug，选择 `HelloNote Backend: Debug Uvicorn`，按 F5。

这份调试配置没有启用 `--reload`，目的是让调试器直接控制服务进程，方便断点、单步执行和变量检查。日常只想自动重启时，使用前面的 `uv run uvicorn ... --reload` 命令即可。

### 6.2 前端调试

前端开发阶段通常使用浏览器开发者工具和 Vue DevTools：

- **Console**：查看 JavaScript 运行错误和调试输出。
- **Network**：查看请求 URL、请求参数、响应数据和状态码。
- **Sources**：查看源代码并设置浏览器断点。
- **Vue DevTools**：检查 Vue 组件层级、组件状态和 Pinia Store。

调试接口请求时，优先检查 Network 面板中的请求地址、状态码和响应内容；不要只根据页面是否弹出错误提示来判断后端问题。

## 7. Git 忽略规则

### 7.1 后端 `.gitignore`

确认后端 `.gitignore` 至少包含：

```gitignore
# Python virtual environment
.venv/

# Python cache
__pycache__/
*.py[cod]

# Test and lint cache
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# Local environment variables
.env
.env.*
!.env.example

# Build artifacts
build/
dist/
*.egg-info/
```

以下文件应该提交 Git：

- `pyproject.toml`
- `uv.lock`
- `.python-version`
- `.env.example`
- `app/`、`tests/`、`migrations/`、必要的 `scripts/`

### 7.2 前端 `.gitignore`

确认前端 `.gitignore` 至少包含：

```gitignore
# Dependencies
node_modules/

# Build output
dist/

# Local environment files
.env.local
.env.*.local

# Tool cache
.vite/
coverage/
```

以下文件应该提交 Git：

- `package.json`
- `pnpm-lock.yaml`
- `vite.config.ts`
- `.env.example`
- `src/`、`public/` 和项目配置文件

不要忽略整个 `.vscode/` 目录。如果其中保存的是团队通用的项目调试配置，可以提交；个人偏好设置则不提交。

## 8. 常见问题排查

### 8.1 `Could not import module "app.main"`

检查：

1. 终端当前目录是否为 `HelloNote-Backend/`。
2. 是否存在 `app/main.py`。
3. 是否存在 `app/__init__.py`。
4. Uvicorn 命令是否写成 `app.main:app`，最后的 `app` 是否对应 `main.py` 中的 FastAPI 实例变量。

### 8.2 `uvicorn` 命令找不到

检查是否在项目目录下执行了 `uv sync`。建议直接使用：

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

不要在系统 Python 环境中随意安装一份 Uvicorn，再期待项目虚拟环境自动使用它。

### 8.3 前端请求出现 404

依次检查：

1. FastAPI 是否真的注册了该路由。
2. 后端实际路由是否以 `/api/v1` 开头。
3. Vite 代理是否配置了 `/api`。
4. Axios 的 `baseURL` 和接口方法拼接后是否形成正确路径。

例如，`baseURL` 是 `/api/v1`，请求方法使用 `get('/health')`，最终路径应为 `/api/v1/health`，不要重复拼接成 `/api/v1/api/v1/health`。

### 8.4 出现 CORS 跨域错误

优先确认：

- 浏览器是否通过 `http://127.0.0.1:5173` 访问前端。
- 前端是否请求相对地址 `/api/v1/...`，而不是直接写后端完整地址。
- Vite 的代理目标是否为 `http://127.0.0.1:8000`。
- 如果采用直接跨端口请求，FastAPI 的 `allow_origins` 是否包含浏览器当前页面的完整来源（协议、主机和端口）。

不要在允许携带凭据的情况下简单设置 `allow_origins=["*"]`；开发阶段也尽量使用明确的来源白名单。

### 8.5 端口已经被占用

如果 `8000` 或 `5173` 已被其他程序占用，可以先停止占用端口的程序，或者同步修改服务端口和代理配置。前端设置了 `strictPort: true`，端口被占用时会直接报错，不会悄悄换到其他端口。

例如将后端改到 `8001` 时，也必须把 `vite.config.ts` 中的代理目标改为 `http://127.0.0.1:8001`。

### 8.6 修改依赖后其他环境运行异常

- Python 依赖变化：通过 `uv add` 或 `uv remove` 修改，再提交更新后的 `pyproject.toml` 和 `uv.lock`。
- 前端依赖变化：通过 `pnpm add` 或 `pnpm remove` 修改，再提交更新后的 `package.json` 和 `pnpm-lock.yaml`。
- 不要只提交依赖声明而漏掉锁文件，也不要手动编辑锁文件。

## 9. 开发环境与生产环境的区别

| 项目 | 本地开发 | 生产部署 |
|---|---|---|
| Uvicorn | 使用 `--reload` | 不使用 `--reload` |
| Uvicorn Host | `127.0.0.1` | 根据部署架构监听内网或 `0.0.0.0` |
| Uvicorn Workers | 通常先使用默认单进程 | 根据资源和部署方式规划 |
| Vite | 使用 `pnpm run dev` | 执行 `pnpm run build` |
| 前端服务 | Vite 开发服务器 | Nginx、对象存储静态托管等 |
| 环境变量 | 本地 `.env` / `.env.*.local` | 部署平台或服务器安全注入 |
| 调试日志 | 可以使用 debug 级别 | 根据日志策略控制，避免泄露敏感信息 |

不要把 `pnpm run dev` 或 Uvicorn 的 `--reload` 当成生产运行方式。Uvicorn 的 `--reload` 与 `--workers` 不能同时使用。

## 10. 推荐的日常开发流程

1. 拉取前端和后端各自仓库的最新代码。
2. 后端执行 `uv sync`，前端执行 `pnpm install`。
3. 确认 MySQL 已启动（当前功能不需要数据库时可以暂不启动）。
4. 在后端终端启动 Uvicorn。
5. 在前端终端启动 Vite。
6. 浏览器访问 `http://127.0.0.1:5173`，通过 Network 和 FastAPI `/docs` 联合调试接口。
7. 修改依赖时使用 uv 或 pnpm 命令，并提交相应锁文件。
8. 提交前检查两个仓库各自的 `git status`，分别进行测试、Commit 和 Push。

---

## 官方文档

- [uv 项目管理](https://docs.astral.sh/uv/guides/projects/)
- [Uvicorn 配置与命令行参数](https://uvicorn.dev/settings/)
- [Vite 入门指南](https://vite.dev/guide/)
- [Vite 开发服务器配置](https://vite.dev/config/server-options)
- [pnpm 安装文档](https://pnpm.io/installation)
- [VS Code Python 调试](https://code.visualstudio.com/docs/python/debugging)
