"""LangGraph workflow orchestration."""
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END
from ..schemas import AgentState
from ..agents import (
    PlannerAgent,
    ResearchAgent,
    RiskAgent,
    OpportunityAgent,
    StrategistAgent
)


class WorkflowState(TypedDict):
    """Workflow state dictionary for LangGraph."""
    state: AgentState


def create_workflow(
    model_name: str = "gpt-4",
    temperature: float = 0.0
) -> StateGraph:
    """Create the decision analysis workflow graph."""
    
    # Initialize agents
    planner = PlannerAgent(model_name=model_name, temperature=temperature)
    research = ResearchAgent(model_name=model_name, temperature=temperature)
    risk = RiskAgent(model_name=model_name, temperature=temperature)
    opportunity = OpportunityAgent(model_name=model_name, temperature=temperature)
    strategist = StrategistAgent(model_name=model_name, temperature=temperature)
    
    # Define node functions
    def planner_node(state: WorkflowState) -> WorkflowState:
        """Execute planner agent."""
        agent_state = state["state"]
        print("🎯 Running Planner Agent...")
        try:
            planner_output = planner.run(
                decision=agent_state.decision_input.decision,
                context=agent_state.decision_input.context or "",
                timeframe=agent_state.decision_input.timeframe or ""
            )
            print(f"✅ Planner complete: {len(planner_output.factors)} factors identified")
            agent_state.planner_output = planner_output
            agent_state.current_step = "planner_complete"
        except Exception as e:
            print(f"❌ Planner failed: {str(e)}")
            agent_state.error = f"Planner error: {str(e)}"
            agent_state.current_step = "error"
        
        return {"state": agent_state}
    
    def research_node(state: WorkflowState) -> WorkflowState:
        """Execute research agent."""
        agent_state = state["state"]
        print("🔍 Running Research Agent...")
        
        if agent_state.error:
            print("⚠️ Skipping Research - previous error")
            return {"state": agent_state}
        
        try:
            research_output = research.run(
                decision=agent_state.decision_input.decision,
                context=agent_state.decision_input.context or "",
                planner_output=agent_state.planner_output
            )
            print(f"✅ Research complete: {len(research_output.analyses)} analyses")
            agent_state.research_output = research_output
            agent_state.current_step = "research_complete"
        except Exception as e:
            print(f"❌ Research failed: {str(e)}")
            agent_state.error = f"Research error: {str(e)}"
            agent_state.current_step = "error"
        
        return {"state": agent_state}
    
    def risk_node(state: WorkflowState) -> WorkflowState:
        """Execute risk agent."""
        agent_state = state["state"]
        print("⚠️ Running Risk Agent...")
        
        if agent_state.error:
            print("⚠️ Skipping Risk - previous error")
            return {"state": agent_state}
        
        try:
            risk_output = risk.run(
                decision=agent_state.decision_input.decision,
                planner_output=agent_state.planner_output,
                research_output=agent_state.research_output
            )
            print(f"✅ Risk complete: {len(risk_output.risk_scores)} scores, overall: {risk_output.overall_risk_level:.1f}/10")
            agent_state.risk_output = risk_output
            agent_state.current_step = "risk_complete"
        except Exception as e:
            print(f"❌ Risk failed: {str(e)}")
            import traceback
            traceback.print_exc()
            agent_state.error = f"Risk error: {str(e)}"
            agent_state.current_step = "error"
        
        return {"state": agent_state}
    
    def opportunity_node(state: WorkflowState) -> WorkflowState:
        """Execute opportunity agent."""
        agent_state = state["state"]
        print("🎁 Running Opportunity Agent...")
        
        if agent_state.error:
            print("⚠️ Skipping Opportunity - previous error")
            return {"state": agent_state}
        
        try:
            opportunity_output = opportunity.run(
                decision=agent_state.decision_input.decision,
                planner_output=agent_state.planner_output,
                research_output=agent_state.research_output
            )
            print(f"✅ Opportunity complete: {len(opportunity_output.opportunity_scores)} scores, overall: {opportunity_output.overall_opportunity_level:.1f}/10")
            agent_state.opportunity_output = opportunity_output
            agent_state.current_step = "opportunity_complete"
        except Exception as e:
            print(f"❌ Opportunity failed: {str(e)}")
            import traceback
            traceback.print_exc()
            agent_state.error = f"Opportunity error: {str(e)}"
            agent_state.current_step = "error"
        
        return {"state": agent_state}
    
    def strategist_node(state: WorkflowState) -> WorkflowState:
        """Execute strategist agent."""
        agent_state = state["state"]
        print("🧠 Running Strategist Agent...")
        
        if agent_state.error:
            print("⚠️ Skipping Strategist - previous error")
            return {"state": agent_state}
        
        try:
            # Validate that previous agents completed successfully
            if not agent_state.risk_output:
                raise ValueError("Risk analysis not completed - risk_output is None")
            if not agent_state.opportunity_output:
                raise ValueError("Opportunity analysis not completed - opportunity_output is None")
            if not agent_state.research_output:
                raise ValueError("Research analysis not completed - research_output is None")
            
            recommendation = strategist.run(
                decision=agent_state.decision_input.decision,
                research_output=agent_state.research_output,
                risk_output=agent_state.risk_output,
                opportunity_output=agent_state.opportunity_output
            )
            print(f"✅ Strategist complete: {recommendation.recommendation}")
            agent_state.recommendation = recommendation
            agent_state.current_step = "complete"
        except Exception as e:
            print(f"❌ Strategist failed: {str(e)}")
            import traceback
            traceback.print_exc()
            agent_state.error = f"Strategist error: {str(e)}"
            agent_state.current_step = "error"
        
        return {"state": agent_state}
    
    # Build the graph
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("research", research_node)
    workflow.add_node("risk", risk_node)
    workflow.add_node("opportunity", opportunity_node)
    workflow.add_node("strategist", strategist_node)
    
    # Define edges - Sequential execution to avoid concurrent updates
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "research")
    workflow.add_edge("research", "risk")
    workflow.add_edge("risk", "opportunity")  # Run opportunity after risk (sequential)
    workflow.add_edge("opportunity", "strategist")
    workflow.add_edge("strategist", END)
    
    return workflow.compile()
