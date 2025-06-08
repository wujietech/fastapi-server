# 模块4：用户中心服务与模块2 持久化服务联合开发技术文档 (修订版)

本文档根据最新修订的《模块4: 用户中心服务详细设计文档 (修订版)》的要求，修订《模块4 用户中心服务与模块2 持久化服务联合开发技术文档》，重点阐明模块2持久化服务为支持修订后的模块4用户中心服务（特别是围绕用户账户 (`user_account`) 与用户身份档案 (`user_identity_profile`) 分离，每个身份档案拥有独立 `user_id`，权限和权益严格关联到身份档案 `user_id` 的新设计）所需提供的数据库与Redis数据结构以及API接口。

## 1. 集成概述

模块4用户中心服务（`sys.service.user_center`）依赖模块2持久化服务（`sys.storage.persistence`）实现所有用户相关数据的持久化和高性能访问。

修订后的模块4设计引入了用户账户 (`account_id`) 和用户身份档案 (`user_id`) 的核心分离。一个用户账户 (`account_id`) 可以拥有多个用户身份档案 (`user_id`)，每个身份档案对应一个特定的角色上下文，并拥有独立的 `user_id`。权限和权益不再关联到单一用户ID或账户，而是严格关联到特定的用户身份档案 (`user_id`)。

这种新模型要求模块2持久化服务：
1.  管理新的 PostgreSQL 表结构，以支持账户和身份档案的分离以及它们之间的关联。
2.  继续为模块4提供对 Redis 中用户实时权限状态和消耗数据的管理和访问能力，但这些数据现在是针对特定用户身份档案的 `user_id` 进行存储和操作。
3.  支持模块4在用户账户下创建新的身份档案（对应新增角色 `user_id` 实例）时所需的数据操作。
4.  提供适配新数据结构的API接口，支持模块4实现用户选择和切换身份档案 (`user_id`) 并使用其对应权益的场景。

模块2继续扮演统一数据基础设施服务的角色，封装底层 PostgreSQL 和 Redis 的复杂性，为模块4提供高性能、可扩展的数据支持，确保数据模型的一致性反映最新的用户中心设计。

## 2. 模块2为模块4提供的数据库与Redis数据结构补充

根据修订后的模块4设计，模块2持久化服务需要管理和/或提供访问能力的核心数据结构进行了调整。

### 2.1 PostgreSQL 数据结构 (由模块2管理)

模块2需要管理以下PostgreSQL表，作为用户中心服务中用户基本信息、社交账号、登录历史、身份档案以及权限/角色/权益定义和分配的事实来源。

#### 2.1.1 `user_accounts` 表 (用户账户实体) - 新增

此表存储账户级别的、与特定身份档案无关的信息。模块2需要管理此表。

| 字段名称          | 数据类型                   | 约束           | 索引策略               | 说明                                   |
| :---------------- | :------------------------- | :------------- | :--------------------- | :------------------------------------- |
| `account_id`      | `UUID`                     | `PRIMARY KEY`  | 主键索引               | 用户账户唯一标识符 (UUID V7)             |
| `email`           | `VARCHAR(255)`             | `NULL`, `UNIQUE` | 可选唯一索引（如果非空） | 邮箱地址，可作为登录凭据                 |
| `phone_number_cn` | `VARCHAR(20)`              | `NULL`, `UNIQUE` | 可选唯一索引（如果非空） | 中国大陆手机号，可作为登录凭据           |
| `password_hash`   | `TEXT`                     | `NULL`         | 无                     | 密码哈希值 (包含盐值和算法信息)            |
| `status`          | `VARCHAR(50)`              | `NOT NULL`     | 可选索引               | 账户状态 (e.g., 'active', 'inactive', 'suspended') |
| `created_at`      | `TIMESTAMP WITH TIME ZONE` | `NOT NULL`     | 索引                   | 创建时间                               |
| `updated_at`      | `TIMESTAMP WITH TIME ZONE` | `NOT NULL`     | 索引                   | 最后更新时间                           |
| `profile_data`    | `JSONB`                    | `NULL`         | 无                     | 账户级别属性 (e.g., 账户名称)            |
| `sharding_key`    | `UUID`                     | `NOT NULL`     | 分片键索引             | 冗余 `account_id` 作为分片键           |

