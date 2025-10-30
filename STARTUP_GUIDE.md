# 🚀 启动脚本使用指南

## 📋 概述

为了简化开发流程，项目提供了两个自动化启动脚本：
- `start.sh` - macOS/Linux 启动脚本
- `start.bat` - Windows 启动脚本

## 🎯 功能特性

### ✅ 自动化启动
- 一键启动前端和后端服务
- 自动检查和安装依赖
- 智能端口检测和管理
- 自动打开浏览器

### 🔍 智能检测
- 检查系统依赖（Python3, Node.js, npm）
- 检测端口占用情况
- 虚拟环境自动激活
- 服务启动状态监控

### 📝 日志管理
- 自动创建 `logs/` 目录
- 分离前后端日志文件
- 实时日志记录

## 📖 使用方法

### macOS/Linux 用户

```bash
# 方法1: 直接执行
./start.sh

# 方法2: 通过bash执行
bash start.sh
```

### Windows 用户

```cmd
# 方法1: 双击运行
双击 start.bat 文件

# 方法2: 命令行执行
start.bat
```

## 🌐 服务地址

启动成功后可以访问：

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端应用 | http://localhost:3000 | 主要访问地址 |
| 前端应用 | http://localhost:3001 | 端口冲突时的备用地址 |
| 后端API | http://localhost:8000 | FastAPI 服务 |
| API文档 | http://localhost:8000/docs | Swagger 文档 |

## 🛠️ 故障排除

### 端口占用问题
- 脚本会自动检测并尝试释放被占用的端口
- 如果仍有问题，手动停止占用进程：
  ```bash
  # macOS/Linux
  lsof -ti:8000 | xargs kill -9
  lsof -ti:3000 | xargs kill -9
  
  # Windows
  netstat -ano | findstr :8000
  taskkill /F /PID <PID>
  ```

### 依赖问题
脚本会自动检查以下依赖：
- Python 3.7+
- Node.js 16+
- npm 或 yarn

如果缺少依赖，请先安装：
```bash
# 安装 Python (macOS)
brew install python

# 安装 Node.js (macOS)
brew install node

# 安装 Python (Ubuntu)
sudo apt install python3 python3-pip

# 安装 Node.js (Ubuntu)
sudo apt install nodejs npm
```

### 虚拟环境
脚本会自动检测以下虚拟环境：
- `backend/venv/`
- `backend/.venv/`

如需创建虚拟环境：
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
```

## 📋 日志查看

### 实时日志监控
```bash
# 查看后端日志
tail -f logs/backend.log

# 查看前端日志
tail -f logs/frontend.log

# 同时查看两个日志
tail -f logs/*.log
```

### 日志文件位置
- 后端日志：`logs/backend.log`
- 前端日志：`logs/frontend.log`

## ⚡ 高级用法

### 自定义端口
如需修改默认端口，编辑相应配置文件：

**后端端口** (backend/main.py):
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # 修改此处
```

**前端端口** (vite.config.ts):
```typescript
export default defineConfig({
  server: {
    port: 3000,  // 修改此处
    host: true
  }
})
```

### 后台运行
如需后台运行服务：
```bash
# macOS/Linux
nohup ./start.sh > /dev/null 2>&1 &

# 停止后台服务
pkill -f "python.*main.py"
pkill -f "npm.*run.*dev"
```

## 🔄 停止服务

### 正常停止
- **macOS/Linux**: 在终端按 `Ctrl + C`
- **Windows**: 关闭命令提示符窗口

### 强制停止
```bash
# macOS/Linux
pkill -f python
pkill -f node

# Windows
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
```

## 🔧 脚本自定义

### 修改启动选项
可以编辑脚本来添加自定义功能：
- 修改日志级别
- 添加环境变量
- 自定义启动参数
- 添加健康检查

### 添加新服务
如需添加其他服务（如数据库），可以参考脚本结构添加相应的启动逻辑。

## 💡 提示

1. **首次使用**：脚本会自动安装依赖，可能需要较长时间
2. **网络问题**：如果依赖安装失败，请检查网络连接
3. **权限问题**：macOS/Linux 用户可能需要 `chmod +x start.sh`
4. **浏览器**：脚本会自动打开默认浏览器访问前端
5. **开发模式**：启动的是开发环境，具有热重载功能

---

*如有问题，请查看日志文件或联系开发团队。*