"""LangGraph state schema."""
from typing import Optional
from pydantic import BaseModel
from .decision import DecisionInput
from .factors import PlannerOutput
from .analysis import ResearchOutput, RiskOutput, OpportunityOutput
from .recommendation import Recommendation


class AgentState(BaseModel):
    """State passed between agents in the workflow."""
    
    # Input
    decision_input: DecisionInput
    
    # Agent outputs
    planner_output: Optional[PlannerOutput] = None
    research_output: Optional[ResearchOutput] = None
    risk_output: Optional[RiskOutput] = None
    opportunity_output: Optional[OpportunityOutput] = None
    
    # Final output
    recommendation: Optional[Recommendation] = None
    
    # Metadata
    current_step: str = "initialized"
    error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
