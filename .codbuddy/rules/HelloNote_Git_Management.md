
# Hello!Note 项目 Git 版本管理规范

> 文档名称：Hello!Note Git 版本管理规范\
> 适用项目：HelloNote-Frontend、HelloNote-Backend\
> 管理方式：前后端独立 Git 仓库\
> 核心目标：规范项目文件管理、AI Rules / Skills 管理、Commit 提交、Push 推送和分支管理。

---

# 一、Git 仓库管理原则

## 1.1 仓库结构

Hello!Note 采用前后端独立 Git 仓库的管理方式。

```
Hello!Note/
├── HelloNote-Backend/       # 后端独立 Git 仓库
└── HelloNote-Frontend/      # 前端独立 Git 仓库
```

管理要求：

1. `HelloNote-Backend` 单独初始化 Git 仓库。
2. `HelloNote-Frontend` 单独初始化 Git 仓库。
3. 两个项目分别配置自己的远程仓库。
4. 两个项目分别进行 Commit 和 Push。
5. 父目录 `Hello!Note` 不初始化 Git 仓库。
6. 前后端的提交历史、分支和版本互不影响。

## 1.2 核心管理原则

Git 主要管理项目的源代码、必要配置、开发规范和项目文档。

以下内容默认不纳入 Git：

- 可以通过包管理工具重新安装的依赖目录。
- 可以通过构建命令重新生成的构建产物。
- 个人本地开发环境配置。
- 不需要共享的 AI Skills。
- 敏感信息和临时运行数据。

但是，需要注意：

**依赖安装目录不提交，不代表依赖声明文件也不提交。**

例如：

| 文件或目录               | 是否纳入 Git |
| ------------------- | -------- |
| `package.json`      | 是        |
| `package-lock.json` | 是        |
| `node_modules/`     | 否        |
| `pyproject.toml`    | 是        |
| `uv.lock`           | 是        |
| `.venv/`            | 否        |
| `dist/`             | 否        |

---

# 二、Git 文件管理规范

## 2.1 必须纳入 Git 管理的文件

这类文件直接影响项目运行、开发规范、代码质量或项目协作。

| 文件或目录               | 管理要求 | 说明                      |
| ------------------- | ---- | ----------------------- |
| 项目源代码               | 纳入   | Python、Vue、TypeScript 等 |
| 项目配置文件              | 纳入   | Vite、Tailwind、ESLint 等  |
| 项目 Rules            | 纳入   | 项目级开发约束和 AI 编码规则        |
| `README.md`         | 纳入   | 项目介绍和运行说明               |
| `.gitignore`        | 纳入   | Git 忽略规则                |
| `.env.example`      | 纳入   | 环境变量模板                  |
| `package.json`      | 纳入   | 前端依赖声明                  |
| `package-lock.json` | 纳入   | npm 依赖版本锁定              |
| `pyproject.toml`    | 纳入   | Python 项目依赖及配置          |
| `uv.lock`           | 纳入   | Python 依赖版本锁定（使用 uv 时）  |
| Alembic 迁移文件        | 纳入   | 数据库结构变更记录               |
| 测试代码                | 纳入   | 单元测试、接口测试等              |
| 项目文档                | 纳入   | 架构、开发和部署说明              |

## 2.2 默认不纳入 Git 管理的文件

| 文件或目录            | 管理要求 | 原因           |
| ---------------- | ---- | ------------ |
| `node_modules/`  | 忽略   | 可通过 npm 重新安装 |
| `dist/`          | 忽略   | 可通过构建命令重新生成  |
| `dist-ssr/`      | 忽略   | 可重新构建        |
| `.venv/`         | 忽略   | Python 虚拟环境  |
| `venv/`          | 忽略   | Python 虚拟环境  |
| `__pycache__/`   | 忽略   | Python 缓存    |
| `*.pyc`          | 忽略   | Python 字节码   |
| `.pytest_cache/` | 忽略   | 测试缓存         |
| `.vite/`         | 忽略   | Vite 缓存      |
| `.env`           | 忽略   | 本地环境变量       |
| `*.log`          | 忽略   | 运行日志         |
| `.idea/`         | 默认忽略 | 个人 IDE 配置    |
| `.DS_Store`      | 忽略   | macOS 系统文件   |
| `Thumbs.db`      | 忽略   | Windows 系统文件 |

