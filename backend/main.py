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
from services.business_analyzer import BusinessAnalyzer
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
        
        # 生成唯一会话ID
        import uuid
        session_id = str(uuid.uuid4())
        
        # 初始化进度跟踪
        analysis_progress[session_id] = {
            'processed': 0,
            'total': 0,
            'percentage': 0.0,
            'status': 'running',
            'error': None
        }
        
        # 进度回调函数
        async def progress_callback(processed: int, total: int):
            analysis_progress[session_id].update({
                'processed': processed,
                'total': total,
                'percentage': round((processed / total) * 100, 2) if total > 0 else 0,
                'status': 'running'
            })
        
        # 执行分析
        try:
            result = await KeywordService.analyze_keywords(
                request.keyword,
                request.variant_types,
                db,
                progress_callback,
                session_id  # 传递session_id确保一致性
            )
            
            # session_id已经在result中了
            
            # 标记完成
            analysis_progress[session_id].update({
                'status': 'completed',
                'percentage': 100.0
            })
            
            return KeywordAnalysisResponse(**result)
            
        except Exception as e:
            # 标记错误
            analysis_progress[session_id].update({
                'status': 'error',
                'error': str(e)
            })
            logger.error(f"关键词分析失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")
        
    except Exception as e:
        logger.error(f"关键词分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.get("/api/progress/{session_id}")
async def get_analysis_progress(session_id: str):
    """获取分析进度"""
    if session_id in analysis_progress:
        progress = analysis_progress[session_id]
        return {
            'session_id': session_id,
            'processed': progress.get('processed', 0),
            'total': progress.get('total', 0), 
            'percentage': progress.get('percentage', 0.0),
            'status': progress.get('status', 'unknown'),
            'error': progress.get('error')
        }
    else:
        return {
            'session_id': session_id,
            'processed': 0,
            'total': 0,
            'percentage': 0.0,
            'status': 'not_found',
            'error': '会话不存在'
        }

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

@app.get("/api/business-analysis/{session_id}")
async def get_business_analysis(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取商业价值分析结果"""
    try:
        results = await KeywordService.get_session_results(session_id, db)
        
        # 如果结果中没有商业分析，则重新生成
        if 'business_analysis' not in results:
            # 重新分析并添加商业价值
            results = KeywordService._add_business_analysis(results)
        
        return {
            'session_id': session_id,
            'business_analysis': results.get('business_analysis', {}),
            'summary': results.get('summary', {})
        }
    except Exception as e:
        logger.error(f"获取商业分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"商业分析失败: {str(e)}")

@app.post("/api/analyze-keyword")
async def analyze_single_keyword(request: dict):
    """分析单个关键词的商业价值"""
    try:
        keyword = request.get('keyword', '')
        if not keyword:
            raise HTTPException(status_code=400, detail="关键词不能为空")
        
        metrics = BusinessAnalyzer.analyze_keyword(keyword)
        
        return {
            'keyword': keyword,
            'commercial_score': metrics.commercial_score,
            'intent_type': metrics.intent_type,
            'competition_level': metrics.competition_level,
            'search_volume_estimate': metrics.search_volume_estimate,
            'difficulty_score': metrics.difficulty_score,
            'opportunity_score': metrics.opportunity_score
        }
    except Exception as e:
        logger.error(f"单关键词分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.post("/api/blue-ocean-discovery")
async def discover_blue_ocean_keywords(request: dict):
    """发现蓝海关键词"""
    try:
        keyword = request.get('keyword', '')
        limit = request.get('limit', 10)
        
        if not keyword:
            raise HTTPException(status_code=400, detail="关键词不能为空")
        
        blue_oceans = await BusinessAnalyzer.discover_blue_ocean_keywords(keyword, limit)
        
        return {
            'keyword': keyword,
            'blue_ocean_count': len(blue_oceans),
            'blue_ocean_keywords': [
                {
                    'keyword': bo.keyword,
                    'opportunity_score': bo.opportunity_score,
                    'search_volume': bo.search_volume,
                    'competition_companies': bo.competition_companies,
                    'competition_level': bo.competition_level,
                    'sem_price': bo.sem_price,
                    'longtail_count': bo.longtail_count,
                    'platforms': bo.platforms,
                    'reasons': bo.reasons
                }
                for bo in blue_oceans
            ]
        }
    except Exception as e:
        logger.error(f"蓝海词发现失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"发现失败: {str(e)}")

@app.post("/api/analyze-with-real-data")
async def analyze_keyword_with_real_data(request: dict):
    """使用5118真实数据分析关键词"""
    try:
        keyword = request.get('keyword', '')
        enable_5118 = request.get('enable_5118', True)
        
        if not keyword:
            raise HTTPException(status_code=400, detail="关键词不能为空")
        
        metrics = await BusinessAnalyzer.analyze_with_real_data(keyword, enable_5118)
        
        return {
            'keyword': keyword,
            'commercial_score': metrics.commercial_score,
            'intent_type': metrics.intent_type,
            'competition_level': metrics.competition_level,
            'search_volume_estimate': metrics.search_volume_estimate,
            'difficulty_score': metrics.difficulty_score,
            'opportunity_score': metrics.opportunity_score,
            'is_blue_ocean': metrics.is_blue_ocean,
            'real_data_available': metrics.real_data_available
        }
    except Exception as e:
        logger.error(f"真实数据分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.get("/api/business-insights/{session_id}")
async def get_business_insights(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取智能商业洞察和分层机会"""
    try:
        results = await KeywordService.get_session_results(session_id, db)
        
        # 获取所有建议词
        all_suggestions = []
        for variant_type, variants in results['results'].items():
            for variant_keyword, suggestions in variants.items():
                all_suggestions.extend(suggestions)
        
        if not all_suggestions:
            return {
                'session_id': session_id,
                'business_insights': {
                    'total_opportunities': 0,
                    'blue_ocean_count': 0,
                    'high_value_count': 0,
                    'avg_commercial_score': 0,
                    'total_search_volume': 0,
                    'categories': {},
                    'recommended_focus': [],
                    'insights': ['⚠️ 未找到有效的建议词数据']
                },
                'opportunities_by_tier': {},
                'recommendations': [],
                'summary_stats': {
                    'total_opportunities': 0,
                    'blue_ocean_count': 0,
                    'high_value_count': 0,
                    'avg_commercial_score': 0,
                    'total_search_volume': 0,
                    'total_count': 0,
                    'unique_count': 0,
                    'duplicate_removed': 0
                },
                'insights_messages': ['⚠️ 未找到有效的建议词数据，请重新进行关键词分析']
            }
        
        # 分析建议词列表 - 强制使用5118真实数据
        try:
            analysis = await BusinessAnalyzer.analyze_suggestion_list_with_real_data(all_suggestions, enable_5118=True)
        except Exception as e:
            logger.error(f"5118数据分析失败: {str(e)}")
            # 优雅降级，但明确标明是估算数据
            analysis = BusinessAnalyzer.analyze_suggestion_list(all_suggestions)
            analysis['data_source_warning'] = '⚠️ 5118真实数据获取失败，已降级为估算模式'
        
        # 生成商业洞察
        insights = BusinessAnalyzer.generate_business_insights(analysis['top_opportunities'])
        
        # 添加去重洞察信息
        duplicate_removed = analysis.get('duplicate_removed', 0)
        if duplicate_removed > 0:
            insights['insights'].insert(0, f"🧹 智能去重处理：从 {analysis.get('total_count', 0)} 个原始建议中去除 {duplicate_removed} 个重复项，保留 {analysis.get('unique_count', 0)} 个有效关键词")
        
        # 添加数据源警告（如果有）
        if 'data_source_warning' in analysis:
            insights['insights'].insert(0, analysis['data_source_warning'])
        
        return {
            'session_id': session_id,
            'business_insights': insights,
            'opportunities_by_tier': insights['categories'],
            'recommendations': insights['recommended_focus'],
            'summary_stats': {
                'total_opportunities': insights['total_opportunities'],
                'blue_ocean_count': insights['blue_ocean_count'],
                'high_value_count': insights['high_value_count'],
                'avg_commercial_score': insights['avg_commercial_score'],
                'total_search_volume': insights['total_search_volume'],
                'total_count': analysis.get('total_count', 0),
                'unique_count': analysis.get('unique_count', 0),
                'duplicate_removed': analysis.get('duplicate_removed', 0)
            },
            'insights_messages': insights['insights']
        }
    except Exception as e:
        logger.error(f"商业洞察分析失败: {str(e)}")
        error_message = f"商业洞察分析失败: {str(e)}"
        
        # 返回错误状态而不是抛出异常
        return {
            'session_id': session_id,
            'business_insights': {
                'total_opportunities': 0,
                'blue_ocean_count': 0,
                'high_value_count': 0,
                'avg_commercial_score': 0,
                'total_search_volume': 0,
                'categories': {},
                'recommended_focus': [],
                'insights': [f'❌ {error_message}']
            },
            'opportunities_by_tier': {},
            'recommendations': [],
            'summary_stats': {
                'total_opportunities': 0,
                'blue_ocean_count': 0,
                'high_value_count': 0,
                'avg_commercial_score': 0,
                'total_search_volume': 0,
                'total_count': 0,
                'unique_count': 0,
                'duplicate_removed': 0
            },
            'insights_messages': [
                f'❌ {error_message}',
                '🔧 请检查网络连接和API配置后重试',
                '💡 如果问题持续，请联系技术支持'
            ]
        }

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