"""Deterministic scoring engine."""
from typing import List, Dict, Tuple
from ..schemas import RiskScore, OpportunityScore


class ScoringEngine:
    """Deterministic scoring calculations."""
    
    @staticmethod
    def calculate_weighted_average(
        scores: List[float],
        weights: List[float] = None
    ) -> float:
        """
        Calculate weighted average of scores.
        
        Args:
            scores: List of scores (0-10)
            weights: Optional weights (defaults to equal weighting)
            
        Returns:
            Weighted average score
        """
        if not scores:
            return 0.0
        
        if weights is None:
            weights = [1.0] * len(scores)
        
        if len(scores) != len(weights):
            raise ValueError("Scores and weights must have same length")
        
        total_weight = sum(weights)
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        return round(weighted_sum / total_weight, 2)
    
    @staticmethod
    def calculate_overall_risk(risk_scores: List[RiskScore]) -> float:
        """
        Calculate overall risk score from individual factor risks.
        
        Uses weighted average with higher weights for critical/high severity.
        
        Args:
            risk_scores: List of risk scores
            
        Returns:
            Overall risk score (0-10)
        """
        if not risk_scores:
            return 0.0
        
        # Weight by severity
        severity_weights = {
            "low": 1.0,
            "medium": 1.5,
            "high": 2.0,
            "critical": 3.0
        }
        
        scores = [r.score for r in risk_scores]
        weights = [
            severity_weights.get(r.severity.lower(), 1.0)
            for r in risk_scores
        ]
        
        return ScoringEngine.calculate_weighted_average(scores, weights)
    
    @staticmethod
    def calculate_overall_opportunity(
        opportunity_scores: List[OpportunityScore]
    ) -> float:
        """
        Calculate overall opportunity score from individual factor opportunities.
        
        Uses weighted average with higher weights for transformative/high potential.
        
        Args:
            opportunity_scores: List of opportunity scores
            
        Returns:
            Overall opportunity score (0-10)
        """
        if not opportunity_scores:
            return 0.0
        
        # Weight by potential
        potential_weights = {
            "low": 1.0,
            "medium": 1.5,
            "high": 2.0,
            "transformative": 3.0
        }
        
        scores = [o.score for o in opportunity_scores]
        weights = [
            potential_weights.get(o.potential.lower(), 1.0)
            for o in opportunity_scores
        ]
        
        return ScoringEngine.calculate_weighted_average(scores, weights)
    
    @staticmethod
    def get_risk_level(score: float) -> str:
        """
        Convert risk score to level.
        
        Args:
            score: Risk score (0-10)
            
        Returns:
            Risk level: minimal, low, medium, high, critical
        """
        if score < 2.5:
            return "minimal"
        elif score < 4.5:
            return "low"
        elif score < 6.5:
            return "medium"
        elif score < 8.5:
            return "high"
        else:
            return "critical"
    
    @staticmethod
    def get_opportunity_level(score: float) -> str:
        """
        Convert opportunity score to level.
        
        Args:
            score: Opportunity score (0-10)
            
        Returns:
            Opportunity level: minimal, low, medium, high, transformative
        """
        if score < 2.5:
            return "minimal"
        elif score < 4.5:
            return "low"
        elif score < 6.5:
            return "medium"
        elif score < 8.5:
            return "high"
        else:
            return "transformative"
    
    @staticmethod
    def calculate_risk_reward_ratio(
        risk_score: float,
        opportunity_score: float
    ) -> float:
        """
        Calculate risk-reward ratio.
        
        Args:
            risk_score: Overall risk score
            opportunity_score: Overall opportunity score
            
        Returns:
            Ratio (opportunity / risk), or 0 if risk is 0
        """
        if risk_score == 0:
            return float('inf') if opportunity_score > 0 else 0.0
        
        return round(opportunity_score / risk_score, 2)
    
    @staticmethod
    def get_recommendation_category(
        risk_score: float,
        opportunity_score: float
    ) -> str:
        """
        Determine recommendation category based on scores.
        
        Args:
            risk_score: Overall risk score
            opportunity_score: Overall opportunity score
            
        Returns:
            Recommendation: "Proceed", "Proceed with Caution", "Do Not Proceed"
        """
        ratio = ScoringEngine.calculate_risk_reward_ratio(
            risk_score,
            opportunity_score
        )
        
        # High opportunity, low risk
        if opportunity_score >= 7.0 and risk_score <= 4.0:
            return "Proceed"
        
        # Low opportunity, high risk
        if opportunity_score <= 4.0 and risk_score >= 7.0:
            return "Do Not Proceed"
        
        # Use ratio for middle ground
        if ratio >= 1.5:
            return "Proceed"
        elif ratio >= 0.8:
            return "Proceed with Caution"
        else:
            return "Do Not Proceed"
    
    @staticmethod
    def analyze_score_distribution(
        scores: List[float]
    ) -> Dict[str, float]:
        """
        Analyze distribution of scores.
        
        Args:
            scores: List of scores
            
        Returns:
            Dictionary with min, max, mean, median, std_dev
        """
        if not scores:
            return {
                "min": 0.0,
                "max": 0.0,
                "mean": 0.0,
                "median": 0.0,
                "std_dev": 0.0
            }
        
        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        
        mean = sum(sorted_scores) / n
        median = (
            sorted_scores[n // 2]
            if n % 2 == 1
            else (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2
        )
        
        variance = sum((x - mean) ** 2 for x in sorted_scores) / n
        std_dev = variance ** 0.5
        
        return {
            "min": round(min(sorted_scores), 2),
            "max": round(max(sorted_scores), 2),
            "mean": round(mean, 2),
            "median": round(median, 2),
            "std_dev": round(std_dev, 2)
        }
