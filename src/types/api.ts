export interface KeywordAnalysisRequest {
  keyword: string
  variant_types: string[]
}

export interface BusinessMetrics {
  commercial_score: number
  intent_type: string
  competition_level: string
  search_volume_estimate: number
  difficulty_score: number
  opportunity_score: number
}

export interface SuggestionAnalysis {
  keyword: string
  commercial_score: number
  intent_type: string
  competition_level: string
  search_volume_estimate: number
  difficulty_score: number
  opportunity_score: number
}

export interface BusinessAnalysis {
  average_commercial_score: number
  top_opportunities: Array<{
    keyword: string
    commercial_score: number
    opportunity_score: number
    intent_type: string
    search_volume_estimate: number
  }>
  intent_distribution: Record<string, number>
  suggestions_analysis: Record<string, SuggestionAnalysis[]>
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
    duplicate_removed?: number
    unique_suggestions?: number
    average_commercial_score?: number
    intent_distribution?: Record<string, number>
    top_opportunities?: Array<{
      keyword: string
      commercial_score: number
      opportunity_score: number
      intent_type: string
      search_volume_estimate: number
    }>
  }
  business_analysis?: Record<string, BusinessAnalysis>
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

export interface VariantTypesResponse {
  variant_types: VariantTypes
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