#### 2.1.2 `user_identity_profiles` 表 (用户身份档案实体) - 原 `users` 表修订并拆分

此表存储用户账户下的身份档案，每个身份档案代表一个特定的角色或上下文，具有独立的 `user_id`。这是原 `users` 表在逻辑上的主要继承者，但结构显著调整，并与 `user_accounts` 关联。模块2需要管理此表。

| 字段名称          | 数据类型                   | 约束           | 索引策略               | 说明                                                                 |
| :---------------- | :------------------------- | :------------- | :--------------------- | :------------------------------------------------------------------- |
| `user_id`         | `UUID`                     | `PRIMARY KEY`  | 主键索引               | 用户身份档案唯一标识符 (UUID V7)，用于权限/权益关联和 API 调用上下文   |
| `account_id`      | `UUID`                     | `NOT NULL`     | 索引, 分片键           | 关联的用户账户 ID (`user_identity_profiles.account_id` REFERENCES `user_accounts.account_id`) |
| `role_id`         | `UUID`                     | `NOT NULL`     | 索引                   | 关联的角色 ID (`user_identity_profiles.role_id` REFERENCES `sys_roles.role_id`) |
| `username`        | `VARCHAR(128)`             | `NOT NULL`     | 无                     | 身份档案的显示名称，仅用于前端UI显示，允许存在重名                   |
| `status`          | `VARCHAR(50)`              | `NOT NULL`     | 可选索引               | 身份档案状态 (e.g., 'active', 'inactive', 'suspended')               |
| `created_at`      | `TIMESTAMP WITH TIME ZONE` | `NOT NULL`     | 索引                   | 创建时间                                                             |
| `updated_at`      | `TIMESTAMP WITH TIME ZONE` | `NOT NULL`     | 索引                   | 最后更新时间                                                         |
| `profile_data`    | `JSONB`                    | `NULL`         | 无                     | 其他身份档案属性，JSONB格式 (e.g., nickname, avatar_url for this specific profile) |
| `sharding_key`    | `UUID`                     | `NOT NULL`     | 分片键索引             | 冗余 `account_id` 作为分片键                                         |

*   与原 `users` 表的主要区别: 字段精简，新增 `account_id` 和 `role_id` 关联。`email`, `phone_number_cn`, `password_hash` 移至 `user_accounts`。`roles`, `tiers` 字段移除，由单一 `role_id` 关联取代。

#### 2.1.3 `user_social_accounts` 表 (社交账号关联) - 修订关联

此表关联到用户账户 (`account_id`)，而非具体的身份档案 (`user_id`)。模块2需要管理此表。

| 字段名称      | 数据类型                   | 约束               | 索引策略       | 说明                   |
| :------------ | :------------------------- | :----------------- | :------------- | :--------------------- |
| `id`          | `UUID`                     | `PRIMARY KEY`      | 主键索引       | 记录唯一标识符 (UUID V7) |
| `account_id`  | `UUID`                     | `NOT NULL`         | 索引, 分片键   | 关联用户账户 ID          |
| `provider`    | `VARCHAR(50)`              | `NOT NULL`         | 索引           | 社交平台提供商           |
| `social_id`   | `VARCHAR(255)`             | `NOT NULL`, `UNIQUE` | 唯一索引（复合 `provider`） | 社交平台提供的唯一ID |
| `created_at`  | `TIMESTAMP WITH TIME ZONE` | `NOT NULL`         | 索引           | 关联时间               |

#### 2.1.4 `login_history` 表 (登录历史) - 修订关联

此表关联到用户账户 (`account_id`)，记录账户级别的登录行为。模块2需要管理此表。

| 字段名称      | 数据类型               | 约束       | 索引策略 | 说明       |
| :------------ | :--------------------- | :--------- | :------- | :--------- |
| `id`          | `UUID`                 | `PRIMARY KEY` | 主键索引 | 记录唯一标识符 (UUID V7) |
| `account_id`  | `UUID`                 | `NOT NULL` | 索引, 分片键 | 用户账户 ID     |
| `timestamp`   | `TIMESTAMP WITH TIME ZONE` | `NOT NULL` | 索引     | 登录时间   |
| `login_method`| `VARCHAR(50)`          | `NULL`     | 索引     | 登录方式   |
| `ip_address`  | `VARCHAR(45)`          | `NULL`     | 可选索引 | 登录 IP 地址 |
| `user_agent`  | `TEXT`                 | `NULL`     | 无       | 用户代理信息 |
| `success`     | `BOOLEAN`              | `NOT NULL` | 可选索引 | 是否成功登录 |
| `details`     | `JSONB`                | `NULL`     | 可选索引 | 其他详情   |

