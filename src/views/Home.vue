<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Apple-style Navigation -->
    <nav class="nav-apple">
      <div class="container-apple">
        <div class="flex items-center justify-between py-4">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-blue-500 rounded-2xl flex items-center justify-center shadow-apple">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <div>
              <h1 class="text-apple-2xl font-semibold text-apple-title tracking-tight">百度关键词分析器</h1>
              <p class="text-apple-sm text-apple-caption mt-1">智能挖掘下拉词，发现长尾机会</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-3">
            <button 
              @click="toggleTheme"
              class="btn-apple-secondary w-11 h-11 !p-0 rounded-full interactive-apple"
            >
              <svg v-if="isDark" class="w-5 h-5 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
              <svg v-else class="w-5 h-5 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
              </svg>
            </button>
            <button 
              @click="showHistory = true"
              class="btn-apple-primary"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              历史记录
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container-apple section-apple">
      <!-- Keyword Configuration Section -->
      <div class="apple-card p-8 animate-apple-enter">
        <div class="flex items-center mb-8">
          <div class="w-8 h-8 bg-blue-500/10 rounded-xl flex items-center justify-center mr-4">
            <svg class="w-5 h-5 text-apple-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <div>
            <h2 class="text-apple-title text-apple-2xl">关键词配置</h2>
            <p class="text-apple-caption text-apple-sm mt-1">设置目标关键词和变体类型</p>
          </div>
        </div>
        
        <div class="grid-apple lg:grid-cols-3 gap-8">
          <!-- Keyword Input -->
          <div class="lg:col-span-1 space-y-3">
            <label class="block text-apple-body text-apple-base font-medium">目标关键词</label>
            <div class="relative">
              <input
                v-model="keyword"
                placeholder="请输入要分析的关键词"
                class="input-apple w-full pl-12"
                :disabled="analyzing"
              />
              <div class="absolute left-4 top-1/2 transform -translate-y-1/2">
                <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
              </div>
            </div>
          </div>
          
          <!-- Variant Types Selection -->
          <div class="lg:col-span-2 space-y-4">
            <label class="block text-apple-body text-apple-base font-medium">变体类型</label>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <label class="flex items-center p-4 apple-card cursor-pointer interactive-apple">
                <input
                  type="checkbox"
                  value="alpha"
                  v-model="selectedTypes"
                  :disabled="analyzing"
                  class="sr-only"
                />
                <div class="flex-shrink-0 w-5 h-5 rounded-md border-2 border-gray-200 dark:border-gray-600 mr-3 flex items-center justify-center"
                     :class="selectedTypes.includes('alpha') ? 'bg-blue-500 border-apple-blue-500' : ''">
                  <svg v-if="selectedTypes.includes('alpha')" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <div class="text-apple-body text-apple-base font-medium">字母后缀</div>
                  <div class="text-apple-caption text-apple-sm">(a-z)</div>
                </div>
              </label>
              
              <label class="flex items-center p-4 apple-card cursor-pointer interactive-apple">
                <input
                  type="checkbox"
                  value="alpha_space"
                  v-model="selectedTypes"
                  :disabled="analyzing"
                  class="sr-only"
                />
                <div class="flex-shrink-0 w-5 h-5 rounded-md border-2 border-gray-200 dark:border-gray-600 mr-3 flex items-center justify-center"
                     :class="selectedTypes.includes('alpha_space') ? 'bg-blue-500 border-apple-blue-500' : ''">
                  <svg v-if="selectedTypes.includes('alpha_space')" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <div class="text-apple-body text-apple-base font-medium">字母前缀带空格</div>
                  <div class="text-apple-caption text-apple-sm">(a-z)</div>
                </div>
              </label>

              <label class="flex items-center p-4 apple-card cursor-pointer interactive-apple">
                <input
                  type="checkbox"
                  value="question_how"
                  v-model="selectedTypes"
                  :disabled="analyzing"
                  class="sr-only"
                />
                <div class="flex-shrink-0 w-5 h-5 rounded-md border-2 border-gray-200 dark:border-gray-600 mr-3 flex items-center justify-center"
                     :class="selectedTypes.includes('question_how') ? 'bg-blue-500 border-apple-blue-500' : ''">
                  <svg v-if="selectedTypes.includes('question_how')" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <div class="text-apple-body text-apple-base font-medium">疑问词-怎么</div>
                  <div class="text-apple-caption text-apple-sm">(怎么-z)</div>
                </div>
              </label>

              <label class="flex items-center p-4 apple-card cursor-pointer interactive-apple">
                <input
                  type="checkbox"
                  value="question_what"
                  v-model="selectedTypes"
                  :disabled="analyzing"
                  class="sr-only"
                />
                <div class="flex-shrink-0 w-5 h-5 rounded-md border-2 border-gray-200 dark:border-gray-600 mr-3 flex items-center justify-center"
                     :class="selectedTypes.includes('question_what') ? 'bg-blue-500 border-apple-blue-500' : ''">
                  <svg v-if="selectedTypes.includes('question_what')" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <div class="text-apple-body text-apple-base font-medium">疑问词-什么</div>
                  <div class="text-apple-caption text-apple-sm">(什么-z)</div>
                </div>
              </label>

              <label class="flex items-center p-4 apple-card cursor-pointer interactive-apple">
                <input
                  type="checkbox"
                  value="question_can"
                  v-model="selectedTypes"
                  :disabled="analyzing"
                  class="sr-only"
                />
                <div class="flex-shrink-0 w-5 h-5 rounded-md border-2 border-gray-200 dark:border-gray-600 mr-3 flex items-center justify-center"
                     :class="selectedTypes.includes('question_can') ? 'bg-blue-500 border-apple-blue-500' : ''">
                  <svg v-if="selectedTypes.includes('question_can')" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <div class="text-apple-body text-apple-base font-medium">疑问词-能</div>
                  <div class="text-apple-caption text-apple-sm">(能-z)</div>
                </div>
              </label>

              <label class="flex items-center p-4 apple-card cursor-pointer interactive-apple">
                <input
                  type="checkbox"
                  value="question_which"
                  v-model="selectedTypes"
                  :disabled="analyzing"
                  class="sr-only"
                />
                <div class="flex-shrink-0 w-5 h-5 rounded-md border-2 border-gray-200 dark:border-gray-600 mr-3 flex items-center justify-center"
                     :class="selectedTypes.includes('question_which') ? 'bg-blue-500 border-apple-blue-500' : ''">
                  <svg v-if="selectedTypes.includes('question_which')" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <div class="text-apple-body text-apple-base font-medium">疑问词-哪</div>
                  <div class="text-apple-caption text-apple-sm">(哪-z)</div>
                </div>
              </label>
            </div>
          </div>
        </div>
        
        <!-- Action Button -->
        <div class="flex justify-center mt-10">
          <button
            :disabled="!keyword || selectedTypes.length === 0 || analyzing"
            @click="startAnalysis"
            class="btn-apple-primary px-10 py-4 text-apple-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div v-if="analyzing" class="flex items-center">
              <div class="loading-apple w-5 h-5 mr-3">
                <svg class="w-5 h-5" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <span>分析中{{ progress ? `(${progress.percentage}%)` : '' }}</span>
            </div>
            <div v-else class="flex items-center">
              <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              开始分析
            </div>
          </button>
        </div>
      </div>

      <!-- Progress Indicator -->
      <div v-if="analyzing && progress" class="apple-card p-6 animate-apple-slide-up">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-blue-500/10 rounded-xl flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-apple-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-apple-title text-apple-lg">分析进度</h3>
              <p class="text-apple-caption text-apple-sm">{{ progress.processed }}/{{ progress.total }} 个变体已完成</p>
            </div>
          </div>
          <div class="text-apple-title text-apple-2xl font-semibold">{{ progress.percentage }}%</div>
        </div>
        <div class="progress-apple h-2">
          <div 
            class="progress-apple-bar" 
            :style="{ width: `${progress.percentage}%` }"
          ></div>
        </div>
      </div>

      <!-- Analysis Results -->
      <AnalysisResults v-if="hasCurrentAnalysis" class="animate-apple-slide-up" />
    </div>

    <!-- History Dialog -->
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
    console.log('开始加载变体类型...')
    const response = await keywordApi.getVariantTypes()
    console.log('API响应:', response)
    
    // 确保我们获取到正确的数据结构
    const variantTypesData = response.variant_types || response
    console.log('解析出的变体类型:', variantTypesData)
    
    // 强制更新store
    keywordStore.setVariantTypes(variantTypesData as VariantTypes)
    console.log('Store更新后的变体类型:', variantTypes.value)
  } catch (error) {
    console.error('加载变体类型失败:', error)
    // 设置默认变体类型
    const defaultTypes: VariantTypes = {
      'alpha': '字母后缀 (a-z)',
      'alpha_space': '字母前缀带空格 (a-z)',
      'question_how': '疑问词-怎么 (怎么-z)',
      'question_what': '疑问词-什么 (什么-z)',
      'question_can': '疑问词-能 (能-z)',
      'question_which': '疑问词-哪 (哪-z)'
    }
    keywordStore.setVariantTypes(defaultTypes)
    ElMessage.error('加载变体类型失败，使用默认配置')
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
    keywordStore.setProgress({ 
      percentage: 0, 
      current: 0, 
      total: 0, 
      message: '🚀 正在启动分析引擎...',
      status: 'starting'
    })
    
    ElMessage.info({
      message: '🔍 开始分析关键词，这可能需要1-2分钟，请耐心等待...',
      duration: 4000
    })
    
    const result = await keywordApi.analyzeKeyword({
      keyword: keyword.value,
      variant_types: selectedTypes.value
    })
    
    keywordStore.setCurrentAnalysis(result)
    
    // 开始轮询进度 - 不要在这里设置为完成状态
    startProgressPolling(result.session_id)
    
    // 删除这里的成功消息，让轮询来处理
    
  } catch (error) {
    keywordStore.setAnalyzing(false)
    
    // 更详细的错误处理
    let message = '分析失败'
    if (error instanceof Error) {
      if (error.message.includes('timeout')) {
        message = '请求超时，请检查网络连接或稍后重试'
      } else if (error.message.includes('Network Error')) {
        message = '网络连接失败，请检查网络状态'
      } else if (error.message.includes('canceled')) {
        message = '请求被取消，可能是网络不稳定'
      } else {
        message = error.message
      }
    }
    
    ElMessage.error({
      message: `❌ ${message}`,
      duration: 6000
    })
    keywordStore.setError(message)
  }
}

