# HelloNote Backend

HelloNote 项目的后端服务，基于 [FastAPI](https://fastapi.tiangolo.com/) 构建，采用分层架构（api / core / db / models / repositories / services）。

## 技术栈

- **语言**：Python >= 3.14
- **Web 框架**：FastAPI
- **ASGI 服务器**：Uvicorn
- **包管理器**：[uv](https://docs.astral.sh/uv/)

## 项目结构

```
HelloNote-Backend/
├── app/
│   ├── main.py        # 唯一应用入口：FastAPI 实例、CORS、路由注册与生命周期
│   ├── api/           # 接口层（v1 路由与端点）
│   ├── core/          # 配置、安全（密码哈希/JWT）、异常
│   ├── db/            # 数据库引擎与会话
│   ├── models/        # SQLAlchemy ORM 模型
│   ├── repositories/  # 数据访问层
│   ├── schemas/       # Pydantic 模型
│   └── services/      # 业务逻辑层
├── pyproject.toml     # 项目元信息与依赖声明
├── uv.lock            # uv 锁定的依赖版本（可复现安装）
├── test_main.http     # 接口测试脚本（VS Code REST Client）
└── .gitignore         # 忽略规则
```

## 环境要求

- Python 3.14 或以上
- 已安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)

## 快速开始

1. 安装依赖：

```bash
uv sync
```

2. 启动开发服务器（热重载）：

```bash
uv run uvicorn app.main:app --reload
```

> 也可以使用 FastAPI 内置的开发命令：`uv run fastapi dev app/main.py`

启动后访问：

- 服务根地址：<http://127.0.0.1:8000>
- 交互式 API 文档（Swagger UI）：<http://127.0.0.1:8000/docs>
- ReDoc 文档：<http://127.0.0.1:8000/redoc>

## API 接口

正式业务接口统一挂载在 `/api/v1` 前缀下，例如：

| 方法 | 路径                  | 说明                  |
| ---- | --------------------- | --------------------- |
| GET  | `/api/v1/health`      | 健康检查（无需鉴权）  |
| POST | `/api/v1/auth/login`  | 登录，返回 JWT        |
| POST | `/api/v1/auth/register` | 注册                |
| GET  | `/api/v1/auth/me`     | 获取当前用户（需鉴权）|
| GET  | `/api/v1/dashboard/stats` | 面板统计（需鉴权） |

完整的接口列表与交互式调试请访问自动生成的文档（Swagger UI）：

- 交互式 API 文档（Swagger UI）：<http://127.0.0.1:8000/docs>
- ReDoc 文档：<http://127.0.0.1:8000/redoc>

### 请求示例

```bash
curl http://127.0.0.1:8000/api/v1/health
```

## 接口测试

项目根目录下的 `test_main.http` 提供了接口测试脚本，可在 VS Code 中使用 **REST Client** 插件直接运行：打开文件后点击每个请求上方的 `Send Request` 即可发送并查看响应。

## 说明

- `.idea/` 等编辑器/IDE 目录已被 `.gitignore` 忽略，不会纳入 Git 版本管理。
- 当前接口仅为示例，后续业务逻辑请在 `app/` 包内的路由模块中扩展。
