"""
商业价值分析服务
提供关键词的商业价值评分、用户意图分析等功能
集成5118真实数据提供准确的市场分析
"""
import re
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from services.five118_service import FiveOneOneEightService, KeywordData5118

@dataclass
class BusinessMetrics:
    """商业指标数据类"""
    commercial_score: float  # 商业价值评分 (0-100)
    intent_type: str        # 用户意图类型
    competition_level: str   # 竞争激烈度
    search_volume_estimate: int  # 搜索量估算
    difficulty_score: float  # SEO难度评分
    opportunity_score: float # 机会评分
    is_blue_ocean: bool = False  # 是否为蓝海词
    real_data_available: bool = False  # 是否有真实数据
    
@dataclass 
class BlueOceanKeyword:
    """蓝海关键词数据"""
    keyword: str
    opportunity_score: float
    search_volume: int
    competition_companies: int
    competition_level: str
    sem_price: str
    longtail_count: int
    platforms: Dict[str, int]  # 各平台指数
    reasons: List[str]  # 推荐理由

class BusinessAnalyzer:
    """商业价值分析器 - 集成5118真实数据"""
    
    # 商业意图关键词库
    COMMERCIAL_KEYWORDS = {
        'high': [
            '购买', '买', '价格', '优惠', '折扣', '促销', '团购', '秒杀', 
            '免费', '试用', '下载', '注册', '开户', '申请', '订购',
            '预约', '咨询', '服务', '代理', '加盟', '招商', '合作'
        ],
        'medium': [
            '费用', '收费', '多少钱', '报价', '评价', '口碑', '推荐',
            '对比', '选择', '哪家好', '排行榜', '品牌', '公司', '厂家'
        ],
        'low': [
            '什么', '怎么', '如何', '为什么', '是什么', '原理', '介绍',
            '教程', '方法', '步骤', '流程', '注意事项', '基础知识'
        ]
    }
    
    # 行业热词库 
    INDUSTRY_KEYWORDS = {
        'education': ['培训', '教育', '学习', '课程', '考试', '证书', '学校', '大学'],
        'finance': ['贷款', '投资', '理财', '保险', '银行', '股票', '基金', '信用卡'],
        'healthcare': ['医院', '医生', '治疗', '药物', '健康', '疾病', '症状', '体检'],
        'ecommerce': ['商城', '购物', '电商', '零售', '批发', '商品', '店铺', '平台'],
        'technology': ['软件', '系统', '技术', '开发', '程序', 'AI', '数据', '云计算'],
        'real_estate': ['房产', '楼盘', '租房', '买房', '装修', '家具', '建材', '物业']
    }

    @staticmethod
    async def analyze_with_real_data(keyword: str, enable_5118: bool = True) -> BusinessMetrics:
        """
        使用5118真实数据分析关键词商业价值
        
        Args:
            keyword: 分析的关键词
            enable_5118: 是否启用5118真实数据
        """
        if enable_5118:
            try:
                async with FiveOneOneEightService() as service:
                    # 获取5118真实数据
                    real_data = await service.get_keyword_data(keyword, page_size=1)
                    
                    if real_data:
                        kw_data = real_data[0]
                        return BusinessAnalyzer._analyze_with_5118_data(kw_data)
            except Exception as e:
                print(f"5118数据获取失败，使用估算模式: {e}")
        
        # 回退到估算模式
        return BusinessAnalyzer.analyze_keyword(keyword)
    
    @staticmethod
    def _analyze_with_5118_data(kw_data: KeywordData5118) -> BusinessMetrics:
        """基于5118真实数据进行分析"""
        
        # 1. 基于真实竞争数据计算商业价值评分
        commercial_score = BusinessAnalyzer._calculate_real_commercial_score(kw_data)
        
        # 2. 基于SEM数据分析用户意图
        intent_type = BusinessAnalyzer._analyze_intent_from_sem_data(kw_data)
        
        # 3. 基于竞价公司数判断竞争激烈度
        competition_level = BusinessAnalyzer._get_real_competition_level(kw_data)
        
        # 4. 使用真实搜索量
        search_volume = kw_data.bidword_pcpv + kw_data.bidword_wisepv
        
        # 5. 基于真实竞争数据计算SEO难度
        difficulty_score = BusinessAnalyzer._calculate_real_seo_difficulty(kw_data)
        
        # 6. 综合真实数据计算机会评分
        opportunity_score = BusinessAnalyzer._calculate_real_opportunity_score(kw_data)
        
        # 7. 蓝海词判断
        is_blue_ocean = BusinessAnalyzer._is_blue_ocean_keyword(kw_data)
        
        return BusinessMetrics(
            commercial_score=round(commercial_score, 1),
            intent_type=intent_type,
            competition_level=competition_level,
            search_volume_estimate=search_volume,
            difficulty_score=round(difficulty_score, 1),
            opportunity_score=round(opportunity_score, 1),
            is_blue_ocean=is_blue_ocean,
            real_data_available=True
        )
    
    @staticmethod
    def _calculate_real_commercial_score(kw_data: KeywordData5118) -> float:
        """基于5118数据计算真实商业价值评分"""
        score = 0.0
        
        # 1. SEM竞价活跃度 (40分)
        if kw_data.bidword_company_count > 0:
            # 有竞价公司说明有商业价值
            score += min(kw_data.bidword_company_count * 3, 30)
            
            # SEM价格反映商业价值
            if kw_data.sem_price:
                try:
                    # 解析价格范围 "0.45~3.20"
                    if '~' in kw_data.sem_price:
                        max_price = float(kw_data.sem_price.split('~')[1])
                        score += min(max_price * 5, 10)  # 最高10分
                except:
                    score += 5  # 有价格信息就加5分
        
        # 2. 流量特点商业价值 (25分)
        sem_reason = kw_data.sem_reason.lower()
        commercial_indicators = ['购买', '价格', '品牌', '推荐', '评测', '对比']
        for indicator in commercial_indicators:
            if indicator in sem_reason:
                score += 5
        
        # 3. 搜索量体现需求强度 (20分)
        total_volume = kw_data.bidword_pcpv + kw_data.bidword_wisepv
        if total_volume > 0:
            score += min(total_volume / 100, 20)
        
        # 4. 多平台指数体现热度 (15分)
        if kw_data.douyin_index > 0:
            score += 8  # 抖音热度高说明消费潜力大
        if kw_data.haosou_index > 0:
            score += 4
        if kw_data.mobile_index > 0:
            score += 3
        
        return min(score, 100.0)
    
    @staticmethod
    def _analyze_intent_from_sem_data(kw_data: KeywordData5118) -> str:
        """基于SEM数据分析用户意图"""
        sem_reason = kw_data.sem_reason.lower()
        keyword = kw_data.keyword.lower()
        
        # 交易型意图判断
        transaction_signals = ['购买', '买', '价格', '优惠', '促销', '团购']
        if any(signal in sem_reason or signal in keyword for signal in transaction_signals):
            return "交易型"
        
        # 商业型意图判断  
        commercial_signals = ['品牌', '推荐', '评测', '对比', '排行', '哪家好']
        if any(signal in sem_reason or signal in keyword for signal in commercial_signals):
            return "商业型"
        
        # 基于竞价活跃度判断
        if kw_data.bidword_company_count >= 10:
            return "商业型"
        elif kw_data.bidword_company_count >= 3:
            return "交易型"
        
        # 信息型意图
        info_signals = ['什么', '怎么', '如何', '教程', '方法']
        if any(signal in keyword for signal in info_signals):
            return "信息型"
        
        return "混合型"
    
    @staticmethod
    def _get_real_competition_level(kw_data: KeywordData5118) -> str:
        """基于真实竞价数据判断竞争激烈度"""
        company_count = kw_data.bidword_company_count
        competition_grade = kw_data.bidword_kwc  # 1高2中3低
        
        if company_count >= 20 or competition_grade == 1:
            return "激烈"
        elif company_count >= 10 or competition_grade == 2:
            return "中等"  
        elif company_count >= 3 or competition_grade == 3:
            return "较低"
        else:
            return "很低"
    
    @staticmethod
    def _calculate_real_seo_difficulty(kw_data: KeywordData5118) -> float:
        """基于真实数据计算SEO难度"""
        difficulty = 0.0
        
        # 竞价公司数反映SEO难度
        difficulty += min(kw_data.bidword_company_count * 2, 40)
        
        # 竞争激烈程度
        competition_score = {1: 30, 2: 20, 3: 10}.get(kw_data.bidword_kwc, 10)
        difficulty += competition_score
        
        # 搜索量高的词SEO难度大
        total_volume = kw_data.bidword_pcpv + kw_data.bidword_wisepv
        difficulty += min(total_volume / 200, 20)
        
        # 多平台热度高难度大
        if kw_data.douyin_index > 100:
            difficulty += 10
        
        return min(difficulty, 100.0)
    
    @staticmethod  
    def _calculate_real_opportunity_score(kw_data: KeywordData5118) -> float:
        """基于真实数据计算机会评分"""
        # 搜索需求得分 (40%)
        search_demand = kw_data.bidword_pcpv + kw_data.bidword_wisepv
        demand_score = min(search_demand / 10, 40)
        
        # 竞争程度得分 (35%) - 竞争越低得分越高
        max_competition = 50  # 假设最大竞争公司数
        competition_score = max(0, (max_competition - kw_data.bidword_company_count) / max_competition * 35)
        
        # 长尾扩展机会 (15%)
        longtail_score = min(kw_data.long_keyword_count / 10000 * 15, 15)
        
        # 商业价值得分 (10%)
        commercial_score = 0
        if kw_data.sem_price:
            commercial_score += 5
        if '购买' in kw_data.sem_reason or '价格' in kw_data.sem_reason:
            commercial_score += 5
        
        total_score = demand_score + competition_score + longtail_score + commercial_score
        return min(total_score, 100.0)
    
    @staticmethod
    def _is_blue_ocean_keyword(kw_data: KeywordData5118) -> bool:
        """判断是否为蓝海关键词 - 优化后的宽松标准"""
        return (
            # 有搜索需求（降低门槛）
            (kw_data.bidword_wisepv >= 10 or kw_data.mobile_index >= 50 or kw_data.index >= 50) and
            
            # 竞争程度适中（放宽标准）
            kw_data.bidword_company_count <= 10 and
            kw_data.bidword_kwc >= 2 and  # 竞争度为中或低
            
            # 有长尾扩展空间（降低门槛）
            kw_data.long_keyword_count >= 100 and
            
            # 有一定商业价值
            (kw_data.bidword_company_count > 0 or 
             kw_data.sem_price != "" or 
             kw_data.bidword_pcpv > 0 or
             kw_data.bidword_wisepv > 0)
        )
    
    @staticmethod
    async def discover_blue_ocean_keywords(base_keyword: str, limit: int = 10) -> List[BlueOceanKeyword]:
        """发现蓝海关键词"""
        try:
            async with FiveOneOneEightService() as service:
                blue_ocean_data = await service.get_blue_ocean_keywords(
                    base_keyword,
                    min_search_volume=10,  # 降低最小搜索量
                    max_competition=10,    # 提高最大竞争公司数 
                    min_longtail_count=100 # 降低最小长尾词数量
                )
                
                results = []
                for kw_data in blue_ocean_data[:limit]:
                    # 生成推荐理由
                    reasons = []
                    if kw_data.bidword_company_count <= 3:
                        reasons.append(f"竞争公司仅{kw_data.bidword_company_count}家")
                    if kw_data.bidword_wisepv >= 50:
                        reasons.append(f"移动端日均{kw_data.bidword_wisepv}次搜索")
                    if kw_data.long_keyword_count >= 1000:
                        reasons.append(f"可扩展{kw_data.long_keyword_count}个长尾词")
                    if kw_data.douyin_index > 0:
                        reasons.append(f"抖音指数{kw_data.douyin_index}")
                    
                    blue_ocean = BlueOceanKeyword(
                        keyword=kw_data.keyword,
                        opportunity_score=service._calculate_opportunity_score(kw_data),
                        search_volume=kw_data.bidword_pcpv + kw_data.bidword_wisepv,
                        competition_companies=kw_data.bidword_company_count,
                        competition_level={1: "高", 2: "中", 3: "低"}.get(kw_data.bidword_kwc, "未知"),
                        sem_price=kw_data.sem_price or "无数据",
                        longtail_count=kw_data.long_keyword_count,
                        platforms={
                            "百度PC": kw_data.index,
                            "百度移动": kw_data.mobile_index,
                            "360搜索": kw_data.haosou_index,
                            "抖音": kw_data.douyin_index
                        },
                        reasons=reasons
                    )
                    results.append(blue_ocean)
                
                return results
                
        except Exception as e:
            print(f"蓝海词发现失败: {e}")
            return []

    # 保留原有的估算方法作为后备
    @staticmethod
    def calculate_commercial_score(keyword: str) -> float:
        """计算商业价值评分（估算模式）"""
        score = 0.0
        keyword_lower = keyword.lower()
        
        # 1. 商业意图词权重 (40分)
        for intent_level, words in BusinessAnalyzer.COMMERCIAL_KEYWORDS.items():
            for word in words:
                if word in keyword:
                    if intent_level == 'high':
                        score += 15
                    elif intent_level == 'medium':
                        score += 8
                    elif intent_level == 'low':
                        score += 3
        
        # 2. 关键词长度评分 (20分)
        length = len(keyword)
        if length >= 8:
            score += 20
        elif length >= 5:
            score += 15
        elif length >= 3:
            score += 10
        else:
            score += 5
            
        # 3. 数字和特殊符号评分 (15分)
        if re.search(r'\d+', keyword):
            score += 10
        if any(char in keyword for char in ['年', '月', '日', '元', '万', '千', '百']):
            score += 5
            
        # 4. 地域性评分 (15分)
        location_words = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', 
                         '附近', '本地', '当地', '周边', '市', '区', '县', '镇']
        if any(loc in keyword for loc in location_words):
            score += 15
            
        # 5. 行业热度评分 (10分)
        for industry, words in BusinessAnalyzer.INDUSTRY_KEYWORDS.items():
            if any(word in keyword for word in words):
                score += 10
                break
        
        return min(score, 100.0)
    
    @staticmethod
    def analyze_user_intent(keyword: str) -> str:
        """分析用户意图类型（估算模式）"""
        keyword_lower = keyword.lower()
        
        # 交易型意图
        transaction_words = BusinessAnalyzer.COMMERCIAL_KEYWORDS['high']
        if any(word in keyword for word in transaction_words):
            return "交易型"
        
        # 商业型意图  
        commercial_words = BusinessAnalyzer.COMMERCIAL_KEYWORDS['medium']
        if any(word in keyword for word in commercial_words):
            return "商业型"
        
        # 信息型意图
        info_words = BusinessAnalyzer.COMMERCIAL_KEYWORDS['low']
        if any(word in keyword for word in info_words):
            return "信息型"
        
        # 导航型意图
        navigation_words = ['官网', '网站', '登录', '首页', '主页', '入口']
        if any(word in keyword for word in navigation_words):
            return "导航型"
        
        return "混合型"
    
    @staticmethod
    def estimate_competition_level(keyword: str, suggestions_count: int) -> str:
        """估算竞争激烈度（估算模式）"""
        commercial_score = BusinessAnalyzer.calculate_commercial_score(keyword)
        
        if commercial_score >= 70 and suggestions_count >= 8:
            return "激烈"
        elif commercial_score >= 50 and suggestions_count >= 5:
            return "中等"
        elif commercial_score >= 30 or suggestions_count >= 3:
            return "较低"
        else:
            return "很低"
    
    @staticmethod
    def estimate_search_volume(keyword: str, suggestions_count: int) -> int:
        """估算搜索量（估算模式）"""
        base_volume = 1000
        
        length_factor = max(0.5, 2.0 - len(keyword) * 0.1)
        commercial_score = BusinessAnalyzer.calculate_commercial_score(keyword)
        commercial_factor = 1.0 + (commercial_score / 100.0)
        suggestions_factor = 1.0 + (suggestions_count * 0.1)
        
        estimated_volume = int(base_volume * length_factor * commercial_factor * suggestions_factor)
        
        return min(estimated_volume, 50000)
    
    @staticmethod
    def calculate_difficulty_score(keyword: str, suggestions_count: int) -> float:
        """计算SEO难度评分（估算模式）"""
        commercial_score = BusinessAnalyzer.calculate_commercial_score(keyword)
        
        difficulty = commercial_score * 0.6
        difficulty += min(suggestions_count * 2, 30)
        
        for industry, words in BusinessAnalyzer.INDUSTRY_KEYWORDS.items():
            if any(word in keyword for word in words):
                difficulty += 10
                break
        
        return min(difficulty, 100.0)
    
    @staticmethod
    def calculate_opportunity_score(commercial_score: float, difficulty_score: float, 
                                   competition_level: str) -> float:
        """计算机会评分（估算模式）"""
        opportunity = commercial_score
        opportunity -= difficulty_score * 0.3
        
        competition_penalty = {
            "很低": 0,
            "较低": 5, 
            "中等": 15,
            "激烈": 25
        }
        opportunity -= competition_penalty.get(competition_level, 10)
        
        return max(0, min(opportunity, 100.0))
    
    @staticmethod
    def analyze_keyword(keyword: str, suggestions_count: int = 0) -> BusinessMetrics:
        """综合分析关键词的商业价值（估算模式）"""
        commercial_score = BusinessAnalyzer.calculate_commercial_score(keyword)
        intent_type = BusinessAnalyzer.analyze_user_intent(keyword)
        competition_level = BusinessAnalyzer.estimate_competition_level(keyword, suggestions_count)
        search_volume_estimate = BusinessAnalyzer.estimate_search_volume(keyword, suggestions_count)
        difficulty_score = BusinessAnalyzer.calculate_difficulty_score(keyword, suggestions_count)
        opportunity_score = BusinessAnalyzer.calculate_opportunity_score(
            commercial_score, difficulty_score, competition_level
        )
        
        return BusinessMetrics(
            commercial_score=round(commercial_score, 1),
            intent_type=intent_type,
            competition_level=competition_level,
            search_volume_estimate=search_volume_estimate,
            difficulty_score=round(difficulty_score, 1),
            opportunity_score=round(opportunity_score, 1),
            real_data_available=False
        )
    
    @staticmethod
    def analyze_suggestion_list(suggestions: List[str]) -> Dict:
        """分析建议词列表的整体商业价值"""
        if not suggestions:
            return {
                'total_count': 0,
                'average_commercial_score': 0,
                'intent_distribution': {},
                'top_opportunities': []
            }
        
        total_commercial_score = 0
        intent_counts = {}
        analyzed_suggestions = []
        
        for suggestion in suggestions:
            metrics = BusinessAnalyzer.analyze_keyword(suggestion, len(suggestions))
            total_commercial_score += metrics.commercial_score
            
            intent_counts[metrics.intent_type] = intent_counts.get(metrics.intent_type, 0) + 1
            
            analyzed_suggestions.append({
                'keyword': suggestion,
                'metrics': metrics
            })
        
        top_opportunities = sorted(
            analyzed_suggestions, 
            key=lambda x: x['metrics'].opportunity_score, 
            reverse=True
        )[:5]
        
        return {
            'total_count': len(suggestions),
            'average_commercial_score': round(total_commercial_score / len(suggestions), 1),
            'intent_distribution': intent_counts,
            'top_opportunities': [
                {
                    'keyword': item['keyword'],
                    'commercial_score': item['metrics'].commercial_score,
                    'opportunity_score': item['metrics'].opportunity_score,
                    'intent_type': item['metrics'].intent_type,
                    'search_volume_estimate': item['metrics'].search_volume_estimate
                }
                for item in top_opportunities
            ]
        }