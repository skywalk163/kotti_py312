@echo off
echo ========================================
echo AI交流社区前端 - 启动脚本
echo ========================================
echo.

echo [1/3] 检查Node.js环境...
node --version
if errorlevel 1 (
    echo 错误: 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖...
if not exist "node_modules" (
    echo 首次运行，正在安装依赖...
    call npm install
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 依赖已安装
)

echo.
echo [3/3] 启动开发服务器...
echo.
echo ========================================
echo 访问地址: http://localhost:3000
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

call npm run dev

pause