#### 2.1.5 `sys_permissions` 表 (系统权限/权益定义)

模块2需要管理此表，结构同原文档，作为系统中所有权限和权益项的定义源。

#### 2.1.6 `sys_roles` 表 (系统角色定义)

模块2需要管理此表，结构同原文档，作为系统中所有角色类型的定义源。在新的设计中，一个身份档案 (`user_identity_profile`) 严格关联一个 `role_id`。

#### 2.1.7 `sys_role_permissions` 表 (角色权限关联)

模块2需要管理此表，结构同原文档，定义特定角色类型 (`role_id`) 包含哪些权限/权益及其配置。这些配置是计算身份档案 (`user_id`) 生效权限的基础。

#### 2.1.8 `user_roles` 表 - 已废弃

根据新的用户中心设计，用户直接被赋予角色记录的功能已转移至 `user_identity_profiles` 表的 `role_id` 字段（一个身份档案即为一个用户账户在特定角色下的体现）。此表在新的设计中不再使用，模块2无需为其提供管理能力。

PostgreSQL 数据结构总结: 模块2需要具备对 `user_accounts`, `user_identity_profiles`, `user_social_accounts`, `login_history`, `sys_permissions`, `sys_roles`, `sys_role_permissions` 这七张表的创建、管理和CRUD操作能力，并根据模块2设计原则（如分片基于 `account_id` 或 ID）进行实现。`user_roles` 表相关能力不再需要。

### 2.2 Redis 数据结构 (由模块2管理和暴露访问) - 聚焦身份档案 `user_id`

模块4基于Redis的高性能权限/权益方案现在严格关联到用户身份档案的 `user_id`。模块2作为持久化服务，负责管理和提供访问以下Redis数据结构，这些结构存储特定用户身份档案 (`user_id`) 实时生效的权限、权益配置和消耗数据。

模块2的职责： Redis Cluster连接管理、Key Sharding (基于 `{user_id}` Key Tag)、受控的、原子性的Redis操作接口。

#### 2.2.1 用户身份档案实时权限/权益配置 (Hash)

-   用途: 存储特定用户身份档案 (`user_id`) 所有实时生效的、计算合并后的权限和权益的配置信息。用于快速授权检查。
-   Key: `user_perms:{user_id}`
    -   `user_id` 是 `user_identity_profiles` 表中的身份档案ID。
    -   使用 `{user_id}` 作为Key Tag，确保属于同一身份档案的权限配置存储在同一个Hash Slot。
-   Type: Hash
-   Fields & Values:
    -   Field: `<permission_name>` (string) - 权限或权益的唯一名称。
    -   Value: `<JSON string of effective config>` (string) - 经过模块4计算合并后，该身份档案 (`user_id`) 对该权限/权益的最终生效配置。例如：
        ```json
        {
          "enabled": true,      // 是否启用
          "limit": 100,         // 限制值 (-1表示无限)
          "unit": "count",      // 单位 (count, bytes, duration, etc.)
          "resets_at": 1678881994 // 下次重置时间戳 (仅对有时限消耗型有效)
        }
        ```
-   管理: 模块4通过调用模块2提供的Redis写入能力（如HMSET代理或封装）来创建或更新此Hash。模块4在用户身份档案创建或其关联角色 (`role_id`) 变更后，针对该身份档案的 `user_id` 计算并提供完整的Hash内容给模块2进行原子更新。

#### 2.2.2 用户身份档案消耗型权益计数器 (String)

-   用途: 存储特定用户身份档案 (`user_id`) 消耗型权益的当前消耗值。用于实时消耗扣减。
-   Key: `user_cons:{user_id}:<right_name>`
    -   `user_id` 是 `user_identity_profiles` 表中的身份档案ID。
    -   使用 `{user_id}` 作为Key Tag，确保属于同一身份档案的消耗计数器与权限配置在同一个Hash Slot。`<right_name>` 是具体的消耗型权益名称。
