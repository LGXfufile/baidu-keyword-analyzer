<template>
  <div class="glass-card p-6 animate-fade-in">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold flex items-center">
        <svg class="w-6 h-6 mr-2 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        分析结果
      </h2>
      
      <div class="flex items-center space-x-3">
        <el-dropdown @command="exportData">
          <el-button type="primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-4-4m4 4l4-4m-6 4V5"/>
            </svg>
            导出数据
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="excel">
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4zm0 2h12v12H4V4z"/>
                </svg>
                Excel格式
              </el-dropdown-item>
              <el-dropdown-item command="csv">
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4zm0 2h12v12H4V4z"/>
                </svg>
                CSV格式
              </el-dropdown-item>
              <el-dropdown-item command="json">
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4zm0 2h12v12H4V4z"/>
                </svg>
                JSON格式
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        
        <el-button @click="refreshData">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
      <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-lg">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-blue-100 text-sm">总建议词</p>
            <p class="text-2xl font-bold">{{ totalSuggestions }}</p>
          </div>
          <svg class="w-8 h-8 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
          </svg>
        </div>
      </div>
      
      <div class="bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-lg">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-green-100 text-sm">成功变体</p>
            <p class="text-2xl font-bold">{{ currentAnalysis?.summary.successful_variants || 0 }}</p>
          </div>
          <svg class="w-8 h-8 text-green-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
      </div>
      
      <div class="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-4 rounded-lg">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-orange-100 text-sm">失败变体</p>
            <p class="text-2xl font-bold">{{ currentAnalysis?.summary.failed_variants || 0 }}</p>
          </div>
          <svg class="w-8 h-8 text-orange-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
      </div>
      
      <div class="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-4 rounded-lg">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-purple-100 text-sm">成功率</p>
            <p class="text-2xl font-bold">{{ successRate }}%</p>
          </div>
          <svg class="w-8 h-8 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
          </svg>
        </div>
      </div>
      
      <div class="bg-gradient-to-r from-indigo-500 to-indigo-600 text-white p-4 rounded-lg">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-indigo-100 text-sm">去重数量</p>
            <p class="text-2xl font-bold">{{ currentAnalysis?.summary.duplicate_removed || 0 }}</p>
          </div>
          <svg class="w-8 h-8 text-indigo-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
      </div>
      
      <div class="bg-gradient-to-r from-teal-500 to-teal-600 text-white p-4 rounded-lg">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-teal-100 text-sm">唯一建议词</p>
            <p class="text-2xl font-bold">{{ currentAnalysis?.summary.unique_suggestions || 0 }}</p>
          </div>
          <svg class="w-8 h-8 text-teal-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 结果展示 -->
    <div class="space-y-6">
      <!-- 视图切换 -->
      <div class="flex items-center justify-between">
        <el-radio-group v-model="viewMode" size="large">
          <el-radio-button label="tree">树形视图</el-radio-button>
          <el-radio-button label="table">表格视图</el-radio-button>
          <el-radio-button label="chart">图表视图</el-radio-button>
        </el-radio-group>
        
        <el-input
          v-model="searchQuery"
          placeholder="搜索关键词..."
          style="width: 200px"
          clearable
        >
          <template #prefix>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </template>
        </el-input>
      </div>

      <!-- 树形视图 -->
      <div v-if="viewMode === 'tree'" class="space-y-4">
        <div
          v-for="(variants, variantType) in filteredResults"
          :key="variantType"
          class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
        >
          <div 
            class="bg-gray-50 dark:bg-gray-800 px-4 py-3 flex items-center justify-between cursor-pointer"
            @click="toggleExpanded(variantType)"
          >
            <div class="flex items-center">
              <svg 
                class="w-4 h-4 mr-2 transition-transform"
                :class="{ 'rotate-90': expandedTypes.includes(variantType) }"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
              <span class="font-medium">{{ getVariantTypeName(variantType) }}</span>
              <el-badge :value="getVariantCount(variants)" class="ml-2" />
            </div>
            <el-button size="small" @click.stop="copyVariantData(variantType, variants)">
              复制全部
            </el-button>
          </div>
          
          <div v-show="expandedTypes.includes(variantType)" class="p-4 space-y-3">
            <div
              v-for="(suggestions, variantKeyword) in variants"
              :key="variantKeyword"
              class="pl-4 border-l-2 border-gray-200 dark:border-gray-700"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-primary-600 dark:text-primary-400">
                  {{ variantKeyword }}
                </span>
                <div class="flex items-center space-x-2">
                  <el-badge :value="suggestions.length" type="info" />
                  <el-button size="small" @click="copySuggestions(suggestions)">
                    复制
                  </el-button>
                </div>
              </div>
              <div class="flex flex-wrap gap-2">
                <el-tag
                  v-for="(suggestion, index) in suggestions"
                  :key="index"
                  class="cursor-pointer hover-lift"
                  @click="copyToClipboard(suggestion)"
                >
                  {{ suggestion }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 表格视图 -->
      <div v-else-if="viewMode === 'table'">
        <el-table :data="tableData" style="width: 100%" stripe>
          <el-table-column prop="variantType" label="变体类型" width="150">
            <template #default="{ row }">
              <el-tag type="primary">{{ getVariantTypeName(row.variantType) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="variantKeyword" label="变体关键词" width="200" />
          <el-table-column prop="suggestion" label="下拉建议词" />
          <el-table-column prop="rank" label="排序" width="80" align="center" />
          <el-table-column label="操作" width="100" align="center">
            <template #default="{ row }">
              <el-button size="small" @click="copyToClipboard(row.suggestion)">
                复制
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 图表视图 -->
      <div v-else-if="viewMode === 'chart'">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- 变体类型分布 -->
          <div class="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium mb-4">变体类型分布</h3>
            <v-chart :option="pieChartOption" style="height: 300px" />
          </div>
          
          <!-- 词云图 -->
          <div class="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium mb-4">高频词汇</h3>
            <v-chart :option="wordCloudOption" style="height: 300px" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { storeToRefs } from 'pinia'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { useKeywordStore } from '@/stores/keyword'
import { keywordApi } from '@/utils/api'
import { downloadFile, copyToClipboard, calculateWordFrequency } from '@/utils'

// 注册ECharts组件
use([
  CanvasRenderer,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

// Store
const keywordStore = useKeywordStore()
const { currentAnalysis, variantTypes, totalSuggestions, successRate } = storeToRefs(keywordStore)

// 数据
const viewMode = ref('tree')
const searchQuery = ref('')
const expandedTypes = ref<string[]>([])

// 计算属性
const filteredResults = computed(() => {
  if (!currentAnalysis.value?.results) return {}
  
  const results = currentAnalysis.value.results
  if (!searchQuery.value) return results
  
  const filtered: Record<string, Record<string, string[]>> = {}
  
  Object.entries(results).forEach(([variantType, variants]) => {
    const filteredVariants: Record<string, string[]> = {}
    
    Object.entries(variants).forEach(([variantKeyword, suggestions]) => {
      const matchingSuggestions = suggestions.filter(suggestion =>
        suggestion.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        variantKeyword.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
      
      if (matchingSuggestions.length > 0) {
        filteredVariants[variantKeyword] = matchingSuggestions
      }
    })
    
    if (Object.keys(filteredVariants).length > 0) {
      filtered[variantType] = filteredVariants
    }
  })
  
  return filtered
})

const tableData = computed(() => {
  const data: Array<{
    variantType: string
    variantKeyword: string
    suggestion: string
    rank: number
  }> = []
  
  Object.entries(filteredResults.value).forEach(([variantType, variants]) => {
    Object.entries(variants).forEach(([variantKeyword, suggestions]) => {
      suggestions.forEach((suggestion, index) => {
        data.push({
          variantType,
          variantKeyword,
          suggestion,
          rank: index + 1
        })
      })
    })
  })
  
  return data
})

const pieChartOption = computed(() => {
  const data = Object.entries(filteredResults.value).map(([variantType, variants]) => ({
    name: getVariantTypeName(variantType),
    value: getVariantCount(variants)
  }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '建议词数量',
        type: 'pie',
        radius: '50%',
        data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
})

const wordCloudOption = computed(() => {
  const allSuggestions: string[] = []
  
  Object.values(filteredResults.value).forEach(variants => {
    Object.values(variants).forEach(suggestions => {
      allSuggestions.push(...suggestions)
    })
  })
  
  const frequency = calculateWordFrequency(allSuggestions)
  const data = Object.entries(frequency)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 20)
    .map(([word, freq]) => ({ name: word, value: freq }))
  
  return {
    tooltip: {
      formatter: '{b}: {c}'
    },
    series: [{
      type: 'wordCloud',
      gridSize: 2,
      sizeRange: [12, 50],
      rotationRange: [-90, 90],
      shape: 'pentagon',
      width: '100%',
      height: '100%',
      data
    }]
  }
})

// 方法
const getVariantTypeName = (type: string): string => {
  return variantTypes.value[type] || type
}

const getVariantCount = (variants: Record<string, string[]>): number => {
  return Object.values(variants).reduce((total, suggestions) => total + suggestions.length, 0)
}

const toggleExpanded = (variantType: string) => {
  const index = expandedTypes.value.indexOf(variantType)
  if (index > -1) {
    expandedTypes.value.splice(index, 1)
  } else {
    expandedTypes.value.push(variantType)
  }
}

const copyVariantData = async (variantType: string, variants: Record<string, string[]>) => {
  const text = Object.entries(variants)
    .map(([keyword, suggestions]) => `${keyword}: ${suggestions.join(', ')}`)
    .join('\n')
  
  const success = await copyToClipboard(text)
  if (success) {
    ElMessage.success('已复制到剪贴板')
  } else {
    ElMessage.error('复制失败')
  }
}

const copySuggestions = async (suggestions: string[]) => {
  const success = await copyToClipboard(suggestions.join('\n'))
  if (success) {
    ElMessage.success('已复制到剪贴板')
  } else {
    ElMessage.error('复制失败')
  }
}

const exportData = async (format: string) => {
  if (!currentAnalysis.value?.session_id) {
    ElMessage.error('没有可导出的数据')
    return
  }
  
  try {
    const blob = await keywordApi.exportResults({
      session_id: currentAnalysis.value.session_id,
      format: format as 'excel' | 'csv' | 'json'
    })
    
    const filename = `keywords_${currentAnalysis.value.session_id}.${format === 'excel' ? 'xlsx' : format}`
    downloadFile(blob, filename)
    
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const refreshData = async () => {
  if (!currentAnalysis.value?.session_id) return
  
  try {
    const result = await keywordApi.getSessionResults(currentAnalysis.value.session_id)
    keywordStore.setCurrentAnalysis(result)
    ElMessage.success('数据已刷新')
  } catch (error) {
    ElMessage.error('刷新失败')
  }
}

onMounted(() => {
  // 默认展开第一个变体类型
  if (currentAnalysis.value?.results) {
    const firstType = Object.keys(currentAnalysis.value.results)[0]
    if (firstType) {
      expandedTypes.value.push(firstType)
    }
  }
})
</script>