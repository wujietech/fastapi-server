# Manus FastAPI 服务器

自媒体 Manus 服务端

## 启动项目

### 项目依赖

* Docker

### docker 启动

```bash
docker compose watch
```

* 前端页面：http://localhost:5173/  可视化管理后台
* 后端 API 接口：http://localhost:8000/ 
* API 接口文档：http://localhost:8000/docs
* PostgreSQL 管理后台：http://localhost:8080/ 不建议直接修改数据
* Traefik UI：http://localhost:8090/ 服务监控后台

### 命令行启动

Docker Compose 启动的一整套服务，如果想让前端后端单独使用镜像外的代码调试，就需要先停掉对应的容器

#### 前端本地开发
```
# 停掉 docker compose 启动的前端
docker compose stop frontend
cd frontend
# 安装依赖
pnpm i
# 启动项目
pnpm dev
```
#### 后端本地开发
```
# 停掉 docker compose 启动的后端
docker compose stop backend
# 创建虚拟环境
uv venv --python 3.11
# 激活虚拟环境
source .venv/bin/activate
cd backend
fastapi dev app/main.py
```

## 目录结构

* `backend`：后端
* `frontend`：前端
* `img`：截图
* `scripts`：相关脚本，如构建、发布、测试用的

### backend

* 根目录文件
    * `pyproject.toml`: Python 项目依赖配置文件
    * `Dockerfile`: 用于构建 Docker 镜像
    * `alembic.ini`: 数据库迁移配置文件
    * `README.md`: 项目说明文档
* app 目录（核心应用代码）
    * 主要文件：
        * main.py: 应用程序入口点
        * models.py: 数据库模型定义
        * crud.py: 数据库 CRUD 操作
        * utils.py: 工具函数
        * initial_data.py: 初始数据设置
    * 重要子目录：
        * api/: API 路由和端点定义，其中 routes 下每个文件代表一个子路由
        * core/: 核心配置和功能
        * alembic/: 数据库迁移文件
        * tests/: 测试用例
        * email-templates/: 邮件模板
* scripts 目录
    * 包含各种脚本文件，用于部署、测试等任务

### frontend

* 根目录配置文件
    * package.json: npm 项目配置和依赖管理
    * vite.config.ts: Vite 构建工具配置
    * tsconfig.json: TypeScript 配置
    * biome.json: Biome 工具配置（代码格式化和检查）
    * nginx.conf: Nginx 服务器配置
    * Dockerfile: Docker 构建配置
* 主要目录结构
    * src/（源代码目录）
    * components/: React 组件
    * routes/: 路由配置和页面组件
    * hooks/: 自定义 React Hooks
    * theme/: UI 主题相关配置
    * client/: API 客户端代码
    * main.tsx: 应用入口文件
    * theme.tsx: 主题配置
    * utils.ts: 工具函数
    * public/: 静态资源目录
    * tests/: 测试文件目录
* 技术栈特点：
    * 使用 TypeScript 进行开发
    * 使用 Vite 作为构建工具
    * 使用 React 作为前端框架
    * 使用 Playwright 进行端到端测试
    * 使用 Nginx 作为生产环境服务器
* 项目特性：
    * 类型安全：
        * 完整的 TypeScript 配置
        * OpenAPI 类型生成（openapi-ts.config.ts）
    * 开发体验：
        * 热重载支持
        * 代码格式化和检查工具
        * 自动生成的 API 客户端
    * 测试支持：
        * Playwright 端到端测试配置
        * 专门的测试 Dockerfile
    * 容器化支持：
        * 开发和生产环境的 Docker 配置
        * Nginx 配置用于生产环境
    * 路由系统：
        * 使用现代的路由解决方案
        * 自动生成的路由树（routeTree.gen.ts）
* 环境配置：
    * .env 文件用于环境变量
    * .nvmrc 指定 Node.js 版本
    * 多环境支持（开发、测试、生产）


