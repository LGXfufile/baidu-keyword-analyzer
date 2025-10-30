export interface KeywordAnalysisRequest {
  keyword: string
  variant_types: string[]
}

export interface KeywordAnalysisResponse {
  session_id: string
  base_keyword: string
  variant_types: string[]
  total_variants: number
  results: Record<string, Record<string, string[]>>
  summary: {
    total_suggestions: number
    successful_variants: number
    failed_variants: number
  }
}

export interface SearchHistory {
  session_id: string
  original_keyword: string
  variant_types: string[]
  total_suggestions: number
  status: 'pending' | 'running' | 'completed' | 'failed'
  created_at: string
}

export interface VariantTypes {
  [key: string]: string
}

export interface ProgressUpdate {
  session_id: string
  processed: number
  total: number
  percentage: number
}

export interface ExportRequest {
  session_id: string
  format: 'excel' | 'csv' | 'json'
}

export interface ApiResponse<T = any> {
  data?: T
  message?: string
  error?: string
}