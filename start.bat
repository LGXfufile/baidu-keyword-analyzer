@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM 百度关键词分析器 - Windows启动脚本
REM Author: Claude Code
REM Description: 启动前端和后端服务

title 百度关键词分析器 - 启动脚本

REM 颜色代码
set "RED=[31m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "NC=[0m"

REM 项目根目录
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

echo ===========================================
echo %GREEN%🎯 百度关键词分析器 - 启动脚本%NC%
echo ===========================================

REM 创建日志目录
if not exist "logs" (
    mkdir logs
    echo %BLUE%[INFO]%NC% 创建日志目录: logs
)

REM 检查Python
echo %BLUE%[INFO]%NC% 检查依赖...
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR]%NC% Python 未安装或未添加到PATH
    pause
    exit /b 1
)

REM 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR]%NC% Node.js 未安装或未添加到PATH
    pause
    exit /b 1
)

REM 检查npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR]%NC% npm 未安装或未添加到PATH
    pause
    exit /b 1
)

echo %GREEN%[SUCCESS]%NC% 依赖检查完成

REM 检查端口占用
echo %BLUE%[INFO]%NC% 检查端口占用...
netstat -ano | findstr :8000 >nul 2>&1
if not errorlevel 1 (
    echo %YELLOW%[WARNING]%NC% 端口 8000 已被占用，尝试停止相关进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
        taskkill /F /PID %%a >nul 2>&1
    )
)

netstat -ano | findstr :3000 >nul 2>&1
if not errorlevel 1 (
    echo %YELLOW%[WARNING]%NC% 端口 3000 已被占用，Vite会自动选择其他端口
)

REM 启动后端
echo %BLUE%[INFO]%NC% 启动后端服务...
cd /d "%PROJECT_ROOT%\backend"

REM 检查虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo %BLUE%[INFO]%NC% 激活虚拟环境...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo %BLUE%[INFO]%NC% 激活虚拟环境...
    call .venv\Scripts\activate.bat
) else (
    echo %YELLOW%[WARNING]%NC% 未找到虚拟环境，使用系统Python
)

REM 安装Python依赖
if exist "requirements.txt" (
    echo %BLUE%[INFO]%NC% 检查Python依赖...
    pip install -r requirements.txt >nul 2>&1
)

REM 启动后端服务
echo %BLUE%[INFO]%NC% 正在启动FastAPI服务器...
start "后端服务" /min cmd /c "python main.py > ..\logs\backend.log 2>&1"

REM 等待后端启动
echo %BLUE%[INFO]%NC% 等待后端服务启动...
set /a count=0
:wait_backend
curl -s http://localhost:8000/ >nul 2>&1
if not errorlevel 1 (
    echo %GREEN%[SUCCESS]%NC% 后端服务启动成功
    echo %GREEN%[SUCCESS]%NC% 后端地址: http://localhost:8000
    echo %GREEN%[SUCCESS]%NC% API文档: http://localhost:8000/docs
    goto backend_ready
)
set /a count+=1
if !count! geq 30 (
    echo %RED%[ERROR]%NC% 后端服务启动失败
    pause
    exit /b 1
)
timeout /t 1 /nobreak >nul
goto wait_backend

:backend_ready
cd /d "%PROJECT_ROOT%"

REM 启动前端
echo %BLUE%[INFO]%NC% 启动前端服务...

REM 安装前端依赖
if not exist "node_modules" (
    echo %BLUE%[INFO]%NC% 安装前端依赖...
    npm install
)

REM 启动前端服务
echo %BLUE%[INFO]%NC% 正在启动Vite开发服务器...
start "前端服务" /min cmd /c "npm run dev > logs\frontend.log 2>&1"

REM 等待前端启动
echo %BLUE%[INFO]%NC% 等待前端服务启动...
set /a count=0
:wait_frontend
curl -s http://localhost:3000/ >nul 2>&1
if not errorlevel 1 (
    echo %GREEN%[SUCCESS]%NC% 前端服务启动成功
    echo %GREEN%[SUCCESS]%NC% 前端地址: http://localhost:3000
    goto frontend_ready
)
curl -s http://localhost:3001/ >nul 2>&1
if not errorlevel 1 (
    echo %GREEN%[SUCCESS]%NC% 前端服务启动成功
    echo %GREEN%[SUCCESS]%NC% 前端地址: http://localhost:3001
    goto frontend_ready
)
set /a count+=1
if !count! geq 30 (
    echo %RED%[ERROR]%NC% 前端服务启动失败
    pause
    exit /b 1
)
timeout /t 1 /nobreak >nul
goto wait_frontend

:frontend_ready
REM 显示服务状态
echo.
echo ==========================================
echo %GREEN%🚀 百度关键词分析器 - 服务状态%NC%
echo ==========================================
echo %BLUE%后端服务:%NC% http://localhost:8000
echo %BLUE%API文档:%NC% http://localhost:8000/docs
echo %BLUE%前端服务:%NC% http://localhost:3000 或 http://localhost:3001
echo ==========================================
echo %YELLOW%提示:%NC%
echo • 关闭此窗口将停止所有服务
echo • 日志文件保存在 logs\ 目录
echo • 按任意键打开浏览器访问前端
echo ==========================================
echo.

REM 自动打开浏览器
timeout /t 3 /nobreak >nul
start http://localhost:3000 2>nul || start http://localhost:3001 2>nul

echo %GREEN%[SUCCESS]%NC% 服务启动完成！浏览器已自动打开
echo %BLUE%[INFO]%NC% 保持此窗口打开以维持服务运行
echo.
pause

REM 停止服务
echo %YELLOW%[WARNING]%NC% 正在停止服务...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
echo %GREEN%[SUCCESS]%NC% 服务已停止