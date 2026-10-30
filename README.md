# HelloNote Backend

HelloNote 项目的后端服务，基于 [FastAPI](https://fastapi.tiangolo.com/) 构建。当前为项目初始化脚手架，提供基础接口示例。

## 技术栈

- **语言**：Python >= 3.14
- **Web 框架**：FastAPI
- **ASGI 服务器**：Uvicorn
- **包管理器**：[uv](https://docs.astral.sh/uv/)

## 项目结构

```
HelloNote-Backend/
├── main.py            # 应用入口：FastAPI 实例与路由定义
├── pyproject.toml     # 项目元信息与依赖声明
├── uv.lock            # uv 锁定的依赖版本（可复现安装）
├── test_main.http     # 接口测试脚本（VS Code REST Client）
└── .gitignore         # 忽略规则（含 .idea / node_modules 等）
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
uv run uvicorn main:app --reload
```

> 也可以使用 FastAPI 内置的开发命令：`uv run fastapi dev main.py`

启动后访问：

- 服务根地址：<http://127.0.0.1:8000>
- 交互式 API 文档（Swagger UI）：<http://127.0.0.1:8000/docs>
- ReDoc 文档：<http://127.0.0.1:8000/redoc>

## API 接口

| 方法 | 路径            | 说明               | 响应示例                          |
| ---- | --------------- | ------------------ | --------------------------------- |
| GET  | `/`             | 根路径，返回欢迎信息 | `{"message": "Hello World"}`      |
| GET  | `/hello/{name}` | 带参数的问候接口     | `{"message": "Hello User"}`       |

### 请求示例

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/hello/User
```

## 接口测试

项目根目录下的 `test_main.http` 提供了接口测试脚本，可在 VS Code 中使用 **REST Client** 插件直接运行：打开文件后点击每个请求上方的 `Send Request` 即可发送并查看响应。

## 说明

- `.idea/` 等编辑器/IDE 目录已被 `.gitignore` 忽略，不会纳入 Git 版本管理。
- 当前接口仅为示例，后续业务逻辑请在 `main.py` 或新增的路由模块中扩展。
