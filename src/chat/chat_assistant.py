"""AI Chat Assistant for follow-up questions."""
from langchain_core.prompts import ChatPromptTemplate
from ..agents.llm_factory import create_llm
from ..schemas import AgentState


class ChatAssistant:
    """AI assistant for answering follow-up questions about decisions."""
    
    def __init__(self, model_name: str = None, temperature: float = 0.3):
        """Initialize chat assistant with slightly higher temperature for conversation."""
        self.llm = create_llm(model_name=model_name, temperature=temperature)
    
    def ask(self, question: str, state: AgentState) -> str:
        """
        Ask a follow-up question about the decision analysis.
        
        Args:
            question: User's question
            state: The decision analysis state
            
        Returns:
            AI assistant's response
        """
        rec = state.recommendation
        
        # Create context from the analysis
        context = f"""
Decision: {state.decision_input.decision}

Recommendation: {rec.recommendation}
Confidence: {rec.confidence_level:.0%}
Risk Score: {rec.overall_risk_score:.1f}/10
Opportunity Score: {rec.overall_opportunity_score:.1f}/10

Key Insights:
{chr(10).join(f"- {insight}" for insight in rec.key_insights)}

Risk-Reward Balance:
{rec.risk_reward_balance}

Next Steps:
{chr(10).join(f"- [{action.priority}] {action.action} (Timeframe: {action.timeframe})" for action in rec.next_steps)}

Risk Analysis:
{chr(10).join(f"- {r.factor_name}: {r.score:.1f}/10 ({r.severity}) - {r.reasoning}" for r in state.risk_output.risk_scores)}

Opportunity Analysis:
{chr(10).join(f"- {o.factor_name}: {o.score:.1f}/10 ({o.potential}) - {o.reasoning}" for o in state.opportunity_output.opportunity_scores)}
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant helping users understand their decision analysis.

You have access to a comprehensive analysis of their decision including:
- Risk and opportunity scores
- Strategic recommendations
- Key insights
- Next steps

Answer their questions clearly and concisely. Be supportive and help them make better decisions.
If they ask about something not in the analysis, acknowledge that and provide general guidance.

Keep responses focused and actionable."""),
            ("user", """Here is the decision analysis:

{context}

User's question: {question}

Please provide a helpful, clear answer.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"context": context, "question": question})
        
        # Extract content from response
        if hasattr(response, 'content'):
            return response.content
        return str(response)

    
    def ask_question(self, state: AgentState, question: str) -> str:
        """
        Ask a follow-up question about the decision analysis.
        Alias for ask() method for backward compatibility.
        
        Args:
            state: The decision analysis state
            question: User's question
            
        Returns:
            AI assistant's response
        """
        return self.ask(question, state)
