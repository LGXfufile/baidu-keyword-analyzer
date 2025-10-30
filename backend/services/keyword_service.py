from typing import List, Dict, Set
import string
import asyncio
from services.baidu_service import BaiduSuggestService
from database import KeywordResult, SearchHistory, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
import uuid
from datetime import datetime

class KeywordService:
    
    VARIANT_TYPES = {
        'alpha': '字母后缀 (a-z)',
        'alpha_space': '字母后缀带空格 ( a- z)',  
        'question_how': '疑问词-怎么 (怎么a-z)',
        'question_what': '疑问词-什么 (什么a-z)',
        'question_can': '疑问词-可以 (可以a-z)',
        'numbers': '数字后缀 (1-9)',
        'common_suffix': '常用后缀'
    }
    
    @staticmethod
    def generate_variants(base_keyword: str, variant_types: List[str]) -> Dict[str, List[str]]:
        """生成关键词变体"""
        variants = {}
        
        for variant_type in variant_types:
            if variant_type == 'alpha':
                variants[variant_type] = [f"{base_keyword}{letter}" for letter in string.ascii_lowercase]
                
            elif variant_type == 'alpha_space':
                variants[variant_type] = [f"{base_keyword} {letter}" for letter in string.ascii_lowercase]
                
            elif variant_type == 'question_how':
                variants[variant_type] = [f"{base_keyword}怎么{letter}" for letter in string.ascii_lowercase]
                
            elif variant_type == 'question_what':
                variants[variant_type] = [f"{base_keyword}什么{letter}" for letter in string.ascii_lowercase]
                
            elif variant_type == 'question_can':
                variants[variant_type] = [f"{base_keyword}可以{letter}" for letter in string.ascii_lowercase]
                
            elif variant_type == 'numbers':
                variants[variant_type] = [f"{base_keyword}{num}" for num in range(1, 10)]
                
            elif variant_type == 'common_suffix':
                common_suffixes = [
                    '是什么', '怎么用', '怎么做', '多少钱', '哪个好',
                    '教程', '方法', '技巧', '攻略', '推荐',
                    '价格', '评测', '对比', '排行榜', '品牌'
                ]
                variants[variant_type] = [f"{base_keyword}{suffix}" for suffix in common_suffixes]
        
        return variants
    
    @staticmethod
    async def analyze_keywords(
        base_keyword: str, 
        variant_types: List[str],
        db: AsyncSession,
        progress_callback=None
    ) -> Dict:
        """分析关键词并获取下拉词"""
        
        # 生成会话ID
        session_id = str(uuid.uuid4())
        
        # 生成变体
        variants = KeywordService.generate_variants(base_keyword, variant_types)
        
        # 统计总数
        total_variants = sum(len(variant_list) for variant_list in variants.values())
        
        # 创建搜索历史记录
        search_history = SearchHistory(
            session_id=session_id,
            original_keyword=base_keyword,
            variant_types=json.dumps(variant_types),
            total_suggestions=0,
            status="running"
        )
        db.add(search_history)
        await db.commit()
        
        results = {
            'session_id': session_id,
            'base_keyword': base_keyword,
            'variant_types': variant_types,
            'total_variants': total_variants,
            'results': {},
            'summary': {
                'total_suggestions': 0,
                'successful_variants': 0,
                'failed_variants': 0
            }
        }
        
        processed = 0
        
        try:
            async with BaiduSuggestService() as baidu_service:
                for variant_type, variant_list in variants.items():
                    results['results'][variant_type] = {}
                    
                    # 批量获取建议词
                    suggestions_dict = await baidu_service.batch_get_suggestions(
                        variant_list, 
                        concurrency=2  # 降低并发数避免被限制
                    )
                    
                    for variant_keyword, suggestions in suggestions_dict.items():
                        processed += 1
                        
                        # 更新进度
                        if progress_callback:
                            await progress_callback(processed, total_variants)
                        
                        if suggestions:
                            results['results'][variant_type][variant_keyword] = suggestions
                            results['summary']['successful_variants'] += 1
                            results['summary']['total_suggestions'] += len(suggestions)
                            
                            # 保存到数据库
                            for rank, suggestion in enumerate(suggestions, 1):
                                keyword_result = KeywordResult(
                                    original_keyword=base_keyword,
                                    variant_keyword=variant_keyword,
                                    suggestion=suggestion,
                                    suggestion_rank=rank,
                                    variant_type=variant_type
                                )
                                db.add(keyword_result)
                        else:
                            results['summary']['failed_variants'] += 1
                        
                        # 每10个变体提交一次
                        if processed % 10 == 0:
                            await db.commit()
                
                # 最终提交
                await db.commit()
                
                # 更新搜索历史
                search_history.total_suggestions = results['summary']['total_suggestions']
                search_history.status = "completed"
                await db.commit()
                
        except Exception as e:
            # 更新搜索历史为失败状态
            search_history.status = "failed"
            await db.commit()
            raise e
        
        return results
    
    @staticmethod
    async def get_search_history(db: AsyncSession, limit: int = 10) -> List[Dict]:
        """获取搜索历史"""
        query = select(SearchHistory).order_by(SearchHistory.created_at.desc()).limit(limit)
        result = await db.execute(query)
        histories = result.scalars().all()
        
        return [
            {
                'session_id': h.session_id,
                'original_keyword': h.original_keyword,
                'variant_types': json.loads(h.variant_types) if h.variant_types else [],
                'total_suggestions': h.total_suggestions,
                'status': h.status,
                'created_at': h.created_at.isoformat()
            }
            for h in histories
        ]
    
    @staticmethod
    async def get_session_results(session_id: str, db: AsyncSession) -> Dict:
        """获取特定会话的结果"""
        query = select(KeywordResult).where(
            KeywordResult.original_keyword == (
                select(SearchHistory.original_keyword).where(
                    SearchHistory.session_id == session_id
                )
            )
        ).order_by(KeywordResult.variant_type, KeywordResult.variant_keyword, KeywordResult.suggestion_rank)
        
        result = await db.execute(query)
        keyword_results = result.scalars().all()
        
        # 按类型组织数据
        organized_results = {}
        for kr in keyword_results:
            if kr.variant_type not in organized_results:
                organized_results[kr.variant_type] = {}
            if kr.variant_keyword not in organized_results[kr.variant_type]:
                organized_results[kr.variant_type][kr.variant_keyword] = []
            organized_results[kr.variant_type][kr.variant_keyword].append(kr.suggestion)
        
        return {
            'session_id': session_id,
            'results': organized_results
        }