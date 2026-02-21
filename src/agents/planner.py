"""Planner Agent - breaks decision into evaluation factors."""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from .base import BaseAgent
from ..schemas import PlannerOutput


class PlannerAgent(BaseAgent):
    """Breaks down a decision into key evaluation factors."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return PlannerOutput
    
    def get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """You are a strategic planning expert. Your job is to break down complex decisions into clear evaluation factors.

For each decision, identify 5-8 key factors that should be evaluated. Consider:
- Financial implications
- Personal impact (happiness, fulfillment, stress)
- Professional growth
- Social/relationship effects
- Health and wellbeing
- Time commitment
- Reversibility
- Alignment with long-term goals

Each factor should be:
- Specific and measurable
- Relevant to the decision
- Non-overlapping with other factors

Categorize each factor as: financial, personal, professional, social, or health."""),
            ("user", """Decision: {decision}

Context: {context}
Timeframe: {timeframe}

Break this decision into evaluation factors.""")
        ])
    
    def run(self, decision: str, context: str = "", timeframe: str = "") -> PlannerOutput:
        """Run the planner agent."""
        return super().run(
            decision=decision,
            context=context or "No additional context provided",
            timeframe=timeframe or "Not specified"
        )