## 2.3 特殊文件管理原则

| 文件类型               | 管理方式 | 说明            |
| ------------------ | ---- | ------------- |
| 数据库迁移文件            | 纳入   | 保证数据库结构变更可追踪  |
| 本地数据库文件            | 默认忽略 | 避免提交本地业务数据    |
| 用户上传附件             | 默认忽略 | 不属于项目源代码      |
| 用户生成的数据            | 默认忽略 | 属于运行时数据       |
| Dockerfile         | 纳入   | 项目构建和运行配置     |
| docker-compose.yml | 纳入   | 项目服务编排配置      |
| 部署配置模板             | 纳入   | 不包含真实密钥       |
| 个人部署配置             | 默认忽略 | 可能包含环境差异或敏感信息 |

---

# 三、AI Rules 和 Skills 管理规范

## 3.1 管理原则

不同 IDE 和 AI 编程工具可能使用不同的 Rules 和 Skills 目录结构。

例如：

- 有些工具将 Rules 放在项目根目录下。
- 有些工具将 Rules 放在隐藏目录中。
- 有些工具使用 Markdown 文件定义规则。
- 有些工具通过配置文件引用其他规则文件。
- 有些工具将 Skills 放在项目目录中。
- 有些工具将 Skills 放在用户主目录或 IDE 的全局配置目录中。

因此，不能通过固定目录名称判断某个文件是否应该纳入 Git。

**必须根据实际开发环境、项目目录结构和文件用途进行判断。**

## 3.2 Rules 管理规范

项目 Rules 用于约束项目开发行为，例如：

- 项目架构和目录结构。
- 前后端代码规范。
- API 接口设计规范。
- 数据库设计规范。
- 命名规范。
- 异常处理规范。
- 安全要求。
- AI 代码生成和修改约束。

这些规则属于项目开发规范，原则上需要纳入 Git 管理。

例如，某个 IDE 使用以下目录：

```
HelloNote-Backend/
├── .ai/
│   └── rules/
│       ├── architecture.md
│       └── python-style.md
```

另一个 IDE 可能使用：

```
HelloNote-Backend/
├── .cursor/
│   └── rules/
│       ├── architecture.mdc
│       └── python-style.mdc
```

无论实际目录名称是什么，只要其中的文件属于项目级 Rules，并且需要在其他开发环境中继续使用，就应当纳入 Git 管理。

### Rules 管理要求

1. 优先识别项目级 Rules，而不是个人全局 Rules。
2. 项目级 Rules 默认纳入 Git。
3. 个人临时规则、实验规则默认不纳入 Git。
4. 不要因为 Rules 所在目录是隐藏目录就直接忽略。
5. 如果 Rules 目录与 Skills 目录处于同一个父目录，应当分别处理，不能直接忽略整个父目录。
6. Rules 如果引用其他规则文件，被引用的项目级文件也应纳入 Git。
7. 对于 IDE 自动生成的个人配置，应当根据实际用途判断，不能将其全部视为项目 Rules。

## 3.3 Skills 管理规范

Skills 主要用于扩展 AI 工具的辅助开发能力，通常包含：

- 特定任务的执行流程。
- 操作指南。
- 辅助脚本。
- 工具调用说明。
- 特定领域的知识和工作方法。

Skills 是否纳入 Git，需要根据实际用途判断。

默认情况下：

**个人安装的、全局使用的、可以独立安装或重新获取的 Skills，不纳入项目 Git 管理。**

但是，以下情况需要区别处理：

| Skills 类型           | Git 管理建议 | 原因         |
| ------------------- | -------- | ---------- |
| 个人全局 Skills         | 不纳入      | 属于个人开发环境   |
| IDE 自动安装的 Skills    | 不纳入      | 可以重新安装     |
| 本地临时 Skills         | 不纳入      | 不属于项目正式内容  |
| 项目专用且可独立获取的 Skills  | 默认不纳入    | 可通过安装或配置恢复 |
| 项目自行编写且必须共享的 Skills | 纳入       | 属于项目开发资产   |
| 项目运行必需的脚本或代码        | 纳入       | 实际属于项目源代码  |

需要特别注意：

