@echo off
REM MediaCMS PostgreSQL 数据库一键配置脚本
REM 使用方法：双击运行，按提示输入 postgres 密码

echo ========================================
echo MediaCMS PostgreSQL 数据库配置脚本
echo ========================================
echo.

REM 检查 psql 是否可用
where psql >nul 2>&1
if errorlevel 1 (
    echo [错误] 找不到 psql 命令
    echo.
    echo 请确保 PostgreSQL 已安装，并且 bin 目录已添加到 PATH
    echo PostgreSQL bin 目录通常在：
    echo   C:\Program Files\PostgreSQL\15\bin
    echo   或
    echo   C:\Program Files\PostgreSQL\17\bin
    echo.
    echo 或者使用完整路径运行：
    echo   "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres
    echo.
    pause
    exit /b 1
)

REM 提示输入 postgres 密码
set PGPASSWORD=
set /p PGPASSWORD="请输入 postgres 用户密码（安装 PostgreSQL 时设置的密码）: "

if "%PGPASSWORD%"=="" (
    echo [错误] 密码不能为空
    pause
    exit /b 1
)

REM 设置环境变量
set PGPASSWORD=%PGPASSWORD%

echo.
echo [检查] 正在检查 PostgreSQL 连接...
psql -U postgres -h localhost -c "SELECT version();" >nul 2>&1
if errorlevel 1 (
    echo [错误] 无法连接到 PostgreSQL 服务器
    echo.
    echo 可能的原因：
    echo 1. PostgreSQL 服务未启动
    echo    解决方法：打开 services.msc，启动 postgresql-x64-xx 服务
    echo.
    echo 2. 密码错误
    echo    请重新运行脚本并输入正确的密码
    echo.
    echo 3. psql 未添加到 PATH
    echo    解决方法：将 PostgreSQL bin 目录添加到系统 PATH
    echo.
    pause
    exit /b 1
)

echo [成功] PostgreSQL 连接正常
echo.

echo [创建] 正在创建数据库 mediacms...
psql -U postgres -h localhost -c "CREATE DATABASE mediacms;" 2>nul
if errorlevel 1 (
    echo [提示] 数据库 mediacms 可能已存在，跳过创建
) else (
    echo [成功] 数据库 mediacms 创建成功
)

echo.
echo [创建] 正在创建用户 mediacms...
psql -U postgres -h localhost -c "CREATE USER mediacms WITH PASSWORD 'mediacms';" 2>nul
if errorlevel 1 (
    echo [提示] 用户 mediacms 可能已存在，跳过创建
) else (
    echo [成功] 用户 mediacms 创建成功
)

echo.
echo [配置] 正在配置用户权限和设置...
psql -U postgres -h localhost -c "ALTER ROLE mediacms SET client_encoding TO 'utf8';" 2>nul
if errorlevel 1 (
    echo [警告] 设置 client_encoding 失败
)

psql -U postgres -h localhost -c "ALTER ROLE mediacms SET default_transaction_isolation TO 'read committed';" 2>nul
if errorlevel 1 (
    echo [警告] 设置 default_transaction_isolation 失败
)

psql -U postgres -h localhost -c "ALTER ROLE mediacms SET timezone TO 'UTC';" 2>nul
if errorlevel 1 (
    echo [警告] 设置 timezone 失败
)

echo.
echo [授权] 正在授予数据库权限...
psql -U postgres -h localhost -c "GRANT ALL PRIVILEGES ON DATABASE mediacms TO mediacms;" 2>nul
if errorlevel 1 (
    echo [错误] 授予权限失败
    pause
    exit /b 1
) else (
    echo [成功] 数据库权限授予成功
)

echo.
echo [授权] 正在授予 Schema 权限...
set PGPASSWORD=mediacms
psql -U mediacms -d mediacms -h localhost -c "GRANT ALL ON SCHEMA public TO mediacms;" 2>nul
psql -U mediacms -d mediacms -h localhost -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO mediacms;" 2>nul
psql -U mediacms -d mediacms -h localhost -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO mediacms;" 2>nul
if errorlevel 1 (
    echo [警告] Schema 权限设置可能失败，但基本功能应该可用
)

echo.
echo [验证] 正在测试数据库连接...
psql -U mediacms -d mediacms -h localhost -c "SELECT version();" >nul 2>&1
if errorlevel 1 (
    echo [错误] 无法使用 mediacms 用户连接到数据库
    echo.
    echo 请检查：
    echo 1. 用户密码是否正确
    echo 2. 权限是否授予成功
    echo 3. 数据库是否存在
    echo.
    pause
    exit /b 1
) else (
    echo [成功] 数据库连接测试通过！
)

echo.
echo ========================================
echo 数据库配置完成！
echo ========================================
echo.
echo 数据库信息：
echo   数据库名: mediacms
echo   用户名: mediacms
echo   密码: mediacms
echo   主机: localhost
echo   端口: 5432
echo.
echo 下一步：运行数据库迁移
echo   python manage.py migrate
echo.
pause