-   Type: String (存储数值的字符串表示)
-   Value: 特定身份档案 (`user_id`) 的当前消耗数值。
-   管理:
    -   模块4通过调用模块2提供的原子操作能力（如INCRBY/DECRBY代理或封装，或Lua脚本执行代理）来增加或减少此String的值，操作对象是传入的特定 `user_id` 对应的Key。
    -   模块4负责根据`user_perms:{user_id}`中的`resets_at`配置，触发定期重置，通过模块2将特定 `user_id` 的此Key的值设置为"0"。

#### 2.2.3 Redis 数据结构部署方案

-   模块2依赖平台统一维护的Redis Cluster基础设施。
-   模块2的内部逻辑或DAL层负责连接到Redis Cluster，并根据Key Tag `{user_id}` 进行命令路由。
-   模块2向模块4暴露的API（或内部调用接口）应是操作的抽象，而非直接暴露Redis连接句柄。模块4调用时传入的是需要操作的身份档案 `user_id`。

## 3. 模块2为模块4提供的API补充

除了原联合开发文档中列出的`users`、`user_social_accounts`、`login_history`等表的CRUD API，模块2需要为模块4补充或调整以下API或能力：

### 3.1 PostgreSQL 数据管理 API (为新增/修订的表补充 CRUD，废弃 `user_roles`)

模块2应提供针对当前生效的PostgreSQL表的标准 CRUD API：`user_accounts`, `user_identity_profiles`, `user_social_accounts`, `login_history`, `sys_permissions`, `sys_roles`, `sys_role_permissions`。

*   新增/修订的 API 示例 (详细规范参考模块2 API规格文档):
    *   `user_accounts` 相关:
        *   `POST /sys/storage/persistence/v1/user-accounts`: 创建用户账户
        *   `GET /sys/storage/persistence/v1/user-accounts/{accountId}`: 获取用户账户
        *   `PUT/PATCH /sys/storage/persistence/v1/user-accounts/{accountId}`: 更新用户账户
        *   `GET /sys/storage/persistence/v1/user-accounts`: 查询用户账户列表 (支持过滤)
        *   `DELETE /sys/storage/persistence/v1/user-accounts/{accountId}`: 删除用户账户
        *   *可能需要特定的验证/登录 API，或者这部分逻辑封装在M4内部调用M2的查询能力实现。*
    *   `user_identity_profiles` 相关:
        *   `POST /sys/storage/persistence/v1/user-identity-profiles`: 创建用户身份档案 (包含 `account_id`, `role_id`, 生成新的 `user_id`)
        *   `GET /sys/storage/persistence/v1/user-identity-profiles/{userId}`: 获取特定 `user_id` 的身份档案详情
        *   `GET /sys/storage/persistence/v1/user-identity-profiles?account_id={accountId}`: 查询特定 `account_id` 下的所有身份档案列表
        *   `PUT/PATCH /sys/storage/persistence/v1/user-identity-profiles/{userId}`: 更新身份档案信息 (包括 `role_id`)
        *   `DELETE /sys/storage/persistence/v1/user-identity-profiles/{userId}`: 删除身份档案
        *   *需要支持按 `account_id` 分片查询，以高效获取一个账户下的所有身份档案。*
    *   `user_social_accounts` 相关:
        *   现有 API 需调整，使其关联 `account_id` 而非旧的 `user_id`。例如 `POST /v1/user-social-accounts` 请求体中应包含 `account_id`。
    *   `login_history` 相关:
        *   现有 API 需调整，使其关联 `account_id` 而非旧的 `user_id`。例如 `POST /v1/login-history` 请求体中应包含 `account_id`。
    *   `sys_permissions`, `sys_roles`, `sys_role_permissions` 相关: 保持原有的 CRUD API。
    *   `user_roles` 相关: 明确废弃或删除所有针对此表的 API。

### 3.2 Redis 数据访问能力 (模块4通过模块2访问 Redis) - 聚焦身份档案 `user_id`

模块2需要为模块4提供访问其管理的Redis Cluster中用户身份档案 (`user_id`) 权限/权益数据的能力。模块4在调用这些API时，必须提供目标身份档案的 `user_id`。