如果某个 Skill 虽然位于 Skills 目录中，但它包含项目专用的业务逻辑、脚本或必要配置，就不能仅仅因为目录名称包含 `skills` 而忽略。

应该进一步判断其实际作用。

## 3.4 Rules 和 Skills 的识别流程

每次初始化 Git 或调整 `.gitignore` 时，按照以下步骤处理。

```
开始检查
   |
   v
扫描项目目录结构
   |
   v
识别 IDE 和 AI 编程工具
   |
   v
读取相关配置文件
   |
   v
定位 Rules 和 Skills
   |
   v
判断文件实际用途
   |
   +---------------------------+
   |                           |
   v                           v
是否属于项目级 Rules？     是否属于 Skills？
   |                           |
   v                           v
纳入 Git 管理              判断是否项目专用
                               |
                         +-----+-----+
                         |           |
                         v           v
                    个人/可安装    项目自定义且
                    的 Skills      必须共享
                         |           |
                         v           v
                      默认忽略     纳入 Git
```

### 实际检查步骤

**第一步：扫描项目目录。**

可以使用：

```
# 查看项目目录结构
tree -a -L 4

# 或使用 find
find . -maxdepth 4 -type f
```

**第二步：识别当前使用的 IDE 和 AI 工具。**

例如：

- Cursor
- Claude Code
- GitHub Copilot
- Codex
- 其他 AI 编程工具

不同工具的规则文件和 Skills 目录可能不同，需要根据实际情况确认。

**第三步：读取配置文件。**

检查项目根目录中的配置文件、规则文件和工具配置，确定：

- 哪些文件是项目级 Rules。
- 哪些文件是个人级配置。
- 哪些目录存放 Skills。
- 哪些文件是工具自动生成的。
- 哪些文件需要在其他开发环境中保留。

**第四步：检查 `.gitignore`。**

确保项目 Rules 没有被误忽略，个人 Skills 和临时配置已经按照实际情况设置忽略规则。

**第五步：检查 Git 跟踪结果。**

```
# 查看 Git 当前跟踪状态
git status

# 查看被忽略的文件
git status --ignored

# 查看指定文件是否被忽略
git check-ignore -v <文件路径>
```

如果某个文件已经被 Git 跟踪，即使后来添加到了 `.gitignore`，Git 也不会自动停止跟踪。

需要取消跟踪时：

```
git rm -r --cached <目录或文件>
```

注意：该操作只取消 Git 跟踪，不会删除本地文件。执行前应确认目标路径，避免误操作。

## 3.5 Rules 和 Skills 的最终约定

| 判断对象              | 默认规则    |
| ----------------- | ------- |
| 项目级 Rules         | 纳入 Git  |
| 个人级 Rules         | 默认忽略    |
| 项目专用且必须共享的 Skills | 纳入 Git  |
| 个人全局 Skills       | 不纳入 Git |
| 可独立安装的 Skills     | 默认不纳入   |
| 工具自动生成的缓存         | 不纳入     |
| 项目必需的脚本和代码        | 纳入 Git  |

最终原则：

**不根据目录名称决定是否提交，而是根据文件实际用途、项目归属和可恢复性决定。**

---

# 四、`.gitignore` 配置规范

前后端分别维护自己的 `.gitignore`。

以下是基础模板，Rules 和 Skills 相关忽略规则必须在完成实际目录扫描后再补充。

## 4.1 后端 `.gitignore`

文件位置：

`HelloNote-Backend/.gitignore`

```
# ==============================
# Python 缓存
# ==============================
__pycache__/
*.py[cod]
*.pyo

# ==============================
# Python 虚拟环境
# ==============================
.venv/
venv/
env/

# ==============================
# 环境变量
# ==============================
.env
.env.*
!.env.example

# ==============================
# 测试缓存
# ==============================
.pytest_cache/
.coverage
htmlcov/

# ==============================
# 代码检查缓存
# ==============================
.mypy_cache/
.ruff_cache/

# ==============================
# 日志
# ==============================
*.log
logs/

# ==============================
# IDE
# ==============================
.idea/
.vscode/

# ==============================
# 系统文件
# ==============================
.DS_Store
Thumbs.db
```

## 4.2 前端 `.gitignore`

文件位置：

`HelloNote-Frontend/.gitignore`

