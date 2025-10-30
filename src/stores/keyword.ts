import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { 
  KeywordAnalysisResponse, 
  SearchHistory, 
  VariantTypes,
  ProgressUpdate 
} from '@/types/api'

export const useKeywordStore = defineStore('keyword', () => {
  // 状态
  const loading = ref(false)
  const analyzing = ref(false)
  const currentAnalysis = ref<KeywordAnalysisResponse | null>(null)
  const searchHistory = ref<SearchHistory[]>([])
  const variantTypes = ref<VariantTypes>({
    'alpha': '字母后缀 (a-z)',
    'alpha_space': '字母前缀带空格 (a-z)',
    'question_how': '疑问词-怎么 (怎么-z)',
    'question_what': '疑问词-什么 (什么-z)',
    'question_can': '疑问词-能 (能-z)',
    'question_which': '疑问词-哪 (哪-z)'
  })
  const progress = ref<ProgressUpdate | null>(null)
  const error = ref<string | null>(null)

  // 计算属性
  const hasCurrentAnalysis = computed(() => !!currentAnalysis.value)
  const totalSuggestions = computed(() => 
    currentAnalysis.value?.summary.total_suggestions || 0
  )
  const successRate = computed(() => {
    if (!currentAnalysis.value) return 0
    const { successful_variants, failed_variants } = currentAnalysis.value.summary
    const total = successful_variants + failed_variants
    return total > 0 ? Math.round((successful_variants / total) * 100) : 0
  })

  // 动作
  const setLoading = (value: boolean) => {
    loading.value = value
  }

  const setAnalyzing = (value: boolean) => {
    analyzing.value = value
  }

  const setCurrentAnalysis = (analysis: KeywordAnalysisResponse | null) => {
    currentAnalysis.value = analysis
  }

  const setSearchHistory = (history: SearchHistory[]) => {
    searchHistory.value = history
  }

  const setVariantTypes = (types: VariantTypes) => {
    variantTypes.value = types
  }

  const setProgress = (progressData: ProgressUpdate | null) => {
    progress.value = progressData
  }

  const setError = (errorMessage: string | null) => {
    error.value = errorMessage
  }

  const clearError = () => {
    error.value = null
  }

  const addToHistory = (item: SearchHistory) => {
    searchHistory.value.unshift(item)
    // 保持最新20条记录
    if (searchHistory.value.length > 20) {
      searchHistory.value = searchHistory.value.slice(0, 20)
    }
  }

  // 重置状态
  const reset = () => {
    loading.value = false
    analyzing.value = false
    currentAnalysis.value = null
    progress.value = null
    error.value = null
  }

  return {
    // 状态
    loading,
    analyzing,
    currentAnalysis,
    searchHistory,
    variantTypes,
    progress,
    error,

    // 计算属性
    hasCurrentAnalysis,
    totalSuggestions,
    successRate,

    // 动作
    setLoading,
    setAnalyzing,
    setCurrentAnalysis,
    setSearchHistory,
    setVariantTypes,
    setProgress,
    setError,
    clearError,
    addToHistory,
    reset,
  }
})