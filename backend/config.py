import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 应用配置
    APP_NAME = "百度关键词分析器"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # 数据库配置
    DATABASE_URL = "sqlite+aiosqlite:///./keywords.db"
    
    # 百度API配置
    BAIDU_SUGGEST_URL = "https://www.baidu.com/sugrec"
    
    # 请求配置
    REQUEST_TIMEOUT = 10
    REQUEST_DELAY_MIN = 1  # 最小延迟秒数
    REQUEST_DELAY_MAX = 3  # 最大延迟秒数
    MAX_RETRIES = 3
    
    # 跨域配置
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://*.vercel.app"
    ]

settings = Settings()