```
# ==============================
# 依赖目录
# ==============================
node_modules/

# ==============================
# 构建产物
# ==============================
dist/
dist-ssr/

# ==============================
# 环境变量
# ==============================
.env
.env.*
!.env.example

# ==============================
# 日志
# ==============================
*.log
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*

# ==============================
# 测试与缓存
# ==============================
coverage/
.vite/

# ==============================
# IDE
# ==============================
.idea/
.vscode/

# ==============================
# 系统文件
# ==============================
.DS_Store
Thumbs.db
```

### 关于 AI 目录的补充

不要直接添加这种过于宽泛的规则：

```
.ai/
.cursor/
.claude/
.agents/
```

因为这些目录可能同时包含：

- 项目 Rules。
- 项目 Skills。
- 工具配置。
- 个人临时文件。

直接忽略整个目录，可能导致项目 Rules 被遗漏。

正确方式是：

1. 先扫描目录。
2. 确认每个子目录的用途。
3. 对个人配置和不需要共享的 Skills 设置精确忽略规则。
4. 保留需要提交的 Rules 和项目共享文件。

---

# 五、Commit 提交规范

## 5.1 Commit 提交格式

统一使用 Conventional Commits 风格。

基本格式：

```
<type>: <description>
```

例如：

```
git commit -m "feat: 添加笔记创建功能"
```

其中：

- `type`：本次提交的类型。
- `description`：本次提交的具体内容。

如果需要补充模块名称，可以使用：

```
<type>(<scope>): <description>
```

例如：

```
git commit -m "feat(notes): 添加笔记创建接口"
```

这里的 `notes` 表示本次修改所属的业务模块。

两种格式均可使用，但建议整个项目保持统一。初期可以优先使用简单格式。

## 5.2 Commit 类型说明

### 1. 常用提交类型

| 类型         | 作用     | 使用场景                     | 示例                    |
| ---------- | ------ | ------------------------ | --------------------- |
| `feat`     | 新增功能   | 添加新的业务功能或接口              | `feat: 添加笔记创建功能`      |
| `fix`      | 修复问题   | 修复程序错误或异常                | `fix: 修复笔记保存失败的问题`    |
| `docs`     | 文档修改   | 修改 README、项目规划、开发文档      | `docs: 更新后端开发文档`      |
| `style`    | 代码格式调整 | 缩进、空格、分号等，不改变业务逻辑        | `style: 统一代码格式`       |
| `refactor` | 代码重构   | 优化代码结构，不改变外部功能           | `refactor: 优化笔记服务层结构` |
| `perf`     | 性能优化   | 提升程序运行或查询效率              | `perf: 优化笔记列表查询`      |
| `test`     | 测试修改   | 添加、调整或修复测试代码             | `test: 添加笔记接口测试`      |
| `build`    | 构建系统修改 | 修改构建工具、构建脚本或依赖配置         | `build: 调整前端构建配置`     |
| `ci`       | 持续集成修改 | 修改 GitHub Actions 等自动化流程 | `ci: 添加自动化测试流程`       |
| `chore`    | 日常维护   | 修改非业务性配置、工具或辅助文件         | `chore: 更新项目配置`       |
| `revert`   | 撤销提交   | 撤销之前的某次 Commit           | `revert: 撤销笔记接口修改`    |

### 2. 各类型详细说明

#### feat：新增功能

用于添加新的业务功能。

示例：

```
git commit -m "feat: 添加用户注册功能"
git commit -m "feat: 添加笔记创建接口"
git commit -m "feat: 添加笔记编辑页面"
git commit -m "feat: 添加标签管理功能"
```

#### fix：修复问题

用于修复已有功能中的 Bug。

示例：

```
git commit -m "fix: 修复用户登录失败的问题"
git commit -m "fix: 修复笔记列表分页异常"
git commit -m "fix: 修复接口参数校验错误"
```

#### docs：文档修改

用于修改项目说明和开发文档。

示例：

```
git commit -m "docs: 更新项目 README"
git commit -m "docs: 补充数据库设计说明"
git commit -m "docs: 更新 Git 管理规范"
```

#### style：代码格式调整

只修改代码格式，不改变程序逻辑。

示例：

