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

    <!-- 最佳商业机会 -->
    <div>
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-apple-title text-apple-lg">🎯 最佳商业机会</h3>
        <el-switch 
          v-model="showAllOpportunities"
          active-text="显示全部"
          inactive-text="仅显示前5个"
        />
      </div>
      
      <div class="space-y-4">
        <div
          v-for="(opportunity, index) in displayOpportunities"
          :key="opportunity.keyword"
          class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-6 hover:shadow-lg transition-all duration-200"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center mb-3">
                <span class="inline-flex items-center justify-center w-8 h-8 bg-blue-500 text-white text-apple-sm font-bold rounded-lg mr-3">
                  {{ index + 1 }}
                </span>
                <h4 class="text-apple-title text-apple-lg font-medium">{{ opportunity.keyword }}</h4>
                <el-tag :type="getIntentTagType(opportunity.intent_type)" class="ml-3">
                  {{ opportunity.intent_type }}
                </el-tag>
              </div>
              
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="text-center">
                  <p class="text-apple-caption text-apple-xs">机会评分</p>
                  <p class="text-apple-title text-apple-lg font-bold text-green-600">
                    {{ opportunity.opportunity_score }}
                  </p>
                </div>
                <div class="text-center">
                  <p class="text-apple-caption text-apple-xs">商业价值</p>
                  <p class="text-apple-title text-apple-lg font-bold text-blue-600">
                    {{ opportunity.commercial_score }}
                  </p>
                </div>
                <div class="text-center">
                  <p class="text-apple-caption text-apple-xs">预估搜索量</p>
                  <p class="text-apple-title text-apple-lg font-bold text-purple-600">
                    {{ formatNumber(opportunity.search_volume_estimate) }}
                  </p>
                </div>
                <div class="text-center">
                  <p class="text-apple-caption text-apple-xs">机会指数</p>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-1">
                    <div 
                      class="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${opportunity.opportunity_score}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="ml-6">
              <el-button size="small" type="primary" @click="copyKeyword(opportunity.keyword)">
                复制关键词
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { KeywordAnalysisResponse } from '@/types/api'

interface Props {
  analysisData?: KeywordAnalysisResponse
}

const props = defineProps<Props>()

// 数据
const showAllOpportunities = ref(false)

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
  topOpportunities.value.reduce((sum, opp) => sum + opp.search_volume_estimate, 0)
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

// 方法
const formatNumber = (num: number): string => {
  if (num >= 10000) {
    return `${Math.round(num / 1000) / 10}万`
  } else if (num >= 1000) {
    return `${Math.round(num / 100) / 10}千`
  }
  return num.toString()
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
</script>

<style scoped>
.apple-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-card:hover {
  transform: translateY(-2px);
}
</style>