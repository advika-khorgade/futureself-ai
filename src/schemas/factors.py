"""Evaluation factors schema."""
from pydantic import BaseModel, Field
from typing import List


class EvaluationFactor(BaseModel):
    """A single factor to evaluate."""
    
    name: str = Field(..., description="Factor name")
    description: str = Field(..., description="Why this factor matters")
    category: str = Field(
        ...,
        description="Category: financial, personal, professional, social, health"
    )


class PlannerOutput(BaseModel):
    """Output from the Planner Agent."""
    
    factors: List[EvaluationFactor] = Field(
        ...,
        description="List of factors to evaluate",
        min_length=3,
        max_length=10
    )
    decision_summary: str = Field(
        ...,
        description="Summarized understanding of the decision"
    )
