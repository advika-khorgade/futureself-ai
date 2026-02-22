"""Manage decision history."""
import json
from datetime import datetime
from typing import List, Optional, Dict
from ..auth.database import DecisionHistory, get_session
from ..schemas import AgentState


class HistoryManager:
    """Manages decision history for users."""
    
    @staticmethod
    def save_decision(user_id: int, state: AgentState, tags: List[str] = None) -> int:
        """
        Save a decision analysis to history.
        
        Returns:
            Decision ID
        """
        session = get_session()
        
        try:
            rec = state.recommendation
            
            # Create history entry
            history = DecisionHistory(
                user_id=user_id,
                decision_text=state.decision_input.decision,
                context=state.decision_input.context,
                timeframe=state.decision_input.timeframe,
                recommendation=rec.recommendation,
                confidence_level=rec.confidence_level,
                risk_score=rec.overall_risk_score,
                opportunity_score=rec.overall_opportunity_score,
                tags=",".join(tags) if tags else "",
                full_analysis=json.dumps({
                    "planner": state.planner_output.model_dump() if state.planner_output else None,
                    "research": state.research_output.model_dump() if state.research_output else None,
                    "risk": state.risk_output.model_dump() if state.risk_output else None,
                    "opportunity": state.opportunity_output.model_dump() if state.opportunity_output else None,
                    "recommendation": rec.model_dump()
                })
            )
            
            session.add(history)
            session.commit()
            
            return history.id
            
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to save decision: {str(e)}")
        finally:
            session.close()
    
    @staticmethod
    def get_user_history(
        user_id: int,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get decision history for a user.
        
        Args:
            user_id: User ID
            search: Search term for decision text
            tags: Filter by tags
            limit: Maximum number of results
            
        Returns:
            List of decision history entries
        """
        session = get_session()
        
        try:
            query = session.query(DecisionHistory).filter(
                DecisionHistory.user_id == user_id
            )
            
            # Apply search filter
            if search:
                query = query.filter(
                    DecisionHistory.decision_text.contains(search)
                )
            
            # Apply tag filter
            if tags:
                for tag in tags:
                    query = query.filter(
                        DecisionHistory.tags.contains(tag)
                    )
            
            # Order by most recent
            query = query.order_by(DecisionHistory.created_at.desc())
            
            # Limit results
            results = query.limit(limit).all()
            
            return [
                {
                    "id": r.id,
                    "decision_text": r.decision_text,
                    "recommendation": r.recommendation,
                    "confidence_level": r.confidence_level,
                    "risk_score": r.risk_score,
                    "opportunity_score": r.opportunity_score,
                    "tags": r.tags.split(",") if r.tags else [],
                    "created_at": r.created_at,
                    "context": r.context,
                    "timeframe": r.timeframe
                }
                for r in results
            ]
            
        finally:
            session.close()
    
    @staticmethod
    def get_decision_by_id(decision_id: int) -> Optional[Dict]:
        """Get full decision analysis by ID."""
        session = get_session()
        
        try:
            decision = session.query(DecisionHistory).filter(
                DecisionHistory.id == decision_id
            ).first()
            
            if not decision:
                return None
            
            return {
                "id": decision.id,
                "decision_text": decision.decision_text,
                "context": decision.context,
                "timeframe": decision.timeframe,
                "recommendation": decision.recommendation,
                "confidence_level": decision.confidence_level,
                "risk_score": decision.risk_score,
                "opportunity_score": decision.opportunity_score,
                "tags": decision.tags.split(",") if decision.tags else [],
                "created_at": decision.created_at,
                "full_analysis": json.loads(decision.full_analysis) if decision.full_analysis else None
            }
            
        finally:
            session.close()
    
    @staticmethod
    def delete_decision(decision_id: int, user_id: int) -> bool:
        """Delete a decision from history."""
        session = get_session()
        
        try:
            decision = session.query(DecisionHistory).filter(
                DecisionHistory.id == decision_id,
                DecisionHistory.user_id == user_id
            ).first()
            
            if decision:
                session.delete(decision)
                session.commit()
                return True
            
            return False
            
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_all_tags(user_id: int) -> List[str]:
        """Get all unique tags for a user."""
        session = get_session()
        
        try:
            results = session.query(DecisionHistory.tags).filter(
                DecisionHistory.user_id == user_id,
                DecisionHistory.tags != ""
            ).all()
            
            # Extract and deduplicate tags
            all_tags = set()
            for (tags_str,) in results:
                if tags_str:
                    all_tags.update(tags_str.split(","))
            
            return sorted(list(all_tags))
            
        finally:
            session.close()

    
    @staticmethod
    def get_user_tags(user_id: int) -> List[str]:
        """Alias for get_all_tags for backward compatibility."""
        return HistoryManager.get_all_tags(user_id)
    
    @staticmethod
    def search_decisions(user_id: int, query: str) -> List:
        """Search decisions by text query."""
        session = get_session()
        
        try:
            results = session.query(DecisionHistory).filter(
                DecisionHistory.user_id == user_id,
                DecisionHistory.decision_text.contains(query)
            ).order_by(DecisionHistory.created_at.desc()).all()
            
            # Convert to list of objects (not dicts) for compatibility
            return results
            
        finally:
            session.close()
    
    @staticmethod
    def get_decisions_by_tag(user_id: int, tag: str) -> List:
        """Get decisions filtered by a specific tag."""
        session = get_session()
        
        try:
            results = session.query(DecisionHistory).filter(
                DecisionHistory.user_id == user_id,
                DecisionHistory.tags.contains(tag)
            ).order_by(DecisionHistory.created_at.desc()).all()
            
            # Convert to list of objects (not dicts) for compatibility
            return results
            
        finally:
            session.close()
