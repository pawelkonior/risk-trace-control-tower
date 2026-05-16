from __future__ import annotations

from fastapi import APIRouter

from .schemas import RwaAnalysisRequest, RwaAnalysisResponse
from .workflow import run_rwa_analysis

router = APIRouter(prefix="/v1/agents", tags=["rwa-agents"])


@router.post("/rwa-analysis/run", response_model=RwaAnalysisResponse)
def run_rwa_analysis_endpoint(request: RwaAnalysisRequest) -> RwaAnalysisResponse:
    """Run guarded RWA executive commentary over anonymized calculator data."""
    return run_rwa_analysis(request)
