"""Output formatting utilities."""
from typing import List
from ..schemas import (
    RiskScore,
    OpportunityScore,
    Recommendation,
    ActionItem
)


class OutputFormatter:
    """Format outputs for display."""
    
    @staticmethod
    def format_risk_scores(risk_scores: List[RiskScore]) -> str:
        """Format risk scores as text."""
        lines = ["Risk Scores:", "=" * 50]
        
        for risk in sorted(risk_scores, key=lambda x: x.score, reverse=True):
            lines.append(
                f"\n{risk.factor_name}: {risk.score:.1f}/10 ({risk.severity.upper()})"
            )
            lines.append(f"  → {risk.reasoning}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_opportunity_scores(opportunity_scores: List[OpportunityScore]) -> str:
        """Format opportunity scores as text."""
        lines = ["Opportunity Scores:", "=" * 50]
        
        for opp in sorted(opportunity_scores, key=lambda x: x.score, reverse=True):
            lines.append(
                f"\n{opp.factor_name}: {opp.score:.1f}/10 ({opp.potential.upper()})"
            )
            lines.append(f"  → {opp.reasoning}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_recommendation(recommendation: Recommendation) -> str:
        """Format recommendation as text."""
        lines = [
            "=" * 60,
            "RECOMMENDATION",
            "=" * 60,
            f"\nDecision: {recommendation.decision}",
            f"\nRecommendation: {recommendation.recommendation}",
            f"Confidence: {recommendation.confidence_level:.0%}",
            f"\nRisk Score: {recommendation.overall_risk_score:.1f}/10",
            f"Opportunity Score: {recommendation.overall_opportunity_score:.1f}/10",
            f"\n{recommendation.risk_reward_balance}",
            "\n" + "=" * 60,
            "KEY INSIGHTS",
            "=" * 60,
        ]
        
        for i, insight in enumerate(recommendation.key_insights, 1):
            lines.append(f"\n{i}. {insight}")
        
        lines.extend([
            "\n" + "=" * 60,
            "NEXT STEPS",
            "=" * 60,
        ])
        
        for action in recommendation.next_steps:
            lines.append(
                f"\n[{action.priority.upper()}] {action.action}"
            )
            lines.append(f"  Timeframe: {action.timeframe}")
        
        if recommendation.critical_assumptions:
            lines.extend([
                "\n" + "=" * 60,
                "CRITICAL ASSUMPTIONS",
                "=" * 60,
            ])
            for assumption in recommendation.critical_assumptions:
                lines.append(f"\n• {assumption}")
        
        if recommendation.watch_signals:
            lines.extend([
                "\n" + "=" * 60,
                "WATCH SIGNALS",
                "=" * 60,
            ])
            for signal in recommendation.watch_signals:
                lines.append(f"\n• {signal}")
        
        return "\n".join(lines)
