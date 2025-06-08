# 📚 Manus MCP Server 文档中心

## 📂 文档目录结构

```
docs/
├── 01-architecture/           # 🏗️ 架构设计
│   ├── M1-Overview-V4总体架构设计.md
│   ├── M2-Overview-V4基础服务设计总览.md
│   └── M1-Spec-MCP四段式命名空间规范.md
├── 02-modules/                # 🔧 模块详细设计  
│   ├── M2-Spec-持久化服务详细设计.md
│   ├── M2-Spec-数据库设计与优化指南.md
│   ├── M2-Spec-Redis缓存架构设计.md
│   ├── M4-Overview-V4用户中心服务设计.md
│   ├── M4-Spec-API实现指南.md
│   ├── M4-Spec-权限管理系统设计.md
│   └── M4-Spec-与模块2联合开发技术文档.md
├── 03-api-specs/              # 📝 API规范
├── 04-deployment/             # 🚀 部署文档
└── 05-project-management/     # 📋 项目管理
    └── 53天冲刺执行总计划-2025年06月08日.md
```

## 🔄 文档同步策略

### 📍 源文档位置 (母版)
```
/Users/naiyue wang/Downloads/数字人MCP Server开发与技术解决方案设计-3/
├── 01-活跃技术方案/01-核心架构设计/
└── 01-活跃技术方案/02-模块详细设计/
```

### 📍 开发文档位置 (工作副本)
```
/Users/naiyue wang/Documents/GitHub/fastapi-server/docs/
```

## 📝 文档命名规范 (Neo标准)

### 模块概览文档：`M{X}-Overview-{功能名称}.md`
- `M1-Overview-V4总体架构设计.md`
- `M2-Overview-V4基础服务设计总览.md`  
- `M4-Overview-V4用户中心服务设计.md`

### 模块规范文档：`M{X}-Spec-{规范名称}.md`
- `M1-Spec-MCP四段式命名空间规范.md`
- `M2-Spec-持久化服务详细设计.md`
- `M2-Spec-数据库设计与优化指南.md`
- `M2-Spec-Redis缓存架构设计.md`
- `M4-Spec-API实现指南.md`
- `M4-Spec-权限管理系统设计.md`
- `M4-Spec-与模块2联合开发技术文档.md`

## ⚡ 快速同步命令

### 同步所有文档到开发环境：
```bash
# 同步架构设计文档
cp "/Users/naiyue wang/Downloads/数字人MCP Server开发与技术解决方案设计-3/01-活跃技术方案/01-核心架构设计/"M*.md docs/01-architecture/

# 同步模块详细设计文档  
cp "/Users/naiyue wang/Downloads/数字人MCP Server开发与技术解决方案设计-3/01-活跃技术方案/02-模块详细设计/"M*.md docs/02-modules/
```

### Git提交更新：
```bash
git add docs/
git commit -m "docs: 同步最新设计文档 - [日期]"
git push origin naiyue_dev
```

## 🎯 当前文档状态

### ✅ P0级文档 (Neo评审中)
1. **M1-Overview**: V4总体架构设计 ✅
2. **M2-Overview**: V4基础服务设计总览 ✅  
3. **M4-Overview**: V4用户中心服务设计 ✅
4. **M1-Spec**: MCP四段式命名空间规范 ✅

### ⚠️ 待补充文档
5. **M1-Spec**: 核心协作规范 (待整理)
6. **M1-Spec**: 六维度质量标准定义 (待整理)

### 📋 P1级文档 (下一批)
- M2-Spec系列：持久化服务技术规范
- M4-Spec系列：用户中心服务技术规范

## 🚀 开发指引

### 开始开发前必读：
1. **PROJECT_CONTEXT.md** - 项目全貌
2. **M1-Overview-V4总体架构设计.md** - 架构蓝图
3. **M2-Overview-V4基础服务设计总览.md** - 技术规范

### 开发优先级：
- **P0**: 模块1(命名空间) + 模块2(持久化) + 模块4(用户中心)
- **P1**: 模块5(OAuth2) + 模块6(MCP存储库)
- **P2**: 模块7-9(业务服务)
- **P3**: 模块10-11(扩展服务)

---
**更新日期**: 2025年6月8日  
**文档状态**: ✅ 同步完成  
**当前版本**: Neo标准化命名规范 V1.0 