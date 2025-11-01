<template>
  <div class="apple-card p-8 animate-apple-enter">
    <!-- 标题区域 -->
    <div class="flex items-center mb-8">
      <div class="w-8 h-8 bg-gradient-to-br from-green-500 to-blue-500 rounded-xl flex items-center justify-center mr-4">
        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
      </div>
      <div>
        <h2 class="text-apple-title text-apple-2xl">商业价值分析</h2>
        <p class="text-apple-caption text-apple-sm mt-1">AI驱动的关键词商业洞察</p>
      </div>
    </div>

    <!-- 整体商业指标 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-2xl">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-blue-100 text-apple-sm opacity-90">平均商业价值</p>
            <p class="text-apple-3xl font-bold">{{ summary?.average_commercial_score || 0 }}</p>
            <p class="text-blue-100 text-apple-xs mt-1">满分100分</p>
          </div>
          <div class="w-12 h-12 bg-blue-400/30 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-2xl">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-green-100 text-apple-sm opacity-90">最佳机会数</p>
            <p class="text-apple-3xl font-bold">{{ topOpportunities.length }}</p>
            <p class="text-green-100 text-apple-xs mt-1">高潜力关键词</p>
          </div>
          <div class="w-12 h-12 bg-green-400/30 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-2xl">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-purple-100 text-apple-sm opacity-90">预估搜索量</p>
            <p class="text-apple-3xl font-bold">{{ formatNumber(totalSearchVolume) }}</p>
            <p class="text-purple-100 text-apple-xs mt-1">月均搜索次数</p>
          </div>
          <div class="w-12 h-12 bg-purple-400/30 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-orange-500 to-orange-600 text-white p-6 rounded-2xl">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-orange-100 text-apple-sm opacity-90">主要意图</p>
            <p class="text-apple-lg font-semibold">{{ primaryIntent }}</p>
            <p class="text-orange-100 text-apple-xs mt-1">用户搜索意图</p>
          </div>
          <div class="w-12 h-12 bg-orange-400/30 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 意图分布图 -->
    <div class="mb-8">
      <h3 class="text-apple-title text-apple-lg mb-4">用户意图分布</h3>
      <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl p-6">
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div 
            v-for="(count, intent) in summary?.intent_distribution || {}"
            :key="intent"
            class="text-center"
          >
            <div class="w-16 h-16 mx-auto mb-3 rounded-full flex items-center justify-center"
                 :class="getIntentColor(intent)">
              <span class="text-white font-bold">{{ count }}</span>
            </div>
            <p class="text-apple-body text-apple-sm font-medium">{{ intent }}</p>
            <p class="text-apple-caption text-apple-xs">
              {{ Math.round((count / totalSuggestions) * 100) }}%
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 商业洞察概览 -->
    <div class="mb-8" v-if="summaryStats">
      <h3 class="text-apple-title text-apple-lg mb-6">📊 商业洞察概览</h3>
      <div class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl p-6">
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4">
          <div class="text-center">
            <div class="text-apple-2xl font-bold text-blue-600">{{ summaryStats.unique_count || summaryStats.total_opportunities }}</div>
            <div class="text-apple-sm text-apple-caption">有效机会数</div>
          </div>
          <div class="text-center">
            <div class="text-apple-2xl font-bold text-cyan-600">{{ summaryStats.blue_ocean_count }}</div>
            <div class="text-apple-sm text-apple-caption">🌊 蓝海词</div>
          </div>
          <div class="text-center">
            <div class="text-apple-2xl font-bold text-green-600">{{ summaryStats.high_value_count }}</div>
            <div class="text-apple-sm text-apple-caption">💰 高价值</div>
          </div>
          <div class="text-center">
            <div class="text-apple-2xl font-bold text-red-600" v-if="summaryStats.duplicate_removed > 0">{{ summaryStats.duplicate_removed }}</div>
            <div class="text-apple-2xl font-bold text-purple-600" v-else>{{ summaryStats.avg_commercial_score }}</div>
            <div class="text-apple-sm text-apple-caption" v-if="summaryStats.duplicate_removed > 0">🧹 去重数量</div>
            <div class="text-apple-sm text-apple-caption" v-else>平均商业评分</div>
          </div>
          <div class="text-center">
            <div class="text-apple-2xl font-bold text-orange-600">{{ formatNumber(summaryStats.total_search_volume) }}</div>
            <div class="text-apple-sm text-apple-caption">总搜索量/月</div>
          </div>
        </div>
        
        <!-- 5118真实数据标识 -->
        <div class="flex items-center justify-center mb-4">
          <div class="inline-flex items-center px-4 py-2 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full text-apple-sm font-medium">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            基于5118真实市场数据分析
          </div>
        </div>
        
        <!-- 洞察信息 -->
        <div class="space-y-2" v-if="insightMessages.length > 0">
          <div 
            v-for="(insight, index) in insightMessages" 
            :key="index"
            class="text-apple-sm text-apple-body bg-white dark:bg-gray-600 rounded-lg px-3 py-2"
          >
            {{ insight }}
          </div>
        </div>
      </div>
    </div>

    <!-- 分层商业机会 -->
    <div v-if="Object.keys(opportunitiesByTier).length > 0">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-apple-title text-apple-lg">🎯 智能商机分层</h3>
        <div class="text-apple-sm text-apple-caption">
          按商业价值智能排序
        </div>
      </div>
      
      <!-- 分层展示 -->
      <div class="space-y-6">
        <div 
          v-for="(opportunities, tierName) in opportunitiesByTier" 
          :key="tierName"
          class="border border-gray-200 dark:border-gray-700 rounded-2xl overflow-hidden"
        >
          <!-- 分层标题 -->
          <div 
            class="px-6 py-4 cursor-pointer transition-all"
            :class="`bg-gradient-to-r ${getTierColor(tierName)} text-white`"
            @click="toggleTier(tierName)"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <span class="text-2xl">{{ getTierIcon(tierName) }}</span>
                <div>
                  <h4 class="text-apple-lg font-semibold">{{ tierName }}</h4>
                  <p class="text-apple-sm opacity-90">{{ opportunities.length }} 个关键词</p>
                </div>
              </div>
              <div class="flex items-center space-x-3">
                <el-tag class="bg-white/20 border-white/30 text-white">
                  {{ opportunities.length > 0 ? `平均评分 ${Math.round(opportunities.reduce((sum: number, opp: any) => sum + opp.opportunity_score, 0) / opportunities.length)}` : '暂无数据' }}
                </el-tag>
                <svg 
                  class="w-5 h-5 transition-transform duration-200"
                  :class="{ 'rotate-180': expandedTiers.includes(String(tierName)) }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </div>
          </div>
          
          <!-- 机会列表 -->
          <div v-show="expandedTiers.includes(String(tierName))" class="bg-white dark:bg-gray-800">
            <div class="p-6 space-y-4">
              <div
                v-for="(opportunity, index) in opportunities.slice(0, showAllOpportunities ? undefined : 5)"
                :key="opportunity.keyword"
                class="border border-gray-200 dark:border-gray-600 rounded-xl p-5 hover:shadow-md transition-all duration-200 hover:border-blue-300"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-3">
                      <span class="inline-flex items-center justify-center w-7 h-7 bg-gradient-to-r text-white text-apple-sm font-bold rounded-lg mr-3"
                            :class="getTierColor(tierName)">
                        {{ index + 1 }}
                      </span>
                      <h5 class="text-apple-title text-apple-base font-medium">{{ opportunity.keyword }}</h5>
                      <el-tag :type="getIntentTagType(opportunity.intent_type)" class="ml-3">
                        {{ opportunity.intent_type }}
                      </el-tag>
                      <el-tag v-if="opportunity.is_blue_ocean" type="info" class="ml-2">
                        🌊 蓝海词
                      </el-tag>
                    </div>
                    
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <!-- 机会评分 -->
                      <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-3">
                        <div class="flex items-center mb-1">
                          <span class="w-2 h-2 rounded-full mr-2" :class="getScoreStatusColor(opportunity.opportunity_score)"></span>
                          <p class="text-apple-xs font-medium text-apple-caption">机会评分</p>
                        </div>
                        <div class="flex items-baseline space-x-1">
                          <p class="text-apple-lg font-bold" :class="getScoreTextColor(opportunity.opportunity_score)">
                            {{ opportunity.opportunity_score }}
                          </p>
                          <span class="text-apple-xs text-apple-caption">/100</span>
                        </div>
                        <p class="text-apple-xs mt-1" :class="getScoreTextColor(opportunity.opportunity_score)">
                          {{ getScoreLevel(opportunity.opportunity_score) }}
                        </p>
                      </div>

                      <!-- 商业价值 -->
                      <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-3">
                        <div class="flex items-center mb-1">
                          <span class="w-2 h-2 rounded-full mr-2" :class="getScoreStatusColor(opportunity.commercial_score)"></span>
                          <p class="text-apple-xs font-medium text-apple-caption">商业价值</p>
                        </div>
                        <div class="flex items-baseline space-x-1">
                          <p class="text-apple-lg font-bold" :class="getScoreTextColor(opportunity.commercial_score)">
                            {{ opportunity.commercial_score }}
                          </p>
                          <span class="text-apple-xs text-apple-caption">/100</span>
                        </div>
                        <p class="text-apple-xs mt-1" :class="getScoreTextColor(opportunity.commercial_score)">
                          {{ getCommercialLevel(opportunity.commercial_score) }}
                        </p>
                      </div>

                      <!-- 预估搜索量 -->
                      <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-3">
                        <div class="flex items-center mb-1">
                          <svg class="w-3 h-3 mr-2 text-indigo-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                          </svg>
                          <p class="text-apple-xs font-medium text-apple-caption">预估搜索量</p>
                        </div>
                        <div class="flex items-baseline space-x-1">
                          <p class="text-apple-lg font-bold text-indigo-600">
                            {{ formatNumber(opportunity.search_volume_estimate) }}
                          </p>
                          <span class="text-apple-xs text-apple-caption">/月</span>
                        </div>
                        <p class="text-apple-xs mt-1 text-indigo-500">
                          5118真实数据
                        </p>
                      </div>

                      <!-- 机会指数 -->
                      <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-3">
                        <div class="flex items-center mb-1">
                          <svg class="w-3 h-3 mr-2 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                          </svg>
                          <p class="text-apple-xs font-medium text-apple-caption">机会指数</p>
                        </div>
                        <div class="flex items-baseline space-x-1 mb-2">
                          <p class="text-apple-lg font-bold text-emerald-600">
                            {{ opportunity.opportunity_score }}
                          </p>
                          <span class="text-apple-xs text-apple-caption">/100</span>
                        </div>
                        <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-1.5">
                          <div 
                            class="h-1.5 rounded-full transition-all duration-500 ease-out"
                            :class="getProgressBarColor(opportunity.opportunity_score)"
                            :style="{ width: `${Math.min(opportunity.opportunity_score, 100)}%` }"
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="ml-4">
                    <el-button size="small" type="primary" @click="copyKeyword(opportunity.keyword)">
                      复制关键词
                    </el-button>
                  </div>
                </div>
              </div>
              
              <!-- 显示更多按钮 -->
              <div v-if="opportunities.length > 5" class="text-center pt-4">
                <el-button @click="showAllOpportunities = !showAllOpportunities">
                  {{ showAllOpportunities ? '收起' : `显示全部 ${opportunities.length} 个` }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-else-if="loadingInsights" class="text-center py-12">
      <div class="relative">
        <!-- 主加载动画 -->
        <div class="w-16 h-16 mx-auto mb-6">
          <div class="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
        </div>
        
        <!-- 加载进度指示 -->
        <div class="mb-6">
          <div class="flex items-center justify-center mb-2">
            <svg class="w-5 h-5 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
            </svg>
            <h3 class="text-apple-lg font-medium text-apple-title">正在获取5118真实数据</h3>
          </div>
          <p class="text-apple-sm text-apple-caption mb-4">正在调用真实API进行商业价值分析，请稍候...</p>
          
          <!-- 加载步骤 -->
          <div class="max-w-md mx-auto space-y-2">
            <div class="flex items-center text-apple-sm">
              <div class="w-2 h-2 bg-green-500 rounded-full mr-3 animate-pulse"></div>
              <span class="text-apple-body">连接5118数据源</span>
            </div>
            <div class="flex items-center text-apple-sm">
              <div class="w-2 h-2 bg-blue-500 rounded-full mr-3 animate-pulse animation-delay-300"></div>
              <span class="text-apple-body">分析关键词商业价值</span>
            </div>
            <div class="flex items-center text-apple-sm">
              <div class="w-2 h-2 bg-purple-500 rounded-full mr-3 animate-pulse animation-delay-600"></div>
              <span class="text-apple-body">生成智能商业洞察</span>
            </div>
          </div>
        </div>
        
        <!-- 提示信息 -->
        <div class="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4 max-w-md mx-auto">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-blue-500 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
            <div class="text-apple-sm">
              <p class="text-blue-700 dark:text-blue-300 font-medium mb-1">数据获取中</p>
              <p class="text-blue-600 dark:text-blue-400 text-apple-xs">
                我们正在从5118获取真实市场数据，这比预估数据更准确但需要更多时间。感谢您的耐心等待！
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 无数据状态 -->
    <div v-else class="text-center py-12">
      <div v-if="businessInsights && businessInsights.insights_messages && businessInsights.insights_messages.length > 0">
        <!-- 有错误信息的情况 -->
        <div class="max-w-md mx-auto">
          <div class="w-16 h-16 mx-auto mb-4 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center">
            <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-apple-lg font-medium text-apple-title mb-4">数据获取失败</h3>
          <div class="space-y-2 mb-6">
            <div 
              v-for="(message, index) in businessInsights.insights_messages" 
              :key="index"
              class="text-apple-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-lg px-3 py-2"
            >
              {{ message }}
            </div>
          </div>
          <el-button type="primary" @click="fetchBusinessInsights">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            重试获取数据
          </el-button>
        </div>
      </div>
      <div v-else>
        <!-- 普通无数据状态 -->
        <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
        </div>
        <h3 class="text-apple-lg font-medium text-apple-caption mb-2">暂无商业分析数据</h3>
        <p class="text-apple-sm text-apple-caption">请先进行关键词分析以获取商业洞察</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { KeywordAnalysisResponse } from '@/types/api'
import { keywordApi } from '@/utils/api'

interface Props {
  analysisData?: KeywordAnalysisResponse
}

const props = defineProps<Props>()

// 数据
const showAllOpportunities = ref(false)
const businessInsights = ref<any>(null)
const loadingInsights = ref(false)
const expandedTiers = ref<string[]>(['蓝海机会', '高价值']) // 默认展开高价值分层

// 计算属性
const summary = computed(() => props.analysisData?.summary)

const topOpportunities = computed(() => 
  summary.value?.top_opportunities || []
)

const displayOpportunities = computed(() =>
  showAllOpportunities.value 
    ? topOpportunities.value
    : topOpportunities.value.slice(0, 5)
)

const totalSuggestions = computed(() => 
  summary.value?.total_suggestions || 0
)

const totalSearchVolume = computed(() =>
  topOpportunities.value.reduce((sum: number, opp: any) => sum + opp.search_volume_estimate, 0)
)

const primaryIntent = computed(() => {
  const distribution = summary.value?.intent_distribution || {}
  let maxCount = 0
  let primary = '混合型'
  
  Object.entries(distribution).forEach(([intent, count]) => {
    if (count > maxCount) {
      maxCount = count
      primary = intent
    }
  })
  
  return primary
})

// 新增：商业洞察相关计算属性
const opportunitiesByTier = computed(() => 
  businessInsights.value?.opportunities_by_tier || {}
)

const summaryStats = computed(() => 
  businessInsights.value?.summary_stats || {
    total_opportunities: 0,
    blue_ocean_count: 0,
    high_value_count: 0,
    avg_commercial_score: 0,
    total_search_volume: 0
  }
)

const insightMessages = computed(() => 
  businessInsights.value?.insights_messages || []
)

// 方法
const formatNumber = (num: number): string => {
  if (num >= 10000) {
    return `${Math.round(num / 1000) / 10}万`
  } else if (num >= 1000) {
    return `${Math.round(num / 100) / 10}千`
  }
  return num.toString()
}

// 新增：评分等级和颜色系统
const getScoreLevel = (score: number): string => {
  if (score >= 80) return '优质机会'
  if (score >= 60) return '较好机会'
  if (score >= 40) return '中等机会'
  if (score >= 20) return '较低机会'
  return '机会很小'
}

const getCommercialLevel = (score: number): string => {
  if (score >= 80) return '高商业价值'
  if (score >= 60) return '中等价值'
  if (score >= 40) return '一般价值'
  if (score >= 20) return '较低价值'
  return '价值很小'
}

const getScoreStatusColor = (score: number): string => {
  if (score >= 80) return 'bg-green-500'
  if (score >= 60) return 'bg-blue-500'
  if (score >= 40) return 'bg-yellow-500'
  if (score >= 20) return 'bg-orange-500'
  return 'bg-red-500'
}

const getScoreTextColor = (score: number): string => {
  if (score >= 80) return 'text-green-600'
  if (score >= 60) return 'text-blue-600'
  if (score >= 40) return 'text-yellow-600'
  if (score >= 20) return 'text-orange-600'
  return 'text-red-600'
}

const getProgressBarColor = (score: number): string => {
  if (score >= 80) return 'bg-gradient-to-r from-green-400 to-green-600'
  if (score >= 60) return 'bg-gradient-to-r from-blue-400 to-blue-600'
  if (score >= 40) return 'bg-gradient-to-r from-yellow-400 to-yellow-600'
  if (score >= 20) return 'bg-gradient-to-r from-orange-400 to-orange-600'
  return 'bg-gradient-to-r from-red-400 to-red-600'
}

const getIntentColor = (intent: string): string => {
  const colors: Record<string, string> = {
    '交易型': 'bg-red-500',
    '商业型': 'bg-orange-500', 
    '信息型': 'bg-blue-500',
    '导航型': 'bg-green-500',
    '混合型': 'bg-purple-500'
  }
  return colors[intent] || 'bg-gray-500'
}

const getIntentTagType = (intent: string): string => {
  const types: Record<string, string> = {
    '交易型': 'danger',
    '商业型': 'warning',
    '信息型': 'info', 
    '导航型': 'success',
    '混合型': ''
  }
  return types[intent] || ''
}

const copyKeyword = async (keyword: string) => {
  try {
    await navigator.clipboard.writeText(keyword)
    ElMessage.success('关键词已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败')
  }
}

// 新增：获取商业洞察数据
const fetchBusinessInsights = async () => {
  if (!props.analysisData?.session_id) return
  
  loadingInsights.value = true
  try {
    const response = await fetch(`/api/business-insights/${props.analysisData.session_id}`)
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    
    // 检查是否有错误信息
    if (data.error) {
      throw new Error(data.error)
    }
    
    businessInsights.value = data
    
    // 显示成功消息（如果是真实数据）
    const hasRealData = data.summary_stats?.total_opportunities > 0
    if (hasRealData) {
      ElMessage.success({
        message: '🎯 5118真实数据分析完成！已获取最新市场洞察',
        duration: 3000
      })
    }
    
  } catch (error) {
    console.error('获取商业洞察失败:', error)
    
    // 优雅的错误处理 - 不退回到假数据，而是显示明确的错误状态
    businessInsights.value = {
      summary_stats: {
        total_opportunities: 0,
        blue_ocean_count: 0,
        high_value_count: 0,
        avg_commercial_score: 0,
        total_search_volume: 0
      },
      insights_messages: [
        '⚠️ 5118数据获取失败，请稍后重试',
        `错误详情: ${error instanceof Error ? error.message : String(error)}`
      ],
      opportunities_by_tier: {}
    }
    
    ElMessage.error({
      message: '获取5118真实数据失败，请检查网络连接后重试',
      duration: 5000
    })
  } finally {
    loadingInsights.value = false
  }
}

// 分层展示控制
const toggleTier = (tierName: string | number) => {
  const tierKey = String(tierName)
  const index = expandedTiers.value.indexOf(tierKey)
  if (index > -1) {
    expandedTiers.value.splice(index, 1)
  } else {
    expandedTiers.value.push(tierKey)
  }
}

const getTierIcon = (tierName: string | number): string => {
  const tierKey = String(tierName)
  const icons: Record<string, string> = {
    '蓝海机会': '🌊',
    '高价值': '💰',
    '热门机会': '🔥',
    '潜力词': '📈',
    '一般建议': '⚪'
  }
  return icons[tierKey] || '📊'
}

const getTierColor = (tierName: string | number): string => {
  const tierKey = String(tierName)
  const colors: Record<string, string> = {
    '蓝海机会': 'from-blue-500 to-cyan-500',
    '高价值': 'from-green-500 to-emerald-500',
    '热门机会': 'from-orange-500 to-red-500',
    '潜力词': 'from-purple-500 to-pink-500',
    '一般建议': 'from-gray-400 to-gray-500'
  }
  return colors[tierKey] || 'from-gray-400 to-gray-500'
}

// 监听数据变化
watch(() => props.analysisData?.session_id, (newSessionId) => {
  if (newSessionId) {
    fetchBusinessInsights()
  }
}, { immediate: true })
</script>

<style scoped>
.apple-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-card:hover {
  transform: translateY(-2px);
}

/* 动画延迟类 */
.animation-delay-300 {
  animation-delay: 300ms;
}

.animation-delay-600 {
  animation-delay: 600ms;
}

/* 优化的加载动画 */
@keyframes pulse-subtle {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse-subtle {
  animation: pulse-subtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>