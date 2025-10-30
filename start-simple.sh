#!/bin/bash

# 简化版启动脚本
set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo -e "${GREEN}🎯 百度关键词分析器 - 快速启动${NC}"
echo "=========================================="

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 创建日志目录
mkdir -p "$PROJECT_ROOT/logs"

# 清理函数
cleanup() {
    echo -e "${YELLOW}正在停止服务...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

# 启动后端
echo -e "${BLUE}启动后端服务...${NC}"
cd "$PROJECT_ROOT/backend"
python3 main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}后端服务启动中 (PID: $BACKEND_PID)${NC}"

# 回到项目根目录
cd "$PROJECT_ROOT"

# 启动前端
echo -e "${BLUE}启动前端服务...${NC}"
npm run dev > logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}前端服务启动中 (PID: $FRONTEND_PID)${NC}"

# 等待服务启动
echo -e "${BLUE}等待服务启动...${NC}"
sleep 5

echo ""
echo "=========================================="
echo -e "${GREEN}🚀 服务启动完成${NC}"
echo "=========================================="
echo -e "${BLUE}后端服务:${NC} http://localhost:8000"
echo -e "${BLUE}API文档:${NC} http://localhost:8000/docs"
echo -e "${BLUE}前端服务:${NC} http://localhost:3000"
echo "=========================================="
echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
echo ""

# 自动打开浏览器
if command -v open &> /dev/null; then
    echo -e "${BLUE}3秒后自动打开浏览器...${NC}"
    sleep 3
    open http://localhost:3000 2>/dev/null || open http://localhost:3001 2>/dev/null || true
fi

# 保持脚本运行
while true; do
    sleep 1
done