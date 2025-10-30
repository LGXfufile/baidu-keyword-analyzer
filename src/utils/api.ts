import axios, { AxiosResponse } from 'axios'
import type {
  KeywordAnalysisRequest,
  KeywordAnalysisResponse,
  SearchHistory,
  VariantTypes,
  VariantTypesResponse,
  ProgressUpdate,
  ExportRequest
} from '@/types/api'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

export const keywordApi = {
  // 获取变体类型
  getVariantTypes(): Promise<VariantTypesResponse> {
    return api.get('/variant-types')
  },

  // 分析关键词
  analyzeKeyword(data: KeywordAnalysisRequest): Promise<KeywordAnalysisResponse> {
    return api.post('/analyze', data)
  },

  // 获取分析进度
  getProgress(sessionId: string): Promise<ProgressUpdate> {
    return api.get(`/progress/${sessionId}`)
  },

  // 获取搜索历史
  getSearchHistory(limit = 10): Promise<SearchHistory[]> {
    return api.get('/history', { params: { limit } })
  },

  // 获取会话结果
  getSessionResults(sessionId: string): Promise<KeywordAnalysisResponse> {
    return api.get(`/results/${sessionId}`)
  },

  // 导出结果
  exportResults(data: ExportRequest): Promise<Blob> {
    return api.post('/export', data, {
      responseType: 'blob',
    })
  },
}

export default api