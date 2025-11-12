-- MediaCMS PostgreSQL 数据库配置 SQL 脚本
-- 使用方法：
--   psql -U postgres -h localhost -f setup-database.sql
-- 或使用密码环境变量：
--   $env:PGPASSWORD='your_password'
--   psql -U postgres -h localhost -f setup-database.sql

-- 创建数据库（如果不存在）
SELECT 'CREATE DATABASE mediacms'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mediacms')\gexec

-- 创建用户（如果不存在）
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'mediacms') THEN
        CREATE USER mediacms WITH PASSWORD 'mediacms';
    END IF;
END
$$;

-- 设置用户编码和时区
ALTER ROLE mediacms SET client_encoding TO 'utf8';
ALTER ROLE mediacms SET default_transaction_isolation TO 'read committed';
ALTER ROLE mediacms SET timezone TO 'UTC';

-- 授予数据库权限
GRANT ALL PRIVILEGES ON DATABASE mediacms TO mediacms;

-- 连接到新数据库
\c mediacms

-- 授予 Schema 权限
GRANT ALL ON SCHEMA public TO mediacms;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO mediacms;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO mediacms;

-- 显示配置信息
SELECT '数据库配置完成！' AS status;
SELECT '数据库: mediacms' AS info;
SELECT '用户: mediacms' AS info;
SELECT '密码: mediacms' AS info;

