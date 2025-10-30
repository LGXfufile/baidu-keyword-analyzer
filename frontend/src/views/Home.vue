<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- 导航栏 -->
    <nav class="glass-card m-4 mb-6">
      <div class="flex items-center justify-between p-4">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          <div>
            <h1 class="text-xl font-bold text-gradient">百度关键词分析器</h1>
            <p class="text-sm text-gray-500 dark:text-gray-400">智能挖掘下拉词，发现长尾机会</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-3">
          <el-button 
            @click="toggleTheme"
            circle
            size="large"
          >
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </el-button>
          <el-button 
            type="primary" 
            @click="showHistory = true"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            历史记录
          </el-button>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="container mx-auto px-4 space-y-6">
      <!-- 搜索配置区 -->
      <div class="glass-card p-6 animate-fade-in">
        <h2 class="text-lg font-semibold mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          关键词配置
        </h2>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- 关键词输入 -->
          <div class="lg:col-span-1">
            <label class="block text-sm font-medium mb-2">目标关键词</label>
            <el-input
              v-model="keyword"
              placeholder="请输入要分析的关键词"
              size="large"
              clearable
              :disabled="analyzing"
            >
              <template #prefix>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
              </template>
            </el-input>
          </div>
          
          <!-- 变体类型选择 -->
          <div class="lg:col-span-2">
            <label class="block text-sm font-medium mb-2">变体类型</label>
            <el-checkbox-group v-model="selectedTypes" :disabled="analyzing">
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <el-checkbox
                  v-for="(label, key) in variantTypes"
                  :key="key"
                  :label="key"
                  class="!mr-0"
                >
                  <span class="text-sm">{{ label }}</span>
                </el-checkbox>
              </div>
            </el-checkbox-group>
          </div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="flex justify-center mt-6">
          <el-button
            type="primary"
            size="large"
            :loading="analyzing"
            :disabled="!keyword || selectedTypes.length === 0"
            @click="startAnalysis"
            class="px-8"
          >
            <template #loading>
              <div class="flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                分析中{{ progress ? `(${progress.percentage}%)` : '' }}
              </div>
            </template>
            <template #default>
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              开始分析
            </template>
          </el-button>
        </div>
      </div>

      <!-- 进度条 -->
      <div v-if="analyzing && progress" class="glass-card p-4 animate-slide-up">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium">分析进度</span>
          <span class="text-sm text-gray-500">{{ progress.processed }}/{{ progress.total }}</span>
        </div>
        <el-progress 
          :percentage="progress.percentage" 
          :stroke-width="8"
          :show-text="false"
        />
      </div>

      <!-- 分析结果 -->
      <AnalysisResults v-if="hasCurrentAnalysis" />
    </div>

    <!-- 历史记录弹窗 -->
    <SearchHistoryDialog v-model:visible="showHistory" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { storeToRefs } from 'pinia'
import { useKeywordStore } from '@/stores/keyword'
import { useThemeStore } from '@/stores/theme'
import { keywordApi } from '@/utils/api'
import AnalysisResults from '@/components/AnalysisResults.vue'
import SearchHistoryDialog from '@/components/SearchHistoryDialog.vue'
import type { VariantTypes } from '@/types/api'

// Store
const keywordStore = useKeywordStore()
const themeStore = useThemeStore()

const { 
  analyzing, 
  variantTypes, 
  progress, 
  hasCurrentAnalysis 
} = storeToRefs(keywordStore)

const { isDark } = storeToRefs(themeStore)

// 数据
const keyword = ref('')
const selectedTypes = ref<string[]>(['alpha', 'question_how'])
const showHistory = ref(false)
let progressTimer: number | null = null

// 方法
const { toggleTheme } = themeStore

const loadVariantTypes = async () => {
  try {
    const types = await keywordApi.getVariantTypes()
    keywordStore.setVariantTypes(types as VariantTypes)
  } catch (error) {
    ElMessage.error('加载变体类型失败')
  }
}

const startAnalysis = async () => {
  if (!keyword.value || selectedTypes.value.length === 0) {
    ElMessage.warning('请输入关键词并选择变体类型')
    return
  }

  try {
    keywordStore.setAnalyzing(true)
    keywordStore.clearError()
    
    const result = await keywordApi.analyzeKeyword({
      keyword: keyword.value,
      variant_types: selectedTypes.value
    })
    
    keywordStore.setCurrentAnalysis(result)
    
    // 开始轮询进度
    startProgressPolling(result.session_id)
    
    ElMessage.success('分析完成！')
  } catch (error) {
    const message = error instanceof Error ? error.message : '分析失败'
    ElMessage.error(message)
    keywordStore.setError(message)
  } finally {
    keywordStore.setAnalyzing(false)
  }
}

const startProgressPolling = (sessionId: string) => {
  if (progressTimer) {
    clearInterval(progressTimer)
  }
  
  progressTimer = setInterval(async () => {
    try {
      const progressData = await keywordApi.getProgress(sessionId)
      keywordStore.setProgress(progressData)
      
      if (progressData.percentage >= 100) {
        clearInterval(progressTimer!)
        progressTimer = null
      }
    } catch (error) {
      clearInterval(progressTimer!)
      progressTimer = null
    }
  }, 1000)
}

onMounted(() => {
  themeStore.initTheme()
  loadVariantTypes()
})

onUnmounted(() => {
  if (progressTimer) {
    clearInterval(progressTimer)
  }
})
</script>