```
git commit -m "style: 统一 Python 代码格式"
git commit -m "style: 调整 Vue 组件缩进"
```

注意：如果修改涉及代码结构或业务逻辑，不应该使用 `style`。

#### refactor：代码重构

用于改善代码结构、降低耦合度、提高可维护性，但不改变原有功能。

示例：

```
git commit -m "refactor: 拆分笔记业务服务"
git commit -m "refactor: 优化 API 请求封装"
git commit -m "refactor: 调整项目目录结构"
```

#### perf：性能优化

用于提高程序性能。

示例：

```
git commit -m "perf: 优化笔记查询效率"
git commit -m "perf: 减少重复 API 请求"
```

#### test：测试修改

用于增加或调整测试代码。

示例：

```
git commit -m "test: 添加用户登录接口测试"
git commit -m "test: 补充笔记删除测试"
```

#### build：构建系统修改

用于修改项目构建工具、构建脚本和相关依赖配置。

示例：

```
git commit -m "build: 更新 Vue 项目构建配置"
git commit -m "build: 调整 Python 项目依赖"
```

注意：如果只是更新普通开发工具配置，也可以使用 `chore`。如果修改的是构建流程本身，优先使用 `build`。

#### ci：持续集成修改

用于修改自动化构建、测试和发布流程。

示例：

```
git commit -m "ci: 添加后端自动化测试"
git commit -m "ci: 配置前端自动构建"
```

#### chore：项目日常维护

用于不属于业务功能、Bug 修复或代码重构的常规维护。

示例：

```
git commit -m "chore: 更新项目配置"
git commit -m "chore: 调整 .gitignore 规则"
git commit -m "chore: 更新开发工具配置"
```

#### revert：撤销提交

用于撤销之前已经提交的修改。

示例：

```
git revert <commit-id>
```

撤销后，Git 会生成一条新的提交记录，而不是直接删除原有历史。

## 5.3 Commit 类型选择建议

遇到不确定的情况，可以按照以下原则选择：

| 实际修改内容          | 推荐类型       |
| --------------- | ---------- |
| 新增笔记功能          | `feat`     |
| 修复笔记 Bug        | `fix`      |
| 修改项目说明文档        | `docs`     |
| 仅调整代码格式         | `style`    |
| 调整代码分层和结构       | `refactor` |
| 优化接口查询性能        | `perf`     |
| 增加测试代码          | `test`     |
| 修改构建工具配置        | `build`    |
| 修改 CI/CD 流程     | `ci`       |
| 修改 `.gitignore` | `chore`    |
| 修改开发环境配置        | `chore`    |
| 撤销之前的提交         | `revert`   |

## 5.4 Commit 编写要求

1. 每次 Commit 尽量只处理一个相对独立的任务。
2. 提交描述必须明确表达修改内容。
3. 建议使用中文描述，保持项目统一。
4. 不要将多个无关功能混合提交。
5. 不要提交临时文件、调试文件和无关内容。
6. 前后端分别提交，不要跨仓库混合提交。

推荐：

```
git commit -m "feat: 添加笔记创建接口"
git commit -m "fix: 修复笔记查询异常"
git commit -m "docs: 更新项目架构文档"
```

不推荐：

```
git commit -m "update"
git commit -m "修改代码"
git commit -m "第一次提交"
git commit -m "完成"
```

---

# 六、Push 推送规范

## 6.1 Push 基本原则

Push 是将本地已经提交的 Git 记录同步到远程仓库。

管理要求：

1. 完成相对独立的功能后进行 Commit。
2. 本地测试通过后再 Push。
3. Push 前确认当前所在分支。
4. Push 前检查本地修改和提交内容。
5. 不要随意覆盖远程仓库已有的提交。
6. 不要将未完成且无法运行的代码随意推送到主分支。
7. 前端和后端分别 Push。

## 6.2 标准 Push 流程

以 `main` 分支为例：

```
# 1. 查看当前分支
git branch

# 2. 查看当前工作区状态
git status

# 3. 查看具体修改
git diff

# 4. 添加需要提交的文件
git add .

# 5. 提交修改
git commit -m "feat: 添加笔记列表功能"

# 6. 推送到远程仓库
git push origin main
```

## 6.3 Push 被拒绝时的处理

如果出现：

