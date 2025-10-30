from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime
from config import settings

# 异步数据库引擎
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

# 异步会话
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class KeywordResult(Base):
    __tablename__ = "keyword_results"
    
    id = Column(Integer, primary_key=True, index=True)
    original_keyword = Column(String(255), index=True)  # 原始关键词
    variant_keyword = Column(String(255), index=True)   # 变体关键词 
    suggestion = Column(String(500))                     # 下拉建议词
    suggestion_rank = Column(Integer)                    # 建议词排序
    variant_type = Column(String(50))                    # 变体类型(alpha, question, etc)
    created_at = Column(DateTime, default=datetime.utcnow)
    search_volume = Column(Float, nullable=True)         # 搜索量(预留)
    
class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    original_keyword = Column(String(255))
    variant_types = Column(Text)  # JSON字符串存储选择的变体类型
    total_suggestions = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="completed")  # pending, running, completed, failed

# 异步数据库依赖
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# 创建表
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)