*   模块2提供的 Redis 操作抽象 (由模块4调用):
    *   获取用户身份档案权限/权益配置:
        *   目的: 供模块4在处理`check_permission`或`get_identity_profile_permissions` API时快速读取特定身份档案 (`user_id`) 的生效权限配置。
        *   模块2暴露方式: 提供根据 `user_id` 获取Hash字段值或所有字段的接口。
        *   示例调用 (模块4调用模块2内部接口或特定API): `persistence.redis.hget(userId, permission_name)` 或 `persistence.redis.hgetall(userId)` (这里`userId`是身份档案ID，模块2内部负责构建完整的Key `user_perms:{userId}`)
    *   获取用户身份档案消耗计数:
        *   目的: 供模块4在处理`check_permission` (检查剩余) 或`get_identity_profile_permissions` API时读取特定身份档案 (`user_id`) 的消耗值。
        *   模块2暴露方式: 提供根据 `user_id` 和权益名称获取String值的接口。
        *   示例调用: `persistence.redis.get(userId, right_name)` (模块2内部构建Key `user_cons:{userId}:<right_name>`)
    *   设置用户身份档案权限/权益配置:
        *   目的: 供模块4的后台任务在特定身份档案 (`user_id`) 权限/权益计算后更新Redis。需要原子性更新整个Hash。
        *   模块2暴露方式: 提供根据 `user_id` 设置Hash多个字段的接口。
        *   示例调用: `persistence.redis.hmset(userId, field_value_map)` (模块2内部构建Key `user_perms:{userId}`)
    *   初始化/重置用户身份档案消耗计数:
        *   目的: 供模块4的后台任务或重置逻辑清零特定身份档案 (`user_id`) 的消耗计数。
        *   模块2暴露方式: 提供根据 `user_id` 和权益名称设置String值的接口。
        *   示例调用: `persistence.redis.set(userId, right_name, value)` (模块2内部构建Key `user_cons:{userId}:<right_name>`)
    *   原子性扣减/增加用户身份档案消耗计数:
        *   目的: 供模块4在处理`deduct_right_consumption` API时进行并发安全的消耗扣减，针对特定身份档案 (`user_id`)。
        *   模块2暴露方式: 提供原子增减接口，参数包含 `user_id`, 权益名称, 数量。
        *   示例调用: `persistence.redis.decrby(userId, right_name, amount)` 或 `persistence.redis.incrby(userId, right_name, amount)` (模块2内部构建Key `user_cons:{userId}:<right_name>`)
        *   模块2应返回操作后的值，并允许模块4处理扣减结果。
    *   执行Lua脚本 (用于原子查询+扣减):
        *   目的: 支持模块4对特定身份档案 (`user_id`) 的消耗进行原子检查和扣减。
        *   模块2暴露方式: 提供执行Lua脚本的接口，模块4提供脚本、`user_id` (作为Key的一部分) 和参数。模块2负责将脚本发送到正确的Key (`user_cons:{userId}:...`) 所在的Redis节点执行。

API 调用总结: 模块4与模块2的交互方式（通过内部库/SDK调用封装的Redis操作）保持不变，但调用时传递的核心标识符从旧的单一`user_id`变为明确的`account_id`（用于账户管理）和用户身份档案的 `user_id`（用于身份档案管理、权限和权益操作）。

## 4. 数据交互流程与操作支持

模块2需要支持模块4以下关键数据交互流程和操作：

1.  用户注册:
    *   模块4调用模块2 PG API 创建 `user_accounts` 记录。
    *   模块4调用模块2 PG API 创建一个初始的 `user_identity_profiles` 记录（包含新生成的 `user_id`，关联新创建的 `account_id` 和默认 `role_id`）。
    *   模块4触发后台任务，该任务调用模块2 PG API 查询该 `user_id` 关联的 `role_id` 的权限配置，计算生效权限，然后调用模块2 Redis API (如 `hmset`, `set`) 初始化该 `user_id` 对应的 `user_perms:{user_id}` Hash 和 `user_cons:{user_id}:*` String Keys。