const startProgressPolling = (sessionId: string) => {
  if (progressTimer) {
    clearInterval(progressTimer)
  }
  
  let pollCount = 0
  const maxPolls = 300 // 最多轮询5分钟 (300 * 1000ms)
  
  progressTimer = setInterval(async () => {
    try {
      pollCount++
      const progressData = await keywordApi.getProgress(sessionId)
      keywordStore.setProgress(progressData)
      
      // 检查完成状态
      if (progressData.status === 'completed') {
        clearInterval(progressTimer!)
        progressTimer = null
        keywordStore.setAnalyzing(false)
        ElMessage.success({
          message: '🎉 关键词分析完成！正在加载商业洞察数据...',
          duration: 3000
        })
        return
      }
      
      // 检查错误状态
      if (progressData.status === 'error' || progressData.status === 'failed') {
        clearInterval(progressTimer!)
        progressTimer = null
        keywordStore.setAnalyzing(false)
        const errorMsg = progressData.error || progressData.message || '未知错误'
        ElMessage.error({
          message: `❌ 分析失败: ${errorMsg}`,
          duration: 6000
        })
        keywordStore.setError(errorMsg)
        return
      }
      
      // 检查会话不存在
      if (progressData.status === 'not_found') {
        clearInterval(progressTimer!)
        progressTimer = null
        keywordStore.setAnalyzing(false)
        ElMessage.error({
          message: '❌ 分析会话不存在，请重新开始分析',
          duration: 4000
        })
        return
      }
      
      // 超时保护
      if (pollCount >= maxPolls) {
        clearInterval(progressTimer!)
        progressTimer = null
        keywordStore.setAnalyzing(false)
        ElMessage.error({
          message: '⏰ 分析超时，可能是5118 API限制导致，请稍后重试',
          duration: 8000
        })
        keywordStore.setError('分析超时 - 可能遇到API速率限制，请稍后重试')
        return
      }
      
      // 更新进度消息
      if (progressData.message) {
        keywordStore.setProgress({
          ...progressData,
          message: `🔄 ${progressData.message} (${pollCount}s)`
        })
      }
      
      // 定期显示进度提醒
      if (pollCount % 30 === 0) { // 每30秒提醒一次
        ElMessage.info({
          message: `⏳ 正在分析中...已用时${pollCount}秒，请继续等待`,
          duration: 2000
        })
      }
      
      // 兼容旧版本：基于百分比判断完成
      if (progressData.percentage >= 100 && progressData.status !== 'running') {
        clearInterval(progressTimer!)
        progressTimer = null
        keywordStore.setAnalyzing(false)
        ElMessage.success({
          message: '🎉 分析完成！',
          duration: 3000
        })
      }
      
    } catch (error) {
      console.error('轮询进度失败:', error)
      
      // 网络错误重试逻辑
      if (pollCount < 5) {
        console.log(`网络错误，将在第${pollCount}次重试...`)
        return // 继续轮询而不停止
      }
      
      clearInterval(progressTimer!)
      progressTimer = null
      keywordStore.setAnalyzing(false)
      ElMessage.error({
        message: '❌ 网络连接失败，无法获取分析进度，请检查网络后重试',
        duration: 6000
      })
      keywordStore.setError('网络连接失败')
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