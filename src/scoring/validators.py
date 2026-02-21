"""Score validation utilities."""
from typing import List
from ..schemas import RiskScore, OpportunityScore, RiskOutput, OpportunityOutput


class ScoreValidator:
    """Validates scoring outputs."""
    
    @staticmethod
    def validate_score_range(score: float, min_val: float = 0.0, max_val: float = 10.0) -> bool:
        """Validate score is within range."""
        return min_val <= score <= max_val
    
    @staticmethod
    def validate_risk_scores(risk_output: RiskOutput) -> List[str]:
        """
        Validate risk scores.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check overall score
        if not ScoreValidator.validate_score_range(risk_output.overall_risk_level):
            errors.append(
                f"Overall risk level {risk_output.overall_risk_level} out of range"
            )
        
        # Check individual scores
        for risk_score in risk_output.risk_scores:
            if not ScoreValidator.validate_score_range(risk_score.score):
                errors.append(
                    f"Risk score for {risk_score.factor_name} "
                    f"({risk_score.score}) out of range"
                )
            
            # Validate severity
            valid_severities = {"low", "medium", "high", "critical"}
            if risk_score.severity.lower() not in valid_severities:
                errors.append(
                    f"Invalid severity '{risk_score.severity}' for {risk_score.factor_name}"
                )
        
        return errors
    
    @staticmethod
    def validate_opportunity_scores(opportunity_output: OpportunityOutput) -> List[str]:
        """
        Validate opportunity scores.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check overall score
        if not ScoreValidator.validate_score_range(
            opportunity_output.overall_opportunity_level
        ):
            errors.append(
                f"Overall opportunity level "
                f"{opportunity_output.overall_opportunity_level} out of range"
            )
        
        # Check individual scores
        for opp_score in opportunity_output.opportunity_scores:
            if not ScoreValidator.validate_score_range(opp_score.score):
                errors.append(
                    f"Opportunity score for {opp_score.factor_name} "
                    f"({opp_score.score}) out of range"
                )
            
            # Validate potential
            valid_potentials = {"low", "medium", "high", "transformative"}
            if opp_score.potential.lower() not in valid_potentials:
                errors.append(
                    f"Invalid potential '{opp_score.potential}' for {opp_score.factor_name}"
                )
        
        return errors
    
    @staticmethod
    def validate_score_consistency(
        risk_output: RiskOutput,
        opportunity_output: OpportunityOutput
    ) -> List[str]:
        """
        Validate consistency between risk and opportunity scores.
        
        Returns:
            List of validation warnings (empty if consistent)
        """
        warnings = []
        
        # Check factor alignment
        risk_factors = {r.factor_name for r in risk_output.risk_scores}
        opp_factors = {o.factor_name for o in opportunity_output.opportunity_scores}
        
        if risk_factors != opp_factors:
            missing_in_risk = opp_factors - risk_factors
            missing_in_opp = risk_factors - opp_factors
            
            if missing_in_risk:
                warnings.append(
                    f"Factors in opportunity but not risk: {missing_in_risk}"
                )
            if missing_in_opp:
                warnings.append(
                    f"Factors in risk but not opportunity: {missing_in_opp}"
                )
        
        return warnings
