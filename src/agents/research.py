"""Research Agent - analyzes context for each factor."""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from .base import BaseAgent
from ..schemas import ResearchOutput, PlannerOutput


class ResearchAgent(BaseAgent):
    """Analyzes context and gathers insights for each evaluation factor."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return ResearchOutput
    
    def get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """You are a research analyst. Your job is to analyze each evaluation factor in depth.

For each factor, provide:
- Key insights about how this factor relates to the decision
- Specific considerations or data points
- Relevant context that would inform scoring

IMPORTANT: You must provide:
1. "analyses" - array of analysis for each factor
2. "overall_context" - a summary of the overall situation

Be thorough but concise. Focus on actionable insights."""),
            ("user", """Decision: {decision}

Context: {context}

Evaluation Factors:
{factors}

Analyze each factor in the context of this decision. Provide both factor-specific analyses AND an overall_context summary.""")
        ])
    
    def run(
        self,
        decision: str,
        context: str,
        planner_output: PlannerOutput
    ) -> ResearchOutput:
        """Run the research agent."""
        factors_text = "\n".join([
            f"- {f.name} ({f.category}): {f.description}"
            for f in planner_output.factors
        ])
        
        return super().run(
            decision=decision,
            context=context,
            factors=factors_text
        )
