"""Analysis and scoring schemas."""
from pydantic import BaseModel, Field
from typing import List, Dict


class FactorAnalysis(BaseModel):
    """Analysis for a single factor."""
    
    factor_name: str
    insights: str = Field(..., description="Key insights about this factor")
    data_points: List[str] = Field(
        default_factory=list,
        description="Specific data points or evidence"
    )


class ResearchOutput(BaseModel):
    """Output from the Research Agent."""
    
    analyses: List[FactorAnalysis] = Field(
        ...,
        description="Analysis for each factor"
    )
    overall_context: str = Field(
        default="Context analysis completed based on provided factors.",
        description="Overall contextual understanding"
    )


class RiskScore(BaseModel):
    """Risk score for a single factor."""
    
    factor_name: str
    score: float = Field(..., ge=0.0, le=10.0, description="Risk score 0-10")
    reasoning: str = Field(..., description="Why this score was assigned")
    severity: str = Field(..., description="low, medium, high, critical")


class RiskOutput(BaseModel):
    """Output from the Risk Agent."""
    
    risk_scores: List[RiskScore] = Field(..., description="Risk scores per factor")
    overall_risk_level: float = Field(..., ge=0.0, le=10.0)
    risk_summary: str


class OpportunityScore(BaseModel):
    """Opportunity score for a single factor."""
    
    factor_name: str
    score: float = Field(..., ge=0.0, le=10.0, description="Opportunity score 0-10")
    reasoning: str = Field(..., description="Why this score was assigned")
    potential: str = Field(..., description="low, medium, high, transformative")


class OpportunityOutput(BaseModel):
    """Output from the Opportunity Agent."""
    
    opportunity_scores: List[OpportunityScore] = Field(
        ...,
        description="Opportunity scores per factor"
    )
    overall_opportunity_level: float = Field(..., ge=0.0, le=10.0)
    opportunity_summary: str
