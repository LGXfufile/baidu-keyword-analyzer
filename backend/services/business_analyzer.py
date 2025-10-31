"""
商业价值分析服务
提供关键词的商业价值评分、用户意图分析等功能
"""
import re
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class BusinessMetrics:
    """商业指标数据类"""
    commercial_score: float  # 商业价值评分 (0-100)
    intent_type: str        # 用户意图类型
    competition_level: str   # 竞争激烈度
    search_volume_estimate: int  # 搜索量估算
    difficulty_score: float  # SEO难度评分
    opportunity_score: float # 机会评分

class BusinessAnalyzer:
    """商业价值分析器"""
    
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
    def calculate_commercial_score(keyword: str) -> float:
        """计算商业价值评分"""
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
        # 长尾词通常商业价值更高，竞争更小
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
        # 包含价格、日期、型号等的词通常商业意图更强
        if re.search(r'\d+', keyword):
            score += 10
        if any(char in keyword for char in ['年', '月', '日', '元', '万', '千', '百']):
            score += 5
            
        # 4. 地域性评分 (15分)
        # 带地域的词通常转化率更高
        location_words = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', 
                         '附近', '本地', '当地', '周边', '市', '区', '县', '镇']
        if any(loc in keyword for loc in location_words):
            score += 15
            
        # 5. 行业热度评分 (10分)
        for industry, words in BusinessAnalyzer.INDUSTRY_KEYWORDS.items():
            if any(word in keyword for word in words):
                score += 10
                break
        
        return min(score, 100.0)  # 限制最高100分
    
    @staticmethod
    def analyze_user_intent(keyword: str) -> str:
        """分析用户意图类型"""
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
        """估算竞争激烈度"""
        # 基于关键词特征和建议词数量
        commercial_score = BusinessAnalyzer.calculate_commercial_score(keyword)
        
        # 商业价值高 + 建议词多 = 竞争激烈
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
        """估算搜索量"""
        # 基于关键词长度、商业价值和建议词数量的简单估算
        base_volume = 1000
        
        # 长度因子
        length_factor = max(0.5, 2.0 - len(keyword) * 0.1)
        
        # 商业价值因子
        commercial_score = BusinessAnalyzer.calculate_commercial_score(keyword)
        commercial_factor = 1.0 + (commercial_score / 100.0)
        
        # 建议词数量因子
        suggestions_factor = 1.0 + (suggestions_count * 0.1)
        
        estimated_volume = int(base_volume * length_factor * commercial_factor * suggestions_factor)
        
        return min(estimated_volume, 50000)  # 限制最大值
    
    @staticmethod
    def calculate_difficulty_score(keyword: str, suggestions_count: int) -> float:
        """计算SEO难度评分"""
        commercial_score = BusinessAnalyzer.calculate_commercial_score(keyword)
        
        # 商业价值越高，SEO难度越大
        difficulty = commercial_score * 0.6
        
        # 建议词越多，说明相关内容越多，难度越大
        difficulty += min(suggestions_count * 2, 30)
        
        # 热门行业词难度更高
        for industry, words in BusinessAnalyzer.INDUSTRY_KEYWORDS.items():
            if any(word in keyword for word in words):
                difficulty += 10
                break
        
        return min(difficulty, 100.0)
    
    @staticmethod
    def calculate_opportunity_score(commercial_score: float, difficulty_score: float, 
                                   competition_level: str) -> float:
        """计算机会评分 (高商业价值 + 低难度 = 高机会)"""
        # 基础机会分 = 商业价值分
        opportunity = commercial_score
        
        # 难度惩罚
        opportunity -= difficulty_score * 0.3
        
        # 竞争惩罚
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
        """综合分析关键词的商业价值"""
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
            opportunity_score=round(opportunity_score, 1)
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
            
            # 统计意图分布
            intent_counts[metrics.intent_type] = intent_counts.get(metrics.intent_type, 0) + 1
            
            analyzed_suggestions.append({
                'keyword': suggestion,
                'metrics': metrics
            })
        
        # 按机会评分排序，取前5个
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