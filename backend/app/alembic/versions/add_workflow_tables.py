"""add workflow related tables

Revision ID: add_workflow_tables
Revises: d98dd8ec85a3
Create Date: 2024-04-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_workflow_tables'
down_revision = 'd98dd8ec85a3'
branch_labels = None
depends_on = None


def upgrade():
    # 设置时区为 Asia/Shanghai
    op.execute("SET TIME ZONE 'Asia/Shanghai';")
    
    # 创建 category 表
    op.create_table(
        'category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('description', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai'")),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai'")),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # 创建 workflow 表
    op.create_table(
        'workflow',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('description', sa.String(length=100), nullable=False),
        sa.Column('needLogin', sa.SmallInteger(), nullable=False, server_default=sa.text('0')),
        sa.Column('params', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('version', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('workflow', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('icon', sa.String(length=100), nullable=False, server_default=''),
        sa.Column('category_id', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('invalid', sa.SmallInteger(), nullable=False, server_default=sa.text('0')),
        sa.Column('ratelimit', sa.Integer(), nullable=False, server_default=sa.text('60')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai'")),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai'")),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # 创建 workflow_log 表
    op.create_table(
        'workflowlog',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('workflow_id', sa.Integer(), nullable=False),
        sa.Column('workflow_version', sa.Integer(), nullable=False),
        sa.Column('params', sa.String(length=100), nullable=False),
        sa.Column('result', sa.Text(), nullable=False),
        sa.Column('status', sa.SmallInteger(), nullable=False, server_default=sa.text('0')),
        sa.Column('retry', sa.SmallInteger(), nullable=False, server_default=sa.text('0')),
        sa.Column('reason', sa.SmallInteger(), nullable=True),
        sa.Column('reason_text', sa.String(length=100), nullable=True),
        sa.Column('client_time', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai'")),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai'")),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建更新时间戳的函数
    op.execute("""
    CREATE OR REPLACE FUNCTION update_modified_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai';
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """)

    # 为每个表创建更新时间戳的触发器
    for table in ['category', 'workflow', 'workflowlog']:
        op.execute(f"""
        CREATE TRIGGER update_{table}_mod_time
            BEFORE UPDATE ON {table}
            FOR EACH ROW
            EXECUTE FUNCTION update_modified_column();
        """)

    # 创建 workflow 版本更新触发器
    op.execute("""
    CREATE OR REPLACE FUNCTION update_workflow_version_and_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.workflow IS DISTINCT FROM OLD.workflow THEN
            NEW.version = OLD.version + 1;
        END IF;
        NEW.updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Shanghai';
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER workflow_version_update
        BEFORE UPDATE ON workflow
        FOR EACH ROW
        EXECUTE FUNCTION update_workflow_version_and_timestamp();
    """)

    # 插入初始分类数据
    op.execute("""
    INSERT INTO category (name, description) 
    VALUES 
        ('default', '默认'),
        ('search', '搜索'),
        ('crawl', '获取内容'),
        ('action', '动作执行')
    ON CONFLICT (name) DO NOTHING;
    """)


def downgrade():
    # 删除触发器
    for table in ['category', 'workflow', 'workflowlog']:
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_mod_time ON {table}")
    
    op.execute("DROP TRIGGER IF EXISTS workflow_version_update ON workflow")

    # 删除函数
    op.execute("DROP FUNCTION IF EXISTS update_modified_column()")
    op.execute("DROP FUNCTION IF EXISTS update_workflow_version_and_timestamp()")

    # 删除表
    op.drop_table('workflowlog')
    op.drop_table('workflow')
    op.drop_table('category') 