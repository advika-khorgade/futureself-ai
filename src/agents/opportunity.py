"""Opportunity Agent - assigns opportunity scores to each factor."""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from .base import BaseAgent
from ..schemas import OpportunityOutput, PlannerOutput, ResearchOutput


class OpportunityAgent(BaseAgent):
    """Evaluates and scores opportunities for each factor."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return OpportunityOutput
    
    def get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """You are an opportunity assessment expert. Your job is to assign opportunity scores to each evaluation factor.

Opportunity Scoring Scale (0-10):
- 0-2: Minimal opportunity - negligible positive impact
- 3-4: Low opportunity - minor positive impact
- 5-6: Medium opportunity - moderate positive impact, worth pursuing
- 7-8: High opportunity - significant positive impact, strong upside
- 9-10: Transformative opportunity - exceptional positive impact, game-changing

For each factor, assign:
- A numerical score (0-10)
- Clear reasoning for the score
- Potential level: low, medium, high, or transformative

Consider:
- Probability of positive outcome
- Magnitude of potential gain
- Long-term value creation
- Compounding effects
- Unique advantages

Be objective and evidence-based.

IMPORTANT: You must respond with valid JSON only."""),
            ("user", """Decision: {decision}

Evaluation Factors:
{factors}

Research Insights:
{research}

Assign opportunity scores to each factor.""")
        ])
    
    def run(
        self,
        decision: str,
        planner_output: PlannerOutput,
        research_output: ResearchOutput
    ) -> OpportunityOutput:
        """Run the opportunity agent."""
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
