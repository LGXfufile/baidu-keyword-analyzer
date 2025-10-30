from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, create_tables
from models import (
    KeywordAnalysisRequest, 
    KeywordAnalysisResponse,
    SearchHistoryResponse,
    VariantTypesResponse,
    ProgressUpdate,
    ExportRequest
)
from services.keyword_service import KeywordService
from config import settings
import asyncio
import logging
import json
import pandas as pd
import io
from typing import List

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="百度关键词下拉词分析工具API"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储分析进度
analysis_progress = {}

@app.on_event("startup")
async def startup_event():
    """应用启动时创建数据库表"""
    await create_tables()
    logger.info("应用启动成功")

@app.get("/")
async def root():
    """健康检查接口"""
    return {
        "message": "百度关键词分析器API",
        "version": settings.VERSION,
        "status": "running"
    }

@app.get("/api/variant-types", response_model=VariantTypesResponse)
async def get_variant_types():
    """获取可用的关键词变体类型"""
    return VariantTypesResponse(variant_types=KeywordService.VARIANT_TYPES)

@app.post("/api/analyze", response_model=KeywordAnalysisResponse)
async def analyze_keyword(
    request: KeywordAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """分析关键词并获取下拉词"""
    try:
        # 验证变体类型
        invalid_types = [vt for vt in request.variant_types if vt not in KeywordService.VARIANT_TYPES]
        if invalid_types:
            raise HTTPException(status_code=400, detail=f"无效的变体类型: {invalid_types}")
        
        # 进度回调函数
        async def progress_callback(processed: int, total: int):
            session_id = analysis_progress.get('current_session')
            if session_id:
                analysis_progress[session_id] = {
                    'processed': processed,
                    'total': total,
                    'percentage': round((processed / total) * 100, 2)
                }
        
        # 执行分析
        result = await KeywordService.analyze_keywords(
            request.keyword,
            request.variant_types,
            db,
            progress_callback
        )
        
        # 保存当前会话ID到进度跟踪
        analysis_progress['current_session'] = result['session_id']
        
        return KeywordAnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"关键词分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.get("/api/progress/{session_id}")
async def get_analysis_progress(session_id: str):
    """获取分析进度"""
    if session_id in analysis_progress:
        progress = analysis_progress[session_id]
        return ProgressUpdate(
            session_id=session_id,
            **progress
        )
    else:
        return ProgressUpdate(
            session_id=session_id,
            processed=0,
            total=0,
            percentage=0.0
        )

@app.get("/api/history", response_model=List[SearchHistoryResponse])
async def get_search_history(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """获取搜索历史"""
    try:
        histories = await KeywordService.get_search_history(db, limit)
        return [SearchHistoryResponse(**h) for h in histories]
    except Exception as e:
        logger.error(f"获取搜索历史失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取历史失败: {str(e)}")

@app.get("/api/results/{session_id}")
async def get_session_results(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取特定会话的分析结果"""
    try:
        results = await KeywordService.get_session_results(session_id, db)
        return results
    except Exception as e:
        logger.error(f"获取会话结果失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取结果失败: {str(e)}")

@app.post("/api/export")
async def export_results(
    request: ExportRequest,
    db: AsyncSession = Depends(get_db)
):
    """导出分析结果"""
    try:
        results = await KeywordService.get_session_results(request.session_id, db)
        
        # 准备导出数据
        export_data = []
        for variant_type, variants in results['results'].items():
            for variant_keyword, suggestions in variants.items():
                for rank, suggestion in enumerate(suggestions, 1):
                    export_data.append({
                        '变体类型': KeywordService.VARIANT_TYPES.get(variant_type, variant_type),
                        '变体关键词': variant_keyword,
                        '下拉建议词': suggestion,
                        '排序': rank
                    })
        
        if not export_data:
            raise HTTPException(status_code=404, detail="没有找到数据")
        
        if request.format == 'excel':
            # 导出Excel
            df = pd.DataFrame(export_data)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='关键词分析结果')
            output.seek(0)
            
            return StreamingResponse(
                io.BytesIO(output.read()),
                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                headers={"Content-Disposition": f"attachment; filename=keywords_{request.session_id}.xlsx"}
            )
            
        elif request.format == 'csv':
            # 导出CSV
            df = pd.DataFrame(export_data)
            output = io.StringIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            
            return StreamingResponse(
                io.BytesIO(output.getvalue().encode('utf-8-sig')),
                media_type='text/csv',
                headers={"Content-Disposition": f"attachment; filename=keywords_{request.session_id}.csv"}
            )
            
        elif request.format == 'json':
            # 导出JSON
            json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
            
            return StreamingResponse(
                io.BytesIO(json_data.encode('utf-8')),
                media_type='application/json',
                headers={"Content-Disposition": f"attachment; filename=keywords_{request.session_id}.json"}
            )
        
        else:
            raise HTTPException(status_code=400, detail="不支持的导出格式")
            
    except Exception as e:
        logger.error(f"导出失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)