2.  为用户账户新增角色身份 (创建新的 `user_id` 实例):
    *   模块4调用模块2 PG API 查询指定 `account_id` 是否存在。
    *   模块4调用模块2 PG API 创建一个新的 `user_identity_profiles` 记录（包含新生成的 `user_id`，关联指定的 `account_id` 和新的 `role_id`）。
    *   模块4触发后台任务，该任务调用模块2 PG API 查询新 `user_id` 关联的 `role_id` 的权限配置，计算生效权限，然后调用模块2 Redis API 初始化该新 `user_id` 对应的 `user_perms:{user_id}` Hash 和 `user_cons:{user_id}:*` String Keys。
    *   明确为每个新增角色创建新 `user_id` 实例时，模块2需要支持的数据操作就是创建新的 `user_identity_profiles` 记录 (PG) 和初始化新的 `user_perms` / `user_cons` Redis Keys (Redis)。
3.  用户认证后身份档案选择与切换:
    *   认证阶段：OAuth2 服务（可能通过模块4 API）调用模块2 PG API 查询 `user_accounts` 进行凭证验证。
    *   获取身份档案列表：OAuth2 服务或客户端调用模块4 API，模块4调用模块2 PG API (`GET /v1/user-identity-profiles?account_id={accountId}`) 获取该账户下的所有 `user_identity_profiles` 列表（包含 `user_id`, `role_id`, `username` 等）。
    *   选择/切换：用户选择一个 `user_id`。后续业务服务请求都将携带此选定的 `user_id`。
4.  用户访问服务 (权限检查与消耗):
    *   业务服务接收到带有选定 `user_id` 的请求。
    *   业务服务调用模块4 API (`check_permission`, `deduct_right_consumption`)，传入请求中的 `user_id`。
    *   模块4接收到带 `user_id` 的调用后，直接调用模块2 Redis API (`hget`, `get`, `decrby`/`incrby`, `eval`)，传入该 `user_id` 和相应的权限/权益名称，模块2执行Redis操作并返回结果。
    *   确保用户权益 (`model:gpt4:calls` limit) 的计算和关联方式： 权益的配置 (`limit`, `resets_at`等) 存储在 `user_perms:{user_id}` Hash 中，严格关联到特定的身份档案 `user_id`。消耗计数存储在 `user_cons:{user_id}:<right_name>` String Key 中，也严格关联到该 `user_id`。模块4的权限计算后台任务确保这一点，模块2提供的Redis API确保读写操作是针对传入的 `user_id` 对应的 Key。

这些流程修订确保了联合开发文档完全反映用户中心服务在多角色处理（特别是引入 `user_account` 与 `user_identity_profile` 分离，每个profile拥有独立 `user_id`）方面的最新设计。

## 5. 文档对Cursor AI开发的适用性提升

本修订版已根据新的用户中心设计，对联合开发文档的关键部分进行了更新，以提供更准确、清晰的指导：

-   数据模型精确化: 详细描述了 `user_accounts` 和 `user_identity_profiles` 的新表结构，以及 `user_social_accounts`, `login_history` 关联到 `account_id` 的修订。明确废弃了 `user_roles` 表。
-   Redis 数据结构关联明确: 清楚阐述了 `user_perms:{user_id}` 和 `user_cons:{user_id}:<right_name>` 中的 `user_id` 现在代表用户身份档案，并说明了这些数据的来源（基于 PG 定义计算）和更新方式。
-   API 接口调整: 列出了模块2需要提供的新增/修订的 PostgreSQL API (针对新表) 和 Redis API (操作基于身份档案 `user_id` 的Keys)，并明确废弃了 `user_roles` 相关API。
-   数据交互流程说明: 概念性地描述了在注册、新增身份档案、选择/切换身份档案、权限检查/消耗等核心流程中，模块4如何与模块2的PG和Redis API进行交互，突出强调了 `account_id` 和身份档案 `user_id` 在不同操作中的使用场景。
-   权益关联一致性: 明确说明了用户身份档案的权益如何体现在 Redis 数据结构中 (`user_perms:{user_id}` 和 `user_cons:{user_id}:<right_name>`)，并严格关联到身份档案 `user_id`。

这些修订解决了先前版本未完全对齐最新用户中心设计的问题，为Cursor AI提供了基于最新模型的、清晰准确的持久化服务交互规范，指导其进行联合开发。