from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class KeywordAnalysisRequest(BaseModel):
    keyword: str
    variant_types: List[str]
    
class KeywordAnalysisResponse(BaseModel):
    session_id: str
    base_keyword: str
    variant_types: List[str]
    total_variants: int
    results: Dict[str, Dict[str, List[str]]]
    summary: Dict[str, int]

class SearchHistoryResponse(BaseModel):
    session_id: str
    original_keyword: str
    variant_types: List[str]
    total_suggestions: int
    status: str
    created_at: str

class VariantTypesResponse(BaseModel):
    variant_types: Dict[str, str]

class ProgressUpdate(BaseModel):
    session_id: str
    processed: int
    total: int
    percentage: float
    
class ExportRequest(BaseModel):
    session_id: str
    format: str  # 'excel', 'csv', 'json'