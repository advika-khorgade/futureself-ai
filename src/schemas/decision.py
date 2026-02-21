"""Decision input schema."""
from pydantic import BaseModel, Field
from typing import Optional


class DecisionInput(BaseModel):
    """User's decision to be analyzed."""
    
    decision: str = Field(
        ...,
        description="The decision to be evaluated",
        min_length=10
    )
    context: Optional[str] = Field(
        None,
        description="Additional context about the decision"
    )
    timeframe: Optional[str] = Field(
        None,
        description="Expected timeframe for the decision (e.g., '6 months', '2 years')"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "decision": "Should I switch careers from software engineering to AI research?",
                "context": "10 years experience in backend development, interested in ML",
                "timeframe": "1 year"
            }
        }
