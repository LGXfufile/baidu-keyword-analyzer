import httpx
import asyncio
import json
import re
from urllib.parse import quote
from typing import List, Dict, Optional
from fake_useragent import UserAgent
from config import settings
import random
import logging

logger = logging.getLogger(__name__)

class BaiduSuggestService:
    def __init__(self):
        self.ua = UserAgent()
        self.session = None
        
    async def __aenter__(self):
        self.session = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.REQUEST_TIMEOUT),
            follow_redirects=True
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    def _get_headers(self) -> Dict[str, str]:
        """生成随机请求头"""
        return {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': self.ua.random,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.baidu.com/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }
    
    def _build_params(self, keyword: str) -> Dict[str, str]:
        """构建请求参数"""
        encoded_keyword = quote(keyword)
        return {
            'pre': '1',
            'p': '3', 
            'ie': 'utf-8',
            'json': '1',
            'prod': 'pc',
            'from': 'pc_web',
            'wd': encoded_keyword,
            'req': '2',
            'csor': '7',
            'cb': f'jQuery{random.randint(100000000000000000000, 999999999999999999999)}_{random.randint(1000000000000, 9999999999999)}',
            '_': str(random.randint(1000000000000, 9999999999999))
        }
    
    def _parse_jsonp_response(self, text: str) -> Optional[Dict]:
        """解析JSONP响应"""
        try:
            # 提取JSON部分
            match = re.search(r'jQuery\d+_\d+\((.*)\)', text)
            if match:
                json_str = match.group(1)
                return json.loads(json_str)
            return None
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"解析JSONP响应失败: {e}")
            return None
    
    async def get_suggestions(self, keyword: str, max_retries: int = None) -> List[str]:
        """获取关键词建议"""
        if max_retries is None:
            max_retries = settings.MAX_RETRIES
            
        for attempt in range(max_retries):
            try:
                # 随机延迟
                delay = random.uniform(settings.REQUEST_DELAY_MIN, settings.REQUEST_DELAY_MAX)
                if attempt > 0:
                    await asyncio.sleep(delay)
                
                params = self._build_params(keyword)
                headers = self._get_headers()
                
                response = await self.session.get(
                    settings.BAIDU_SUGGEST_URL,
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = self._parse_jsonp_response(response.text)
                    if data and 'g' in data:
                        suggestions = []
                        for item in data['g']:
                            if 'q' in item:
                                suggestions.append(item['q'])
                        return suggestions
                    else:
                        logger.warning(f"响应数据格式异常: {keyword}")
                        
                else:
                    logger.warning(f"请求失败 {response.status_code}: {keyword}")
                    
            except httpx.TimeoutException:
                logger.warning(f"请求超时 (尝试 {attempt + 1}/{max_retries}): {keyword}")
            except Exception as e:
                logger.error(f"请求异常 (尝试 {attempt + 1}/{max_retries}): {keyword}, 错误: {e}")
        
        logger.error(f"获取建议词失败，已重试 {max_retries} 次: {keyword}")
        return []
    
    async def batch_get_suggestions(self, keywords: List[str], concurrency: int = 3) -> Dict[str, List[str]]:
        """批量获取关键词建议"""
        semaphore = asyncio.Semaphore(concurrency)
        
        async def get_with_semaphore(keyword: str):
            async with semaphore:
                suggestions = await self.get_suggestions(keyword)
                return keyword, suggestions
        
        tasks = [get_with_semaphore(keyword) for keyword in keywords]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        suggestions_dict = {}
        for result in results:
            if isinstance(result, tuple):
                keyword, suggestions = result
                suggestions_dict[keyword] = suggestions
            else:
                logger.error(f"批量获取异常: {result}")
                
        return suggestions_dict