```
! [rejected] main -> main (fetch first)
error: failed to push some refs
```

通常表示远程仓库存在本地没有的提交。

可以先同步远程提交：

```
git pull --rebase origin main
```

没有冲突时，再执行：

```
git push origin main
```

如果出现冲突：

```
# 查看冲突文件
git status

# 手动解决冲突后
git add <冲突文件>

# 继续 rebase
git rebase --continue

# 完成后推送
git push origin main
```

如果需要放弃本次 rebase：

```
git rebase --abort
```

注意：

- 不要直接删除冲突文件。
- 不要随意使用 `git push --force`。
- 如果确实需要强制推送，必须先确认不会覆盖其他人的提交。
- 必要时优先使用 `git push --force-with-lease`，并理解其影响。

---

# 七、分支管理规范

## 7.1 分支设计

项目初期不需要复杂的 Git Flow，可以采用简单的分支管理方式。

| 分支          | 用途         |
| ----------- | ---------- |
| `main`      | 稳定、可运行的主分支 |
| `dev`       | 日常开发分支     |
| `feature/*` | 新功能开发      |
| `fix/*`     | 问题修复       |

## 7.2 分支命名规范

统一使用英文名称和短横线。

例如：

```
feature/note-management
feature/user-auth
feature/ai-summary

fix/note-save-error
fix/login-error
```

## 7.3 创建功能分支

```
# 创建并切换到功能分支
git switch -c feature/note-management

# 查看当前分支
git branch

# 开发完成后提交
git add .
git commit -m "feat: 添加笔记管理功能"

# 推送功能分支
git push -u origin feature/note-management
```

完成开发和测试后，可以通过 Pull Request / Merge Request 合并到主分支。

## 7.4 初期分支建议

如果项目主要由个人独立开发，可以先只使用：

```
main
```

等到项目规模扩大、需要并行开发或保留稳定版本时，再引入 `dev` 和功能分支。

---

# 八、前后端独立 Git 操作

前端和后端拥有各自独立的仓库，必须分别执行 Git 操作。

## 8.1 后端 Git 操作

进入后端目录：

```
cd HelloNote-Backend
```

检查仓库：

```
git status
git branch
git remote -v
```

提交并推送：

```
git add .
git commit -m "feat: 添加笔记查询接口"
git push origin main
```

## 8.2 前端 Git 操作

进入前端目录：

```
cd HelloNote-Frontend
```

检查仓库：

```
git status
git branch
git remote -v
```

提交并推送：

```
git add .
git commit -m "feat: 添加笔记列表页面"
git push origin main
```

## 8.3 管理原则

```
后端仓库：
HelloNote-Backend
       |
       v
检查修改
       |
       v
Commit
       |
       v
Push

前端仓库：
HelloNote-Frontend
       |
       v
检查修改
       |
       v
Commit
       |
       v
Push
```

前端的 Commit 不会影响后端的 Git 历史，反之亦然。

---

# 九、日常开发 Git 工作流程

建议将以下流程作为日常开发的固定习惯。

## 9.1 开发前

```
# 查看当前分支
git branch

# 检查工作区
git status

# 同步远程仓库
git pull --rebase origin main
```

如果当前使用功能分支，则将 `main` 替换为对应分支。

## 9.2 开发过程中

完成一个相对独立的功能后：

```
# 检查修改
git status

# 查看具体差异
git diff

# 添加文件
git add .

# 提交
git commit -m "feat: 添加笔记编辑功能"
```

## 9.3 开发完成后

```
# 查看最近提交记录
git log --oneline -5

# 推送到远程仓库
git push origin main
```

## 9.4 开发结束后

确认：

- 代码已经提交。
- 代码已经推送。
- 远程仓库已经同步。
- 没有误提交敏感信息。
- 没有误提交依赖目录和构建产物。
- 没有遗留不明修改。

---

# 十、Git 常用命令速查

