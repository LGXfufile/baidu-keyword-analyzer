#!/bin/bash

# 百度关键词分析器 - 一键启动脚本
# Author: Claude Code
# Description: 启动前端和后端服务

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 清理函数
cleanup() {
    log_warning "正在停止服务..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        log_info "后端服务已停止"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        log_info "前端服务已停止"
    fi
    exit 0
}

# 设置信号处理
trap cleanup SIGINT SIGTERM

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装，请先安装 Python3"
        exit 1
    fi
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js 未安装，请先安装 Node.js"
        exit 1
    fi
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        log_error "npm 未安装，请先安装 npm"
        exit 1
    fi
    
    log_success "依赖检查完成"
}

# 检查端口是否被占用
check_port() {
    local port=$1
    if command -v lsof &> /dev/null; then
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            log_warning "端口 $port 已被占用"
            return 1
        fi
    else
        # 如果没有lsof，使用netstat
        if netstat -tuln 2>/dev/null | grep -q ":$port "; then
            log_warning "端口 $port 已被占用"
            return 1
        fi
    fi
    return 0
}

# 启动后端
start_backend() {
    log_info "启动后端服务..."
    
    cd "$PROJECT_ROOT/backend"
    
    # 检查后端端口
    if ! check_port 8000; then
        log_warning "尝试停止占用端口 8000 的进程..."
        if command -v lsof &> /dev/null; then
            lsof -ti:8000 | xargs kill -9 2>/dev/null || true
        fi
        sleep 2
    fi
    
    # 检查虚拟环境是否存在
    if [ -d "venv" ]; then
        log_info "激活虚拟环境..."
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        log_info "激活虚拟环境..."
        source .venv/bin/activate
    else
        log_warning "未找到虚拟环境，使用系统Python"
    fi
    
    # 安装依赖（如果需要）
    if [ -f "requirements.txt" ]; then
        log_info "检查Python依赖..."
        pip install -r requirements.txt > /dev/null 2>&1
    fi
    
    # 启动后端
    log_info "正在启动FastAPI服务器..."
    python3 main.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    
    # 等待后端启动
    log_info "等待后端服务启动..."
    for i in {1..30}; do
        if command -v curl &> /dev/null; then
            if curl -s http://localhost:8000/ >/dev/null 2>&1; then
                log_success "后端服务启动成功 (PID: $BACKEND_PID)"
                log_success "后端地址: http://localhost:8000"
                log_success "API文档: http://localhost:8000/docs"
                break
            fi
        else
            # 如果没有curl，等待足够时间后假定启动成功
            if [ $i -eq 10 ]; then
                log_success "后端服务启动成功 (PID: $BACKEND_PID)"
                log_success "后端地址: http://localhost:8000"
                log_success "API文档: http://localhost:8000/docs"
                break
            fi
        fi
        if [ $i -eq 30 ]; then
            log_error "后端服务启动失败"
            cleanup
            exit 1
        fi
        sleep 1
    done
    
    cd "$PROJECT_ROOT"
}

# 启动前端
start_frontend() {
    log_info "启动前端服务..."
    
    cd "$PROJECT_ROOT"
    
    # 检查前端端口
    if ! check_port 3000; then
        log_warning "端口 3000 已被占用，Vite会自动选择其他端口"
    fi
    
    # 安装依赖（如果需要）
    if [ ! -d "node_modules" ]; then
        log_info "安装前端依赖..."
        npm install
    fi
    
    # 启动前端
    log_info "正在启动Vite开发服务器..."
    npm run dev > logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    # 等待前端启动
    log_info "等待前端服务启动..."
    for i in {1..30}; do
        if command -v curl &> /dev/null; then
            if curl -s http://localhost:3000/ >/dev/null 2>&1; then
                log_success "前端服务启动成功 (PID: $FRONTEND_PID)"
                log_success "前端地址: http://localhost:3000"
                break
            elif curl -s http://localhost:3001/ >/dev/null 2>&1; then
                log_success "前端服务启动成功 (PID: $FRONTEND_PID)"
                log_success "前端地址: http://localhost:3001"
                break
            fi
        else
            # 如果没有curl，等待足够时间后假定启动成功
            if [ $i -eq 15 ]; then
                log_success "前端服务启动成功 (PID: $FRONTEND_PID)"
                log_success "前端地址: http://localhost:3000"
                break
            fi
        fi
        if [ $i -eq 30 ]; then
            log_error "前端服务启动失败"
            cleanup
            exit 1
        fi
        sleep 1
    done
}

# 创建日志目录
create_log_dir() {
    if [ ! -d "$PROJECT_ROOT/logs" ]; then
        mkdir -p "$PROJECT_ROOT/logs"
        log_info "创建日志目录: $PROJECT_ROOT/logs"
    fi
}

# 显示服务状态
show_status() {
    echo
    echo "=========================================="
    echo -e "${GREEN}🚀 百度关键词分析器 - 服务状态${NC}"
    echo "=========================================="
    echo -e "${BLUE}后端服务:${NC} http://localhost:8000"
    echo -e "${BLUE}API文档:${NC} http://localhost:8000/docs"
    echo -e "${BLUE}前端服务:${NC} http://localhost:3000 或 http://localhost:3001"
    echo "=========================================="
    echo -e "${YELLOW}提示:${NC}"
    echo "• 按 Ctrl+C 停止所有服务"
    echo "• 日志文件保存在 logs/ 目录"
    echo "• 如需查看实时日志: tail -f logs/backend.log 或 logs/frontend.log"
    echo "=========================================="
    echo
}

# 主函数
main() {
    clear
    echo "=========================================="
    echo -e "${GREEN}🎯 百度关键词分析器 - 启动脚本${NC}"
    echo "=========================================="
    
    # 检查依赖
    check_dependencies
    
    # 创建日志目录
    create_log_dir
    
    # 启动服务
    start_backend
    start_frontend
    
    # 显示状态
    show_status
    
    # 自动打开浏览器（可选）
    if command -v open &> /dev/null; then
        log_info "3秒后自动打开浏览器..."
        sleep 3
        open http://localhost:3000 2>/dev/null || open http://localhost:3001 2>/dev/null || true
    fi
    
    # 保持脚本运行
    log_info "服务正在运行中，按 Ctrl+C 停止..."
    while true; do
        sleep 1
    done
}

# 运行主函数
main "$@"