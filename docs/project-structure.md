backend/
├── main.py              # FastAPI 主应用
├── models.py            # 数据模型
├── services/
│   ├── __init__.py
│   ├── baidu_service.py # 百度API调用服务
│   └── keyword_service.py # 关键词处理服务
├── database.py          # 数据库配置
├── requirements.txt     # Python依赖
└── config.py           # 配置文件

frontend/
├── src/
│   ├── components/     # Vue组件
│   ├── views/         # 页面视图
│   ├── stores/        # Pinia状态管理
│   ├── utils/         # 工具函数
│   └── main.ts        # 入口文件
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── index.html

docs/
├── api.md             # API文档
└── deployment.md      # 部署说明