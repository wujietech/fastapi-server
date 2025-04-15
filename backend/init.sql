-- 1、用户表 user
CREATE TABLE IF NOT EXISTS "user" (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_superuser BOOLEAN NOT NULL DEFAULT false,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "user" IS '用户表';
COMMENT ON COLUMN "user".id IS '用户ID';
COMMENT ON COLUMN "user".email IS '邮箱';
COMMENT ON COLUMN "user".is_active IS '是否激活';
COMMENT ON COLUMN "user".is_superuser IS '是否超级用户';
COMMENT ON COLUMN "user".full_name IS '全名';
COMMENT ON COLUMN "user".hashed_password IS '密码哈希';
COMMENT ON COLUMN "user".created_at IS '创建时间';
COMMENT ON COLUMN "user".updated_at IS '更新时间';

-- 2、商品表 item
CREATE TABLE IF NOT EXISTS item (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    owner_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_owner
        FOREIGN KEY (owner_id)
        REFERENCES "user"(id)
        ON DELETE CASCADE
);
COMMENT ON TABLE item IS '商品表';
COMMENT ON COLUMN item.id IS '商品ID';
COMMENT ON COLUMN item.title IS '标题';
COMMENT ON COLUMN item.description IS '描述';
COMMENT ON COLUMN item.owner_id IS '所有者ID';
COMMENT ON COLUMN item.created_at IS '创建时间';
COMMENT ON COLUMN item.updated_at IS '更新时间';

-- 3、分类表 category
CREATE TABLE IF NOT EXISTS category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN category.id IS '自增ID';
COMMENT ON COLUMN category.name IS '分类名';
COMMENT ON COLUMN category.description IS '分类描述';
COMMENT ON COLUMN category.created_at IS '创建时间';
COMMENT ON COLUMN category.updated_at IS '更新时间';

-- 创建自动更新 updated_at 的函数
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器
CREATE TRIGGER update_category_mod_time
    BEFORE UPDATE ON category
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- 插入初始分类数据
INSERT INTO category (name, description) 
VALUES 
    ('default', '默认'),
    ('search', '搜索'),
    ('crawl', '获取内容'),
    ('action', '动作执行')
ON CONFLICT (name) DO NOTHING;

-- 4、工作流表 workflow
CREATE TABLE IF NOT EXISTS workflow (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(100) NOT NULL,
    needLogin SMALLINT NOT NULL DEFAULT 0,
    params JSONB NOT NULL DEFAULT '{}',
    version INT NOT NULL DEFAULT 1,
    workflow JSONB NOT NULL DEFAULT '{}',
    icon VARCHAR(100) NOT NULL DEFAULT '',
    category INT NOT NULL DEFAULT 1,
    invalid SMALLINT NOT NULL DEFAULT 0,
    ratelimit INT NOT NULL DEFAULT 60,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_category
        FOREIGN KEY (category)
        REFERENCES category(id)
        ON DELETE RESTRICT
);

-- 创建触发器函数
CREATE OR REPLACE FUNCTION update_workflow_version_and_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    -- 检查 workflow 字段是否发生变化
    IF NEW.workflow IS DISTINCT FROM OLD.workflow THEN
        NEW.version = OLD.version + 1;
    END IF;
    -- 更新时间戳
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 创建触发器
CREATE TRIGGER workflow_version_update
    BEFORE UPDATE ON workflow
    FOR EACH ROW
    EXECUTE FUNCTION update_workflow_version_and_timestamp();

-- 添加注释
COMMENT ON TABLE workflow IS '工作流配置表';
COMMENT ON COLUMN workflow.id IS '自增ID';
COMMENT ON COLUMN workflow.name IS 'workflow 名';
COMMENT ON COLUMN workflow.description IS 'workflow 作用';
COMMENT ON COLUMN workflow.needLogin IS '是否需要登录';
COMMENT ON COLUMN workflow.params IS 'workflow 参数的描述';
COMMENT ON COLUMN workflow.version IS '版本号';
COMMENT ON COLUMN workflow.workflow IS 'workflow 配置';
COMMENT ON COLUMN workflow.icon IS '图标';
COMMENT ON COLUMN workflow.category IS '分类id';
COMMENT ON COLUMN workflow.invalid IS '是否有效，1=失效，0=有效';
COMMENT ON COLUMN workflow.ratelimit IS '执行间隔建议，单位：秒';
COMMENT ON COLUMN workflow.created_at IS '创建时间';
COMMENT ON COLUMN workflow.updated_at IS '更新时间';

-- 为 JSONB 字段创建索引（可选）
-- CREATE INDEX idx_workflow_params ON workflow USING GIN (params);
-- CREATE INDEX idx_workflow_workflow ON workflow USING GIN (workflow);

-- 5、工作流执行日志表 workflow_log
CREATE TABLE IF NOT EXISTS workflow_log (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL,
    workflow_version INTEGER NOT NULL,
    params VARCHAR(100) NOT NULL,
    result TEXT NOT NULL,
    status SMALLINT NOT NULL DEFAULT 0,
    retry SMALLINT NOT NULL DEFAULT 0,
    reason SMALLINT,
    reason_text VARCHAR(100),
    client_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_workflow
        FOREIGN KEY (workflow_id)
        REFERENCES workflow(id)
        ON DELETE RESTRICT
);

-- 添加注释
COMMENT ON TABLE workflow_log IS '工作流执行日志表';
COMMENT ON COLUMN workflow_log.id IS '自增ID';
COMMENT ON COLUMN workflow_log.workflow_id IS '工作流ID';
COMMENT ON COLUMN workflow_log.workflow_version IS '执行时的工作流版本号';
COMMENT ON COLUMN workflow_log.params IS '工作流参数';
COMMENT ON COLUMN workflow_log.result IS '工作流执行结果';
COMMENT ON COLUMN workflow_log.status IS '执行状态，0=成功，1=失败';
COMMENT ON COLUMN workflow_log.retry IS '是否重试，0=否，1=是';
COMMENT ON COLUMN workflow_log.reason IS '失败原因：1=用户拒绝登录，2=用户未处理登录(超时)，3=工作流报错，4=触发风控';
COMMENT ON COLUMN workflow_log.reason_text IS '失败原因文字描述';
COMMENT ON COLUMN workflow_log.client_time IS '客户端执行时间';
COMMENT ON COLUMN workflow_log.created_at IS '创建时间';

-- 创建触发器
CREATE TRIGGER update_log_mod_time
    BEFORE UPDATE ON workflow_log
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
    
-- 创建索引（建议）
-- CREATE INDEX idx_workflow_log_wid ON workflow_log(wid);
-- CREATE INDEX idx_workflow_log_status ON workflow_log(status);
-- CREATE INDEX idx_workflow_log_created_at ON workflow_log(created_at);