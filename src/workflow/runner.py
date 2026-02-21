"""Workflow runner for executing the decision analysis."""
from typing import Optional, Callable
from ..schemas import DecisionInput, AgentState, Recommendation
from .graph import create_workflow, WorkflowState


class DecisionWorkflowRunner:
    """Runs the complete decision analysis workflow."""
    
    def __init__(
        self,
        model_name: str = "gpt-4",
        temperature: float = 0.0
    ):
        """Initialize the workflow runner."""
        self.workflow = create_workflow(
            model_name=model_name,
            temperature=temperature
        )
    
    def run(
        self,
        decision_input: DecisionInput,
        progress_callback: Optional[Callable[[str, int], None]] = None
    ) -> AgentState:
        """
        Execute the full workflow.
        
        Args:
            decision_input: The decision to analyze
            progress_callback: Optional callback for progress updates (step_name, progress_percent)
            
        Returns:
            AgentState with all agent outputs and final recommendation
        """
        # Initialize state
        initial_state = AgentState(
            decision_input=decision_input,
            current_step="initialized"
        )
        
        # Progress tracking
        steps = {
            "planner_complete": ("🔍 Step 2/5: Researching context...", 30),
            "research_complete": ("⚠️ Step 3/5: Analyzing risks...", 50),
            "risk_complete": ("🎁 Step 4/5: Identifying opportunities...", 70),
            "opportunity_complete": ("🧠 Step 5/5: Synthesizing recommendation...", 85),
            "complete": ("✅ Complete!", 100)
        }
        
        # Run workflow with progress tracking
        workflow_state: WorkflowState = {"state": initial_state}
        
        # Stream through workflow steps
        for event in self.workflow.stream(workflow_state):
            if "state" in event:
                current_state = event["state"]
                step = current_state.current_step
                
                if step in steps and progress_callback:
                    step_name, progress = steps[step]
                    progress_callback(step_name, progress)
        
        # Get final result
        result = self.workflow.invoke(workflow_state)
        return result["state"]
    
    def get_recommendation(self, decision_input: DecisionInput) -> Optional[Recommendation]:
        """
        Run workflow and return just the recommendation.
        
        Args:
            decision_input: The decision to analyze
            
        Returns:
            Recommendation or None if error occurred
        """
        final_state = self.run(decision_input)
        
        if final_state.error:
            raise Exception(f"Workflow error: {final_state.error}")
        
        return final_state.recommendation
