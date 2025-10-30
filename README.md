# 🚀 百度关键词分析器

智能挖掘百度搜索下拉词，发现长尾关键词和用户需求的专业工具。

## ✨ 功能特性

### 🎯 关键词分析
- **多变体生成**: 支持字母后缀、疑问词等多种变体类型
- **批量分析**: 一次性分析多个变体，提高效率
- **实时进度**: 可视化进度条，实时显示分析状态

### 📊 数据处理
- **智能去重**: 自动去除重复建议词，提升数据质量
- **统计概览**: 详细的数据统计和成功率分析
- **历史记录**: 保存分析历史，方便回顾和对比

### 📈 可视化展示
- **多视图模式**: 树形视图、表格视图、图表视图
- **交互式操作**: 一键复制、搜索过滤、数据导出
- **响应式设计**: 完美适配桌面和移动设备

### 💾 数据导出
- **多格式支持**: Excel、CSV、JSON 格式导出
- **完整数据**: 包含变体类型、关键词、排序等完整信息

## 🛠️ 技术栈

### 前端
- **Vue 3** + **TypeScript** - 现代化前端框架
- **Element Plus** - 企业级UI组件库
- **Pinia** - 状态管理
- **ECharts** - 数据可视化
- **Tailwind CSS** - 原子化CSS框架

### 后端
- **FastAPI** - 高性能Python API框架
- **SQLite** + **SQLAlchemy** - 数据存储
- **httpx** - 异步HTTP客户端
- **Pandas** - 数据处理

## 🚀 快速开始

### 方式一：一键启动（推荐）

```bash
# macOS/Linux
./start-simple.sh

# Windows
start.bat
```

### 方式二：手动启动

**启动后端:**
```bash
cd backend
python3 main.py
```

**启动前端:**
```bash
npm install  # 首次运行
npm run dev
```

### 服务地址
- 🌐 前端应用: http://localhost:3000
- 🔧 后端API: http://localhost:8000
- 📚 API文档: http://localhost:8000/docs

## 📖 使用说明

### 1. 基础分析
1. 输入目标关键词
2. 选择变体类型（建议选择2-3种）
3. 点击"开始分析"按钮
4. 等待分析完成

### 2. 查看结果
- **树形视图**: 按变体类型分组显示
- **表格视图**: 列表形式展示所有数据
- **图表视图**: 可视化分析结果

### 3. 数据操作
- **复制**: 点击关键词或"复制"按钮
- **搜索**: 使用搜索框过滤结果
- **导出**: 选择格式导出数据

### 4. 统计信息
- 📈 总建议词数量
- ✅ 成功/失败变体统计
- 🎯 分析成功率
- 🔄 去重数据统计

## 📁 项目结构

```
baidu-keyword-analyzer/
├── 📁 backend/              # 后端服务
│   ├── main.py              # FastAPI应用入口
│   ├── models.py            # 数据模型
│   ├── database.py          # 数据库配置
│   ├── config.py            # 配置文件
│   ├── requirements.txt     # Python依赖
│   └── 📁 services/         # 业务逻辑
│       ├── keyword_service.py   # 关键词分析服务
│       └── baidu_service.py     # 百度API服务
├── 📁 src/                  # 前端源码
│   ├── 📁 components/       # Vue组件
│   ├── 📁 stores/          # Pinia状态管理
│   ├── 📁 utils/           # 工具函数
│   └── 📁 views/           # 页面视图
├── 📁 logs/                # 运行日志
├── start-simple.sh         # 启动脚本 (macOS/Linux)
├── start.bat               # 启动脚本 (Windows)
└── package.json            # 前端依赖配置
```

## 🔧 故障排除

### 常见问题

**Q: 端口被占用怎么办？**
```bash
# 查看端口占用
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# 停止进程
kill -9 <PID>  # macOS/Linux
taskkill /F /PID <PID>  # Windows
```

**Q: 依赖安装失败？**
```bash
# 更新pip
python3 -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

**Q: 前端启动失败？**
```bash
# 清除缓存
rm -rf node_modules package-lock.json
npm install
```

### 日志查看
```bash
# 实时查看日志
tail -f logs/backend.log   # 后端日志
tail -f logs/frontend.log  # 前端日志
```

## 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情

---

⭐ 如果这个项目对你有帮助，请给个星标支持一下！