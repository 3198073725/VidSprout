@echo off
chcp 65001 >nul
echo ===== 提交 README.md 文档 =====
echo.

REM 检查Git是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: Git 未安装
    echo 请先安装 Git 或运行 setup-git.bat 脚本
    pause
    exit /b 1
)

echo ✅ Git 已安装
echo.

REM 检查是否已经是Git仓库
if not exist .git (
    echo ⚠️  当前目录不是Git仓库，正在初始化...
    git init
    echo ✅ Git 仓库初始化完成
    echo.
)

REM 添加README.md文件
echo 📝 添加 README.md 文件到暂存区...
git add README.md
echo ✅ README.md 已添加到暂存区
echo.

REM 检查是否有更改
git diff --cached --quiet
if %errorlevel% equ 0 (
    echo ℹ️  README.md 没有更改，无需提交
    pause
    exit /b 0
)

REM 显示将要提交的更改
echo 📊 将要提交的更改:
git diff --cached --stat
echo.

REM 提交更改
echo 💾 提交 README.md 文档...
git commit -m "docs: 更新项目README文档

- 完善项目介绍和功能说明
- 添加中文本地化说明
- 更新技术栈和安装指南
- 添加使用说明和开发指南
- 完善联系方式和贡献指南"

if %errorlevel% equ 0 (
    echo ✅ README.md 提交成功！
) else (
    echo ❌ 提交失败
    pause
    exit /b 1
)

echo.
echo 📋 提交历史:
git log --oneline -5
echo.

echo 🎉 README.md 文档提交完成！
echo.
echo 💡 后续操作:
echo   - 如需推送到远程仓库: git push
echo   - 查看提交详情: git show
echo   - 查看文件状态: git status
echo.
pause
