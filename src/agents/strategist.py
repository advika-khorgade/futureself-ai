"""Strategist Agent - synthesizes final recommendation."""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from .base import BaseAgent
from ..schemas import (
    Recommendation,
    PlannerOutput,
    ResearchOutput,
    RiskOutput,
    OpportunityOutput
)


class StrategistAgent(BaseAgent):
    """Synthesizes all analysis into a final strategic recommendation."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return Recommendation
    
    def get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """You are a strategic advisor. Your job is to synthesize all analysis into a clear, actionable recommendation.

Based on the risk and opportunity scores, provide:

1. Clear Recommendation:
   - "Proceed" - if opportunities significantly outweigh risks
   - "Proceed with Caution" - if opportunities and risks are balanced
   - "Do Not Proceed" - if risks significantly outweigh opportunities

2. Confidence Level (0-1):
   - How confident are you in this recommendation?
   - Consider data quality, uncertainty, and factor alignment

3. Key Insights (3-5):
   - Most important findings from the analysis
   - Critical factors that drive the recommendation

4. Risk-Reward Balance:
   - Clear summary of the tradeoff

5. Next Steps:
   - Concrete, actionable steps
   - Prioritized (high/medium/low)
   - Time-bound

6. Critical Assumptions:
   - What must be true for this recommendation to hold?

7. Watch Signals:
   - What should be monitored that might change the recommendation?

Be decisive, clear, and actionable."""),
            ("user", """Decision: {decision}

Overall Risk Score: {overall_risk}/10
Overall Opportunity Score: {overall_opportunity}/10

Risk Analysis:
{risk_details}

Opportunity Analysis:
{opportunity_details}

Research Context:
{research_summary}

Provide your strategic recommendation.""")
        ])
    
    def run(
        self,
        decision: str,
        research_output: ResearchOutput,
        risk_output: RiskOutput,
        opportunity_output: OpportunityOutput
    ) -> Recommendation:
        """Run the strategist agent."""
        risk_details = "\n".join([
            f"- {r.factor_name}: {r.score}/10 ({r.severity}) - {r.reasoning}"
            for r in risk_output.risk_scores
        ])
        
        opportunity_details = "\n".join([
            f"- {o.factor_name}: {o.score}/10 ({o.potential}) - {o.reasoning}"
            for o in opportunity_output.opportunity_scores
        ])
        
        research_summary = research_output.overall_context
        
        result = super().run(
            decision=decision,
            overall_risk=risk_output.overall_risk_level,
            overall_opportunity=opportunity_output.overall_opportunity_level,
            risk_details=risk_details,
            opportunity_details=opportunity_details,
            research_summary=research_summary
        )
        
        # Add computed scores
        result.overall_risk_score = risk_output.overall_risk_level
        result.overall_opportunity_score = opportunity_output.overall_opportunity_level
        
        return result
