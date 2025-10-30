# 百度关键词下拉词分析器

🔍 智能挖掘百度搜索下拉词，发现长尾关键词和用户需求

## 功能特性

- 🚀 **智能变体生成** - 自动生成 a-z 后缀、疑问词等变体
- 📊 **数据可视化** - 词云图、趋势分析、分类统计
- 💾 **多格式导出** - 支持 Excel、CSV、JSON 格式
- 🎨 **现代化界面** - Vue3 + Tailwind CSS，支持深色模式
- ⚡ **高性能采集** - 异步并发，智能反爬策略

## 技术栈

### 前端
- Vue 3 + TypeScript + Vite
- Tailwind CSS + Element Plus
- ECharts 数据可视化

### 后端  
- FastAPI + Python 3.9+
- SQLite 数据存储
- 异步HTTP请求处理

## 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 部署

项目支持 Vercel 一键部署，包含完整的 CI/CD 流程。

## 许可证

MIT License