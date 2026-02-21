"""Streamlit UI components."""
import streamlit as st
import plotly.graph_objects as go
from typing import Optional
from ..schemas import DecisionInput, AgentState


def render_header():
    """Render application header."""
    st.markdown("""
        <div class="main-header">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">🔮 FutureSelf AI</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                AI-Powered Decision Intelligence Platform
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_input_form() -> Optional[DecisionInput]:
    """
    Render decision input form.
    
    Returns:
        DecisionInput if form submitted, None otherwise
    """
    st.markdown("### 📝 Describe Your Decision")
    st.markdown("Our AI will analyze your decision across multiple dimensions to provide strategic insights.")
    
    with st.form("decision_form", clear_on_submit=False):
        decision = st.text_area(
            "What decision are you evaluating?",
            placeholder="Example: Should I switch careers from software engineering to AI research?",
            height=120,
            help="Describe the decision you need to make in detail"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            context = st.text_area(
                "Additional Context (Optional)",
                placeholder="Example: 10 years experience in backend development, interested in ML",
                height=120,
                help="Provide any relevant background information"
            )
        
        with col2:
            timeframe = st.text_input(
                "Decision Timeframe (Optional)",
                placeholder="Example: 1 year, 6 months",
                help="When do you need to make this decision?"
            )
        
        col_left, col_center, col_right = st.columns([1, 1, 1])
        with col_center:
            submitted = st.form_submit_button(
                "🚀 Analyze Decision",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            if not decision or len(decision) < 10:
                st.error("⚠️ Please provide a decision description (at least 10 characters)")
                return None
            
            return DecisionInput(
                decision=decision,
                context=context if context else None,
                timeframe=timeframe if timeframe else None
            )
    
    return None


def render_results(state: AgentState):
    """Render analysis results."""
    st.success("✅ Analysis Complete!")
    
    st.markdown("---")
    
    # Recommendation Summary
    rec = state.recommendation
    
    # Hero section with main recommendation
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 12px; margin: 1rem 0; color: white;">
            <h2 style="margin: 0; color: white;">Strategic Recommendation</h2>
            <h1 style="margin: 0.5rem 0; font-size: 2.5rem; color: white;">{rec.recommendation}</h1>
            <p style="margin: 0; font-size: 1.2rem; opacity: 0.95;">
                Confidence Level: {rec.confidence_level:.0%}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Score cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_score_card("Risk Assessment", rec.overall_risk_score, "red", 10)
    
    with col2:
        render_score_card("Opportunity Potential", rec.overall_opportunity_score, "green", 10)
    
    with col3:
        ratio = rec.overall_opportunity_score / rec.overall_risk_score if rec.overall_risk_score > 0 else 0
        render_score_card("Risk/Reward Ratio", ratio, "blue", 3)
    
    st.markdown("---")
    
    # Tabs for detailed results
    tabs = st.tabs([
        "📊 Executive Summary",
        "⚠️ Risk Analysis",
        "🎁 Opportunity Analysis",
        "🎯 Evaluation Factors",
        "🔍 Research Insights"
    ])
    
    with tabs[0]:
        render_overview(state)
    
    with tabs[1]:
        render_risk_analysis(state)
    
    with tabs[2]:
        render_opportunity_analysis(state)
    
    with tabs[3]:
        render_factors(state)
    
    with tabs[4]:
        render_research(state)


def render_score_card(title: str, value: float, color: str, max_value: float):
    """Render a professional score card."""
    percentage = (value / max_value) * 100
    
    color_map = {
        "red": "#ef4444",
        "green": "#10b981",
        "blue": "#3b82f6"
    }
    
    bar_color = color_map.get(color, "#6366f1")
    
    st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid {bar_color};">
            <p style="margin: 0; color: #64748b; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">
                {title}
            </p>
            <h2 style="margin: 0.5rem 0; color: #1e293b; font-size: 2.5rem; font-weight: 700;">
                {value:.1f}<span style="font-size: 1.5rem; color: #64748b;">/{max_value:.0f}</span>
            </h2>
            <div style="background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden; margin-top: 0.5rem;">
                <div style="background: {bar_color}; height: 100%; width: {percentage}%; 
                            transition: width 0.3s ease;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_overview(state: AgentState):
    """Render overview tab."""
    rec = state.recommendation
    
    st.subheader("Risk-Reward Balance")
    st.info(rec.risk_reward_balance)
    
    st.subheader("Key Insights")
    for i, insight in enumerate(rec.key_insights, 1):
        st.markdown(f"**{i}.** {insight}")
    
    st.subheader("Next Steps")
    for action in rec.next_steps:
        priority_emoji = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }.get(action.priority.lower(), "⚪")
        
        st.markdown(
            f"{priority_emoji} **[{action.priority.upper()}]** {action.action}"
        )
        st.caption(f"Timeframe: {action.timeframe}")
    
    if rec.critical_assumptions:
        st.subheader("Critical Assumptions")
        for assumption in rec.critical_assumptions:
            st.markdown(f"• {assumption}")
    
    if rec.watch_signals:
        st.subheader("Watch Signals")
        for signal in rec.watch_signals:
            st.markdown(f"• {signal}")


def render_risk_analysis(state: AgentState):
    """Render risk analysis tab."""
    risk_output = state.risk_output
    
    st.subheader(f"Overall Risk: {risk_output.overall_risk_level:.1f}/10")
    st.write(risk_output.risk_summary)
    
    st.divider()
    
    # Risk scores table
    for risk in sorted(risk_output.risk_scores, key=lambda x: x.score, reverse=True):
        severity_color = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }.get(risk.severity.lower(), "⚪")
        
        with st.expander(
            f"{severity_color} {risk.factor_name}: {risk.score:.1f}/10 ({risk.severity.upper()})"
        ):
            st.write(risk.reasoning)


def render_opportunity_analysis(state: AgentState):
    """Render opportunity analysis tab."""
    opp_output = state.opportunity_output
    
    st.subheader(f"Overall Opportunity: {opp_output.overall_opportunity_level:.1f}/10")
    st.write(opp_output.opportunity_summary)
    
    st.divider()
    
    # Opportunity scores table
    for opp in sorted(opp_output.opportunity_scores, key=lambda x: x.score, reverse=True):
        potential_color = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "transformative": "🌟"
        }.get(opp.potential.lower(), "⚪")
        
        with st.expander(
            f"{potential_color} {opp.factor_name}: {opp.score:.1f}/10 ({opp.potential.upper()})"
        ):
            st.write(opp.reasoning)


def render_factors(state: AgentState):
    """Render evaluation factors tab."""
    planner_output = state.planner_output
    
    st.subheader("Decision Summary")
    st.write(planner_output.decision_summary)
    
    st.divider()
    
    st.subheader("Evaluation Factors")
    for factor in planner_output.factors:
        with st.expander(f"**{factor.name}** ({factor.category})"):
            st.write(factor.description)


def render_research(state: AgentState):
    """Render research insights tab."""
    research_output = state.research_output
    
    st.subheader("Overall Context")
    st.write(research_output.overall_context)
    
    st.divider()
    
    st.subheader("Factor Analysis")
    for analysis in research_output.analyses:
        with st.expander(f"**{analysis.factor_name}**"):
            st.write(analysis.insights)
            
            if analysis.data_points:
                st.markdown("**Key Data Points:**")
                for point in analysis.data_points:
                    st.markdown(f"• {point}")


def render_gauge(label: str, value: float, color: str):
    """Render a gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label},
        gauge={
            'axis': {'range': [None, 10]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 3], 'color': "lightgray"},
                {'range': [3, 7], 'color': "gray"},
                {'range': [7, 10], 'color': "darkgray"}
            ],
        }
    ))
    
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def render_error(error_message: str):
    """Render error message."""
    st.error(f"❌ Error: {error_message}")
    st.info("Please try again or check your configuration.")
