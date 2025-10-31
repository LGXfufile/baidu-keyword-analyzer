"""
5118 API集成服务
提供真实的关键词搜索量、竞争度等数据
"""
import aiohttp
import asyncio
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from config import settings

logger = logging.getLogger(__name__)

@dataclass
class KeywordData5118:
    """5118关键词数据结构"""
    keyword: str
    index: int  # 流量指数
    mobile_index: int  # 移动指数
    haosou_index: int  # 360指数
    douyin_index: int  # 抖音指数
    long_keyword_count: int  # 长尾词数量
    bidword_company_count: int  # 竞价公司数量
    bidword_kwc: int  # 竞价竞争度(1高2中3低)
    bidword_pcpv: int  # PC日检索量
    bidword_wisepv: int  # 移动日检索量
    sem_reason: str  # 流量特点
    sem_price: str  # SEM点击价格
    page_url: str  # 推荐网站

class FiveOneOneEightService:
    """5118 API服务类"""
    
    def __init__(self, api_key: str = "39BBC591817B4116879FD9BF3D8F584C"):
        self.api_key = api_key
        self.base_url = "http://apis.5118.com"
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                "Authorization": self.api_key,
                "Content-Type": "application/json"
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def get_keyword_data(
        self, 
        keyword: str, 
        page_size: int = 100,
        sort_by_mobile: bool = True,
        filter_type: int = 2  # 2:所有流量词
    ) -> List[KeywordData5118]:
        """
        获取关键词的5118数据
        
        Args:
            keyword: 查询关键词
            page_size: 返回数量，最大100
            sort_by_mobile: 是否按移动检索量排序
            filter_type: 过滤类型，2=所有流量词
        """
        if not self.session:
            raise RuntimeError("请在async with语句中使用此服务")
            
        # 构建请求参数
        params = {
            "keyword": keyword,
            "page_index": 1,
            "page_size": min(page_size, 100),
            "sort_fields": 8 if sort_by_mobile else 7,  # 8:移动检索量 7:PC检索量
            "sort_type": "desc",
            "filter": filter_type
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/keyword/word/v2",
                json=params
            ) as response:
                
                if response.status != 200:
                    logger.error(f"5118 API请求失败: HTTP {response.status}")
                    return []
                
                data = await response.json()
                
                # 检查返回错误码
                if data.get("errcode") != "0":
                    logger.error(f"5118 API返回错误: {data.get('errcode')} - {data.get('errmsg')}")
                    return []
                
                # 解析返回的关键词数据
                word_list = data.get("data", {}).get("word", [])
                
                result = []
                for word_data in word_list:
                    try:
                        keyword_obj = KeywordData5118(
                            keyword=word_data.get("keyword", ""),
                            index=word_data.get("index", 0),
                            mobile_index=word_data.get("mobile_index", 0),
                            haosou_index=word_data.get("haosou_index", 0),
                            douyin_index=word_data.get("douyin_index", 0),
                            long_keyword_count=word_data.get("long_keyword_count", 0),
                            bidword_company_count=word_data.get("bidword_company_count", 0),
                            bidword_kwc=word_data.get("bidword_kwc", 3),
                            bidword_pcpv=word_data.get("bidword_pcpv", 0),
                            bidword_wisepv=word_data.get("bidword_wisepv", 0),
                            sem_reason=word_data.get("sem_reason", ""),
                            sem_price=word_data.get("sem_price", ""),
                            page_url=word_data.get("page_url", "")
                        )
                        result.append(keyword_obj)
                    except Exception as e:
                        logger.warning(f"解析关键词数据失败: {e}")
                        continue
                
                logger.info(f"5118获取关键词数据成功: {keyword} -> {len(result)}条")
                return result
                
        except Exception as e:
            logger.error(f"5118 API调用异常: {e}")
            return []
    
    async def get_blue_ocean_keywords(
        self, 
        keyword: str, 
        min_search_volume: int = 50,
        max_competition: int = 3,
        min_longtail_count: int = 100
    ) -> List[KeywordData5118]:
        """
        获取蓝海关键词
        
        Args:
            keyword: 基础关键词
            min_search_volume: 最小搜索量（移动端）
            max_competition: 最大竞价公司数
            min_longtail_count: 最小长尾词数量
        """
        # 先获取所有相关关键词
        all_keywords = await self.get_keyword_data(keyword, page_size=100)
        
        blue_ocean_keywords = []
        
        for kw_data in all_keywords:
            # 蓝海词判断逻辑
            is_blue_ocean = (
                # 有一定搜索需求
                (kw_data.bidword_wisepv >= min_search_volume or kw_data.mobile_index >= 100) and
                
                # 竞争程度不高
                kw_data.bidword_company_count <= max_competition and
                kw_data.bidword_kwc >= 2 and  # 竞争度为中或低
                
                # 有长尾扩展机会
                kw_data.long_keyword_count >= min_longtail_count and
                
                # 有商业价值
                (self._has_commercial_value(kw_data.sem_reason) or 
                 kw_data.sem_price != "" or
                 kw_data.bidword_company_count > 0)
            )
            
            if is_blue_ocean:
                blue_ocean_keywords.append(kw_data)
        
        # 按机会评分排序
        blue_ocean_keywords.sort(
            key=lambda x: self._calculate_opportunity_score(x), 
            reverse=True
        )
        
        logger.info(f"发现蓝海词: {len(blue_ocean_keywords)} 个")
        return blue_ocean_keywords[:20]  # 返回前20个最佳机会
    
    def _has_commercial_value(self, sem_reason: str) -> bool:
        """判断是否有商业价值"""
        commercial_indicators = [
            "购买", "价格", "多少钱", "费用", "优惠", "促销",
            "品牌", "推荐", "评测", "对比", "排行",
            "加盟", "代理", "招商", "合作"
        ]
        return any(indicator in sem_reason for indicator in commercial_indicators)
    
    def _calculate_opportunity_score(self, kw_data: KeywordData5118) -> float:
        """计算机会评分"""
        # 搜索量得分 (30%)
        search_score = min((kw_data.bidword_wisepv + kw_data.bidword_pcpv) / 1000 * 30, 30)
        
        # 竞争度得分 (40%) - 竞争越低得分越高
        competition_score = (4 - kw_data.bidword_company_count) * 10
        competition_score += (kw_data.bidword_kwc - 1) * 10  # kwc=3(低竞争)得分最高
        
        # 长尾机会得分 (20%)
        longtail_score = min(kw_data.long_keyword_count / 10000 * 20, 20)
        
        # 多平台指数得分 (10%)
        multi_platform_score = 0
        if kw_data.douyin_index > 0:
            multi_platform_score += 5
        if kw_data.haosou_index > 0:
            multi_platform_score += 3
        if kw_data.mobile_index > 0:
            multi_platform_score += 2
        
        total_score = search_score + competition_score + longtail_score + multi_platform_score
        return min(total_score, 100.0)
    
    async def batch_analyze_keywords(self, keywords: List[str]) -> Dict[str, List[KeywordData5118]]:
        """批量分析多个关键词"""
        results = {}
        
        # 控制并发数量，避免API限制
        semaphore = asyncio.Semaphore(3)
        
        async def analyze_single(keyword: str):
            async with semaphore:
                data = await self.get_keyword_data(keyword)
                results[keyword] = data
                await asyncio.sleep(0.5)  # 防止请求过快
        
        # 并发执行
        tasks = [analyze_single(kw) for kw in keywords]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return results