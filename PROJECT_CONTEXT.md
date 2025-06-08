# 🚀 Manus MCP Server 项目开发上下文

## 📋 项目概述

**项目名称**: Agent-TARS与Manus MCP Server联合架构开发  
**开发期限**: 2025年6月8日 - 2025年7月31日 (53天冲刺)  
**项目性质**: 多模态AI Agent平台核心基础设施  
**技术栈**: FastAPI + PostgreSQL + Redis + MCP协议  

## 🎯 核心目标

构建一个支撑**百万级并发用户**的AI Agent工具平台，核心组件：
- **Agent-TARS**: 客户端应用
- **ScaleMCP**: 统一网关  
- **Manus MCP Server**: 核心服务平台

## 🏗️ 模块化架构设计

### 已完成设计文档的模块：
1. **模块1**: 核心架构原则与命名空间机制 (`sys.*`)
2. **模块2**: 持久化服务 (`sys.storage.persistence`)  
3. **模块4**: 用户中心服务 (`sys.service.user_center`)

### 待开发模块：
4. **模块5**: OAuth2服务 (`sys.service.oauth2`)
5. **模块6**: MCP存储库 (`sys.service.mcp_repository`)
6. **模块7**: ScaleMCP统一网关
7. **模块8**: Task Management (`sys.compute.general.task_management`)
8. **模块9**: Server File Management (`sys.storage.server_file`)
9. **模块10**: 小红书MCP Server
10. **模块11**: 数字人MCP Server

## 📚 核心设计文档位置

```
docs/
├── 01-architecture/           # 架构设计
│   ├── M1-Overview-V4总体架构设计.md
│   ├── M2-Overview-V4基础服务设计总览.md
│   └── M1-Spec-MCP四段式命名空间规范.md
├── 02-modules/                # 模块详细设计  
│   ├── M4-Overview-V4用户中心服务设计.md
│   └── ...
├── 03-api-specs/              # API规范
├── 04-deployment/             # 部署文档
└── 05-project-management/     # 项目管理
    └── 53天冲刺执行总计划-2025年06月08日.md
```

## 🔧 技术架构关键点

### 核心技术特性：
- **命名空间机制**: 四段式结构 `<Scope>.<Category>.<Service>.<Function>`
- **UUID V7**: 时间排序的全局唯一标识符
- **分片策略**: PostgreSQL基于user_id分片，Redis集群缓存
- **MCP协议**: 服务间标准化通信协议

### 性能要求：
- **并发用户**: 100万+
- **响应时间**: < 100ms (P95)
- **可用性**: 99.9%
- **数据一致性**: 强一致性(核心数据) + 最终一致性(缓存)

## 💻 开发环境要求

### 基础技术栈：
```python
# 后端框架
FastAPI >= 0.104.0
uvicorn >= 0.24.0

# 数据库
PostgreSQL >= 14.0  
asyncpg >= 0.29.0
SQLAlchemy >= 2.0.0

# 缓存
Redis >= 7.0
redis >= 5.0.0

# 其他核心依赖
pydantic >= 2.5.0
python-multipart >= 0.0.6
```

### 开发工具：
- **IDE**: Cursor AI + VSCode
- **版本控制**: Git (GitHub)
- **容器化**: Docker + Docker Compose
- **API文档**: FastAPI自动生成OpenAPI

## 🚦 开发阶段规划

### Phase 1 (6月8-20日): 基础服务开发
- [x] 项目初始化与环境搭建
- [ ] 模块1: 核心架构与命名空间
- [ ] 模块2: 持久化服务 (PostgreSQL + Redis)
- [ ] 模块4: 用户中心服务

### Phase 2 (6月21-7月5日): 核心服务开发  
- [ ] 模块5: OAuth2认证服务
- [ ] 模块6: MCP存储库服务
- [ ] 模块7: ScaleMCP网关

### Phase 3 (7月6-20日): 业务服务开发
- [ ] 模块8: Task Management服务
- [ ] 模块9: Server File Management
- [ ] 模块10: 小红书MCP Server

### Phase 4 (7月21-31日): 集成测试与优化
- [ ] 模块11: 数字人MCP Server  
- [ ] 系统集成测试
- [ ] 性能优化与部署

## 👥 团队协作

### 核心团队：
- **naiyue (王廼悦)**: 项目负责人、产品设计
- **Neo**: 技术架构师、文档评审专家
- **Alex (Cursor AI)**: 技术开发伙伴、代码生成

### 协作原则：
- **分秒必争日日精进** 🌟
- **文档驱动开发**: 设计先行，代码跟随
- **双重验证**: naiyue+Alex技术验证 → Neo专业评审
- **质量第一**: 六维度质量标准 (功能性、可靠性、性能、可维护性、可用性、安全性)

## 🔍 开发指导原则

### 代码质量标准：
1. **可读性**: 清晰的函数命名、充分的注释
2. **可测试性**: 单元测试覆盖率 > 90%
3. **可维护性**: 模块化设计、职责单一
4. **性能优化**: 异步编程、连接池、缓存策略
5. **安全性**: 输入验证、权限控制、数据加密

### API设计规范：
- **RESTful设计**: 语义化URL、HTTP状态码
- **统一响应格式**: 标准化JSON响应结构
- **错误处理**: 统一错误码体系和异常处理
- **文档完整**: 自动生成的OpenAPI文档

## 📄 重要文档引用

开发过程中请重点参考：
1. `docs/01-architecture/M1-Overview-V4总体架构设计.md` - 整体架构设计
2. `docs/01-architecture/M2-Overview-V4基础服务设计总览.md` - 技术实现规范  
3. `docs/02-modules/M4-Overview-V4用户中心服务设计.md` - 用户管理系统
4. `docs/05-project-management/53天冲刺执行总计划-2025年06月08日.md` - Neo制定的执行计划

## 🚀 下一步行动

### 立即开始的任务：
1. **环境验证**: 确认PostgreSQL、Redis连接正常
2. **基础框架**: 搭建FastAPI项目结构  
3. **数据模型**: 实现用户账户与身份档案分离模型
4. **API框架**: 建立统一的API响应和错误处理机制

### 开发优先级：
- **P0**: 模块1命名空间机制 + 模块2持久化服务
- **P1**: 模块4用户中心服务 + 模块5OAuth2服务  
- **P2**: 模块6-9核心服务模块
- **P3**: 模块10-11业务扩展模块

---

**项目座右铭**: 在53天内创造技术奇迹！💪  
**成功标准**: 2025年7月31日前交付完整可用的百万级并发AI Agent平台！🎯 