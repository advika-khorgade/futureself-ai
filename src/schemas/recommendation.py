"""Final recommendation schema."""
from pydantic import BaseModel, Field
from typing import List, Optional


class ActionItem(BaseModel):
    """A specific action to take."""
    
    action: str = Field(..., description="The action to take")
    priority: str = Field(..., description="high, medium, low")
    timeframe: str = Field(..., description="When to do this")


class Recommendation(BaseModel):
    """Final strategic recommendation."""
    
    decision: str = Field(..., description="The original decision")
    recommendation: str = Field(
        ...,
        description="Clear recommendation: proceed, proceed with caution, or do not proceed"
    )
    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in recommendation (0-1)"
    )
    
    # Synthesis
    key_insights: List[str] = Field(
        ...,
        description="3-5 key insights from the analysis",
        min_length=3,
        max_length=5
    )
    risk_reward_balance: str = Field(
        ...,
        description="Summary of risk vs opportunity balance"
    )
    
    # Actionable guidance
    next_steps: List[ActionItem] = Field(
        ...,
        description="Concrete next steps",
        min_length=1
    )
    
    # Considerations
    critical_assumptions: List[str] = Field(
        default_factory=list,
        description="Key assumptions this recommendation depends on"
    )
    watch_signals: List[str] = Field(
        default_factory=list,
        description="Signals to monitor that might change the recommendation"
    )
    
    # Metadata
    overall_risk_score: float = Field(..., ge=0.0, le=10.0)
    overall_opportunity_score: float = Field(..., ge=0.0, le=10.0)