## 技术栈和特性

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) 用于 Python 后端 API。
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) 用于 Python SQL 数据库交互（ORM）。
    - 🔍 [Pydantic](https://docs.pydantic.dev)，由 FastAPI 使用，用于数据验证和设置管理。
    - 💾 [PostgreSQL](https://www.postgresql.org) 作为 SQL 数据库。
- 🚀 [React](https://react.dev) 用于前端。
    - 💃 使用 TypeScript、hooks、Vite 和其他现代前端技术栈组件。
    - 🎨 [Chakra UI](https://chakra-ui.com) 用于前端组件。
    - 🤖 自动生成的前端客户端。
    - 🧪 [Playwright](https://playwright.dev) 用于端到端测试。
    - 🦇 支持深色模式。
- 🐋 [Docker Compose](https://www.docker.com) 用于开发和生产环境。
- 🔒 默认安全的密码哈希。
- 🔑 JWT（JSON Web Token）认证。
- 📫 基于邮件的密码恢复。
- ✅ 使用 [Pytest](https://pytest.org) 进行测试。
- 📞 [Traefik](https://traefik.io) 作为反向代理/负载均衡器。
- 🚢 使用 Docker Compose 的部署说明，包括如何设置前端 Traefik 代理以处理自动 HTTPS 证书。
- 🏭 基于 GitHub Actions 的 CI（持续集成）和 CD（持续部署）。

### 如何使用私有仓库

如果你想要一个私有仓库，GitHub 不允许你直接 fork 它，因为它不允许更改 fork 的可见性。

但你可以执行以下操作：

- 创建一个新的 GitHub 仓库，例如 `my-full-stack`。
- 手动克隆此仓库，设置项目名称为你想使用的名称，例如 `my-full-stack`：

```bash
git clone git@github.com:fastapi/full-stack-fastapi-template.git my-full-stack
```

- 进入新目录：

```bash
cd my-full-stack
```

- 将新的 origin 设置为你的新仓库，从 GitHub 界面复制它，例如：

```bash
git remote set-url origin git@github.com:octocat/my-full-stack.git
```

- 添加此仓库作为另一个"remote"，以便之后获取更新：

```bash
git remote add upstream git@github.com:fastapi/full-stack-fastapi-template.git
```

- 将代码推送到你的新仓库：

```bash
git push -u origin master
```

### 从原始模板更新

克隆仓库并进行更改后，你可能想要获取此原始模板的最新更改。

- 确保你已将原始仓库添加为远程仓库，可以用以下命令检查：

```bash
git remote -v

origin    git@github.com:octocat/my-full-stack.git (fetch)
origin    git@github.com:octocat/my-full-stack.git (push)
upstream    git@github.com:fastapi/full-stack-fastapi-template.git (fetch)
upstream    git@github.com:fastapi/full-stack-fastapi-template.git (push)
```

- 拉取最新更改但不合并：

```bash
git pull --no-commit upstream master
```

这将下载此模板的最新更改但不提交它们，这样你可以在提交之前检查所有内容是否正确。

- 如果有冲突，在编辑器中解决它们。

- 完成后，提交更改：

```bash
git merge --continue
```

### 配置

你可以在 `.env` 文件中更新配置以自定义你的设置。

在部署之前，确保至少更改以下值：

- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`
- `POSTGRES_PASSWORD`

你可以（也应该）从 secrets 中以环境变量的形式传递这些值。

阅读 [deployment.md](./deployment.md) 文档了解更多详情。

### 生成密钥

`.env` 文件中的某些环境变量默认值为 `changethis`。

你必须用密钥更改它们，要生成密钥可以运行以下命令：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

复制内容并用作密码/密钥。再次运行该命令以生成另一个安全密钥。

## 如何使用 - 使用 Copier 的替代方案

此仓库还支持使用 [Copier](https://copier.readthedocs.io) 生成新项目。

它将复制所有文件，询问你配置问题，并用你的答案更新 `.env` 文件。

### 安装 Copier

你可以通过以下方式安装 Copier：

```bash
pip install copier
```

或者更好的是，如果你有 [`pipx`](https://pipx.pypa.io/)，你可以用以下命令运行：

```bash
pipx install copier
```

**注意**：如果你有 `pipx`，安装 copier 是可选的，你可以直接运行它。

### 使用 Copier 生成项目

为你的新项目目录决定一个名称，你将在下面使用它。例如，`my-awesome-project`。

转到将作为项目父目录的目录，并使用你的项目名称运行命令：

```bash
copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
```

如果你有 `pipx` 但没有安装 `copier`，你可以直接运行它：

```bash
pipx run copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
```

**注意** `--trust` 选项是必需的，以便能够执行[创建后脚本](https://github.com/fastapi/full-stack-fastapi-template/blob/master/.copier/update_dotenv.py)来更新你的 `.env` 文件。

### 输入变量

Copier 会询问你一些数据，你可能想在生成项目之前准备好这些数据。

但不用担心，之后你可以在 `.env` 文件中更新任何内容。

输入变量及其默认值（部分自动生成）是：

- `project_name`：（默认：`"FastAPI Project"`）项目名称，显示给 API 用户（在 .env 中）。
- `stack_name`：（默认：`"fastapi-project"`）用于 Docker Compose 标签和项目名称的堆栈名称（无空格，无句点）（在 .env 中）。
- `secret_key`：（默认：`"changethis"`）项目的密钥，用于安全性，存储在 .env 中，你可以用上述方法生成一个。
- `first_superuser`：（默认：`"admin@example.com"`）第一个超级用户的邮箱（在 .env 中）。
- `first_superuser_password`：（默认：`"changethis"`）第一个超级用户的密码（在 .env 中）。
- `smtp_host`：（默认：""）用于发送邮件的 SMTP 服务器主机，你可以稍后在 .env 中设置。
- `smtp_user`：（默认：""）用于发送邮件的 SMTP 服务器用户，你可以稍后在 .env 中设置。
- `smtp_password`：（默认：""）用于发送邮件的 SMTP 服务器密码，你可以稍后在 .env 中设置。
- `emails_from_email`：（默认：`"info@example.com"`）用于发送邮件的邮箱账户，你可以稍后在 .env 中设置。
- `postgres_password`：（默认：`"changethis"`）PostgreSQL 数据库的密码，存储在 .env 中，你可以用上述方法生成一个。
- `sentry_dsn`：（默认：""）Sentry 的 DSN，如果你使用它，你可以稍后在 .env 中设置。

## 后端开发

后端文档：[backend/README.md](./backend/README.md)。

## 前端开发

前端文档：[frontend/README.md](./frontend/README.md)。

## 部署

部署文档：[deployment.md](./deployment.md)。

## 开发

通用开发文档：[development.md](./development.md)。

这包括使用 Docker Compose、自定义本地域名、`.env` 配置等。

## 发布说明

查看文件 [release-notes.md](./release-notes.md)。

## 许可证

Full Stack FastAPI Template 根据 MIT 许可证的条款获得许可。
