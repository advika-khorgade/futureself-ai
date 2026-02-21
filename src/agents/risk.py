"""Risk Agent - assigns risk scores to each factor."""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from .base import BaseAgent
from ..schemas import RiskOutput, PlannerOutput, ResearchOutput


class RiskAgent(BaseAgent):
    """Evaluates and scores risks for each factor."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return RiskOutput
    
    def get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """You are a risk assessment expert. Your job is to assign risk scores to each evaluation factor.

Risk Scoring Scale (0-10):
- 0-2: Minimal risk - negligible negative impact
- 3-4: Low risk - minor negative impact, easily manageable
- 5-6: Medium risk - moderate negative impact, requires attention
- 7-8: High risk - significant negative impact, needs mitigation
- 9-10: Critical risk - severe negative impact, potentially catastrophic

For each factor, assign:
- A numerical score (0-10)
- Clear reasoning for the score
- Severity level: low, medium, high, or critical

Consider:
- Probability of negative outcome
- Magnitude of potential loss
- Reversibility
- Time to recover
- Cascading effects

Be objective and evidence-based.

IMPORTANT: You must respond with valid JSON only."""),
            ("user", """Decision: {decision}

Evaluation Factors:
{factors}

Research Insights:
{research}

Assign risk scores to each factor.""")
        ])
    
    def run(
        self,
        decision: str,
        planner_output: PlannerOutput,
        research_output: ResearchOutput
    ) -> RiskOutput:
        """Run the risk agent."""
        factors_text = "\n".join([
            f"- {f.name}: {f.description}"
            for f in planner_output.factors
        ])
        
        research_text = "\n".join([
            f"- {a.factor_name}: {a.insights}"
            for a in research_output.analyses
        ])
        
        return super().run(
            decision=decision,
            factors=factors_text,
            research=research_text
        )