| 命令                            | 作用          |
| ----------------------------- | ----------- |
| `git init`                    | 初始化仓库       |
| `git clone <url>`             | 克隆远程仓库      |
| `git remote -v`               | 查看远程仓库      |
| `git remote add origin <url>` | 添加远程仓库      |
| `git status`                  | 查看工作区状态     |
| `git diff`                    | 查看未暂存的修改    |
| `git diff --cached`           | 查看已暂存的修改    |
| `git add .`                   | 添加当前目录修改    |
| `git add <file>`              | 添加指定文件      |
| `git commit -m "描述"`          | 提交修改        |
| `git log --oneline`           | 查看简洁提交记录    |
| `git branch`                  | 查看分支        |
| `git switch <branch>`         | 切换分支        |
| `git switch -c <branch>`      | 创建并切换分支     |
| `git pull --rebase`           | 拉取并变基同步     |
| `git push`                    | 推送提交        |
| `git fetch`                   | 获取远程更新但不合并  |
| `git merge <branch>`          | 合并分支        |
| `git rebase <branch>`         | 变基          |
| `git restore <file>`          | 恢复工作区文件修改   |
| `git stash`                   | 暂存未提交的修改    |
| `git check-ignore -v <file>`  | 检查文件被哪条规则忽略 |
| `git status --ignored`        | 查看被忽略的文件    |
| `git rm --cached <file>`      | 取消跟踪但保留本地文件 |

---

# 十一、Git 管理检查清单

每次提交和推送之前，可以按照以下清单进行检查。

## 11.1 仓库管理

- 前后端是否使用独立 Git 仓库？
- 两个仓库是否分别配置远程地址？
- 当前是否处于正确的项目目录？
- 当前是否处于正确的分支？

## 11.2 文件管理

- 是否扫描并检查了项目目录？
- 是否根据实际 IDE 和 AI 工具识别了 Rules 和 Skills？
- 项目级 Rules 是否纳入 Git？
- 个人级 Rules 是否按需忽略？
- 个人或可独立安装的 Skills 是否默认忽略？
- 项目必须共享的自定义 Skills 是否纳入 Git？
- `node_modules/` 是否被忽略？
- `.venv/` 是否被忽略？
- `dist/` 等构建产物是否被忽略？
- `.env` 是否被忽略？
- `.env.example` 是否保留？
- 依赖声明文件是否纳入 Git？
- 依赖锁定文件是否纳入 Git？
- 数据库迁移文件是否纳入 Git？

## 11.3 Commit 检查

- 本次修改是否已经完成？
- 是否执行了 `git status`？
- 是否检查了 `git diff`？
- 是否没有提交无关文件？
- Commit 类型是否正确？
- Commit 描述是否清楚？

## 11.4 Push 检查

- 是否确认当前分支？
- 是否确认远程仓库地址？
- 是否完成本地测试？
- 是否已经完成 Commit？
- 是否确认远程没有未同步的重要提交？
- 是否推送到了正确的远程分支？
- 是否确认远程仓库已经同步？

---

# 十二、最终 Git 管理约定

Hello!Note 项目统一遵循以下原则：

1. 前端和后端分别维护独立 Git 仓库。
2. 父工作区不初始化 Git 仓库。
3. Rules 和 Skills 不根据固定目录名称判断，而是根据实际 IDE、AI 工具、目录结构和文件用途识别。
4. 项目级 Rules 原则上纳入 Git 管理。
5. 个人级 Rules 默认不纳入 Git 管理。
6. 个人 Skills 和可独立安装的 Skills 默认不纳入 Git 管理。
7. 项目自定义且必须共享的 Skills 纳入 Git 管理。
8. 可重新安装的依赖目录不纳入 Git 管理。
9. 依赖声明文件和锁定文件必须纳入 Git 管理。
10. 可重新生成的构建产物默认不纳入 Git 管理。
11. `.env` 等敏感配置不纳入 Git 管理。
12. `.env.example` 等配置模板纳入 Git 管理。
13. 数据库迁移文件纳入 Git 管理。
14. Commit 统一采用 `type: description` 格式。
15. Push 前检查代码、分支和远程仓库状态。
16. 不随意使用强制推送覆盖远程提交。

**核心原则：Git 管理项目本身、项目规范和必要配置，而不是管理可以重新生成的环境和临时文件。**

额外建议： 以后更换 IDE 或 AI 编程工具时，不要直接复制旧的 `.gitignore` 中的 AI 目录规则。先扫描新工具生成的项目文件，再区分 Rules、Skills 和个人配置。这样能避免误删或漏提交项目级规则。**git的分支也要按照实际项目的分支提供管理**。