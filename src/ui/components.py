"""Streamlit UI components."""
import streamlit as st
import plotly.graph_objects as go
from typing import Optional
from datetime import datetime
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
            
            tags = st.text_input(
                "Tags (Optional)",
                placeholder="Example: career, finance, important",
                help="Add comma-separated tags to categorize this decision"
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
            
            # Store tags in session state for later use
            if tags:
                st.session_state['decision_tags'] = [tag.strip() for tag in tags.split(',') if tag.strip()]
            else:
                st.session_state['decision_tags'] = []
            
            return DecisionInput(
                decision=decision,
                context=context if context else None,
                timeframe=timeframe if timeframe else None
            )
    
    return None


def render_results(state: AgentState):
    """Render analysis results."""
    st.success("✅ Analysis Complete!")
    
    # Save to history
    from ..history import HistoryManager
    user = st.session_state.get('user')
    tags = st.session_state.get('decision_tags', [])
    
    if user and 'decision_saved' not in st.session_state:
        user_id = user.get('id')
        if user_id:
            try:
                decision_id = HistoryManager.save_decision(user_id, state, tags)
                st.session_state['decision_saved'] = True
                st.session_state['current_decision_id'] = decision_id
            except Exception as e:
                st.warning(f"Note: Could not save to history: {str(e)}")
    
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
    
    # Export and Chat section
    render_export_and_chat(state)


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



def render_export_and_chat(state: AgentState):
    """Render export and chat interface."""
    from ..chat import ChatAssistant
    from ..export import PDFExporter
    
    st.markdown("---")
    
    # Export section
    st.markdown("### 📄 Export Analysis")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📥 Download PDF", type="secondary", use_container_width=True):
            try:
                user = st.session_state.get('user', {})
                username = user.get('username', 'User')
                
                pdf_buffer = PDFExporter.export_decision(state, username)
                
                st.download_button(
                    label="💾 Save PDF File",
                    data=pdf_buffer,
                    file_name=f"decision_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
                st.success("✅ PDF generated! Click the button above to save.")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    st.markdown("---")
    
    # Chat interface
    st.markdown("### 💬 Ask Follow-up Questions")
    st.markdown("Have questions about this analysis? Ask our AI assistant!")
    
    # Store state in session for persistence
    if 'current_analysis_state' not in st.session_state:
        st.session_state.current_analysis_state = state
    
    # Initialize chat assistant
    if 'chat_assistant' not in st.session_state:
        st.session_state.chat_assistant = ChatAssistant()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about this decision..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Use stored state for consistency
                    current_state = st.session_state.current_analysis_state
                    response = st.session_state.chat_assistant.ask_question(current_state, prompt)
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    
                    # Check if it's a rate limit error
                    if "429" in str(e) or "rate limit" in str(e).lower():
                        error_msg = "⚠️ API rate limit reached. Please wait a few minutes before asking more questions, or try again tomorrow when your rate limit resets."
                    
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})


def render_history_page():
    """Render decision history page."""
    from ..history import HistoryManager
    from ..auth.auth_manager import AuthManager
    import json
    
    st.markdown("""
        <div class="main-header">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">📚 Decision History</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                Review your past analyses and insights
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get current user
    user = st.session_state.get('user')
    if not user:
        st.error("Please log in to view history")
        return
    
    user_id = user.get('id')
    if not user_id:
        st.error("User ID not found. Please log in again.")
        return
    
    # Search and filter controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search decisions", placeholder="Search by decision text...")
    
    with col2:
        # Get all tags for this user
        all_tags = HistoryManager.get_user_tags(user_id)
        selected_tag = st.selectbox("🏷️ Filter by tag", ["All"] + all_tags)
    
    with col3:
        sort_by = st.selectbox("📊 Sort by", ["Newest First", "Oldest First", "Highest Risk", "Highest Opportunity"])
    
    # Get decisions
    try:
        if search_query:
            decisions = HistoryManager.search_decisions(user_id, search_query)
        elif selected_tag and selected_tag != "All":
            decisions = HistoryManager.get_decisions_by_tag(user_id, selected_tag)
        else:
            decisions = HistoryManager.get_user_history(user_id)
        
        # Sort decisions
        if sort_by == "Oldest First":
            decisions = sorted(decisions, key=lambda x: x.created_at if hasattr(x, 'created_at') else x['created_at'])
        elif sort_by == "Highest Risk":
            decisions = sorted(decisions, key=lambda x: (x.risk_score if hasattr(x, 'risk_score') else x.get('risk_score')) or 0, reverse=True)
        elif sort_by == "Highest Opportunity":
            decisions = sorted(decisions, key=lambda x: (x.opportunity_score if hasattr(x, 'opportunity_score') else x.get('opportunity_score')) or 0, reverse=True)
        else:  # Newest First
            decisions = sorted(decisions, key=lambda x: x.created_at if hasattr(x, 'created_at') else x['created_at'], reverse=True)
        
        if not decisions:
            st.info("📭 No decisions found. Start by creating your first analysis!")
            return
        
        st.markdown(f"### Found {len(decisions)} decision(s)")
        
        # Display decisions
        for decision in decisions:
            # Handle both dict and object types
            if isinstance(decision, dict):
                decision_text = decision.get('decision_text', '')
                created_at = decision.get('created_at')
                recommendation = decision.get('recommendation')
                risk_score = decision.get('risk_score')
                opportunity_score = decision.get('opportunity_score')
                tags = decision.get('tags', [])
                if isinstance(tags, str):
                    tags = tags.split(',') if tags else []
                context = decision.get('context')
                timeframe = decision.get('timeframe')
                full_analysis = decision.get('full_analysis')
                decision_id = decision.get('id')
            else:
                decision_text = decision.decision_text
                created_at = decision.created_at
                recommendation = decision.recommendation
                risk_score = decision.risk_score
                opportunity_score = decision.opportunity_score
                tags = decision.tags.split(',') if decision.tags else []
                context = decision.context
                timeframe = decision.timeframe
                full_analysis = decision.full_analysis
                decision_id = decision.id
            
            with st.expander(
                f"**{decision_text[:80]}...** - {created_at.strftime('%Y-%m-%d %H:%M')}",
                expanded=False
            ):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Recommendation", recommendation or "N/A")
                
                with col2:
                    st.metric("Risk Score", f"{risk_score:.1f}/10" if risk_score else "N/A")
                
                with col3:
                    st.metric("Opportunity Score", f"{opportunity_score:.1f}/10" if opportunity_score else "N/A")
                
                if tags:
                    st.markdown("**Tags:** " + " ".join([f"`{tag}`" for tag in tags]))
                
                if context:
                    st.markdown("**Context:**")
                    st.write(context)
                
                if timeframe:
                    st.markdown(f"**Timeframe:** {timeframe}")
                
                # Show full analysis button
                if full_analysis:
                    if st.button(f"📊 View Full Analysis", key=f"view_{decision_id}"):
                        st.session_state[f'show_analysis_{decision_id}'] = not st.session_state.get(f'show_analysis_{decision_id}', False)
                    
                    if st.session_state.get(f'show_analysis_{decision_id}', False):
                        try:
                            analysis = json.loads(full_analysis)
                            
                            # Display in a prettier format
                            st.markdown("---")
                            st.markdown("### 📊 Detailed Analysis")
                            
                            # Recommendation
                            if 'recommendation' in analysis:
                                rec = analysis['recommendation']
                                st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                                padding: 1.5rem; border-radius: 12px; color: white; margin: 1rem 0;">
                                        <h3 style="margin: 0; color: white;">Recommendation: {rec.get('recommendation', 'N/A')}</h3>
                                        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                                            Confidence: {rec.get('confidence_level', 0)*100:.0f}%
                                        </p>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                if rec.get('key_insights'):
                                    st.markdown("**Key Insights:**")
                                    for insight in rec['key_insights']:
                                        st.markdown(f"• {insight}")
                                
                                if rec.get('risk_reward_balance'):
                                    st.markdown("**Risk-Reward Balance:**")
                                    st.info(rec['risk_reward_balance'])
                            
                            # Evaluation Factors
                            if 'planner' in analysis and 'factors' in analysis['planner']:
                                with st.expander("🎯 Evaluation Factors", expanded=False):
                                    for factor in analysis['planner']['factors']:
                                        st.markdown(f"**{factor['name']}** ({factor['category']})")
                                        st.write(factor['description'])
                                        st.markdown("---")
                            
                            # Risk Analysis
                            if 'risk' in analysis:
                                with st.expander("⚠️ Risk Analysis", expanded=False):
                                    risk = analysis['risk']
                                    st.metric("Overall Risk Score", f"{risk.get('overall_risk_level', 0):.1f}/10")
                                    st.write(risk.get('risk_summary', ''))
                                    
                                    if risk.get('risk_scores'):
                                        st.markdown("**Risk Scores by Factor:**")
                                        for score in risk['risk_scores']:
                                            st.markdown(f"• **{score['factor_name']}**: {score['score']:.1f}/10 ({score['severity']})")
                            
                            # Opportunity Analysis
                            if 'opportunity' in analysis:
                                with st.expander("🎁 Opportunity Analysis", expanded=False):
                                    opp = analysis['opportunity']
                                    st.metric("Overall Opportunity Score", f"{opp.get('overall_opportunity_level', 0):.1f}/10")
                                    st.write(opp.get('opportunity_summary', ''))
                                    
                                    if opp.get('opportunity_scores'):
                                        st.markdown("**Opportunity Scores by Factor:**")
                                        for score in opp['opportunity_scores']:
                                            st.markdown(f"• **{score['factor_name']}**: {score['score']:.1f}/10 ({score['potential']})")
                            
                            # Raw JSON (collapsed by default)
                            with st.expander("🔍 View Raw JSON Data", expanded=False):
                                st.json(analysis)
                                
                        except Exception as e:
                            st.error(f"Error displaying analysis: {str(e)}")
                            with st.expander("View Raw Data"):
                                st.text(full_analysis)
                
                # Delete button
                if st.button(f"🗑️ Delete", key=f"delete_{decision_id}"):
                    if HistoryManager.delete_decision(decision_id, user_id):
                        st.success("Decision deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete decision")
    
    except Exception as e:
        st.error(f"Error loading history: {str(e)}")



def render_analytics_page():
    """Render analytics dashboard with insights and visualizations."""
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import pandas as pd
    from datetime import datetime, timedelta
    from ..history import HistoryManager
    
    st.markdown("""
        <div class="main-header">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">📈 Analytics Dashboard</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                Insights from your decision-making journey
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get current user
    user = st.session_state.get('user')
    if not user:
        st.error("Please log in to view analytics")
        return
    
    user_id = user.get('id')
    if not user_id:
        st.error("User ID not found. Please log in again.")
        return
    
    # Get all decisions
    try:
        decisions = HistoryManager.get_user_history(user_id, limit=1000)
        
        if not decisions:
            st.info("📭 No decisions yet. Create your first analysis to see insights!")
            return
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(decisions)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['date'] = df['created_at'].dt.date
        
        # Summary Statistics
        st.markdown("### 📊 Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Decisions",
                len(df),
                help="Total number of decisions analyzed"
            )
        
        with col2:
            avg_risk = df['risk_score'].mean() if 'risk_score' in df else 0
            st.metric(
                "Avg Risk Score",
                f"{avg_risk:.1f}/10",
                help="Average risk across all decisions"
            )
        
        with col3:
            avg_opp = df['opportunity_score'].mean() if 'opportunity_score' in df else 0
            st.metric(
                "Avg Opportunity",
                f"{avg_opp:.1f}/10",
                help="Average opportunity across all decisions"
            )
        
        with col4:
            avg_conf = df['confidence_level'].mean() if 'confidence_level' in df else 0
            st.metric(
                "Avg Confidence",
                f"{avg_conf*100:.0f}%",
                help="Average confidence in recommendations"
            )
        
        st.markdown("---")
        
        # Charts in tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📅 Timeline",
            "🎯 Risk vs Opportunity",
            "📋 Recommendations",
            "🏷️ Tags"
        ])
        
        with tab1:
            st.markdown("### Decision Timeline")
            
            # Decisions over time
            timeline_df = df.groupby('date').size().reset_index(name='count')
            
            fig = px.line(
                timeline_df,
                x='date',
                y='count',
                title='Decisions Over Time',
                labels={'date': 'Date', 'count': 'Number of Decisions'},
                markers=True
            )
            fig.update_traces(line_color='#667eea', line_width=3, marker=dict(size=8))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk and Opportunity trends
            st.markdown("### Risk & Opportunity Trends")
            
            daily_stats = df.groupby('date').agg({
                'risk_score': 'mean',
                'opportunity_score': 'mean'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_stats['date'],
                y=daily_stats['risk_score'],
                name='Risk Score',
                line=dict(color='#ef4444', width=3),
                mode='lines+markers'
            ))
            fig.add_trace(go.Scatter(
                x=daily_stats['date'],
                y=daily_stats['opportunity_score'],
                name='Opportunity Score',
                line=dict(color='#10b981', width=3),
                mode='lines+markers'
            ))
            fig.update_layout(
                title='Average Risk & Opportunity Over Time',
                xaxis_title='Date',
                yaxis_title='Score (0-10)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("### Risk vs Opportunity Analysis")
            
            # Scatter plot
            fig = px.scatter(
                df,
                x='risk_score',
                y='opportunity_score',
                size='confidence_level',
                color='recommendation',
                hover_data=['decision_text'],
                title='Risk-Opportunity Matrix',
                labels={
                    'risk_score': 'Risk Score',
                    'opportunity_score': 'Opportunity Score',
                    'recommendation': 'Recommendation'
                }
            )
            
            # Add quadrant lines
            fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add quadrant labels
            fig.add_annotation(x=2.5, y=7.5, text="Low Risk<br>High Opportunity", showarrow=False, opacity=0.5)
            fig.add_annotation(x=7.5, y=7.5, text="High Risk<br>High Opportunity", showarrow=False, opacity=0.5)
            fig.add_annotation(x=2.5, y=2.5, text="Low Risk<br>Low Opportunity", showarrow=False, opacity=0.5)
            fig.add_annotation(x=7.5, y=2.5, text="High Risk<br>Low Opportunity", showarrow=False, opacity=0.5)
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Distribution charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    df,
                    x='risk_score',
                    nbins=20,
                    title='Risk Score Distribution',
                    labels={'risk_score': 'Risk Score', 'count': 'Frequency'},
                    color_discrete_sequence=['#ef4444']
                )
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.histogram(
                    df,
                    x='opportunity_score',
                    nbins=20,
                    title='Opportunity Score Distribution',
                    labels={'opportunity_score': 'Opportunity Score', 'count': 'Frequency'},
                    color_discrete_sequence=['#10b981']
                )
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("### Recommendation Breakdown")
            
            # Recommendation distribution
            rec_counts = df['recommendation'].value_counts().reset_index()
            rec_counts.columns = ['recommendation', 'count']
            
            fig = px.pie(
                rec_counts,
                values='count',
                names='recommendation',
                title='Decision Recommendations',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            # Confidence by recommendation
            st.markdown("### Confidence Levels by Recommendation")
            
            fig = px.box(
                df,
                x='recommendation',
                y='confidence_level',
                title='Confidence Distribution by Recommendation Type',
                labels={'confidence_level': 'Confidence Level', 'recommendation': 'Recommendation'},
                color='recommendation'
            )
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.markdown("### Tag Analysis")
            
            # Extract all tags
            all_tags = []
            for tags in df['tags']:
                if tags:
                    all_tags.extend(tags)
            
            if all_tags:
                tag_counts = pd.Series(all_tags).value_counts().head(15)
                
                fig = px.bar(
                    x=tag_counts.values,
                    y=tag_counts.index,
                    orientation='h',
                    title='Top 15 Most Used Tags',
                    labels={'x': 'Count', 'y': 'Tag'},
                    color=tag_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Tag cloud style display
                st.markdown("### Tag Cloud")
                tag_html = " ".join([
                    f'<span style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
                    f'color: white; padding: 8px 16px; margin: 4px; border-radius: 20px; font-size: {min(24, 12 + count)}px;">'
                    f'{tag} ({count})</span>'
                    for tag, count in tag_counts.items()
                ])
                st.markdown(f'<div style="line-height: 2.5;">{tag_html}</div>', unsafe_allow_html=True)
            else:
                st.info("No tags found. Start adding tags to your decisions!")
        
        # Insights section
        st.markdown("---")
        st.markdown("### 💡 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Most common recommendation
            most_common_rec = df['recommendation'].mode()[0] if len(df) > 0 else "N/A"
            st.info(f"**Most Common Recommendation:** {most_common_rec}")
            
            # Highest risk decision
            if 'risk_score' in df and len(df) > 0:
                highest_risk = df.loc[df['risk_score'].idxmax()]
                st.warning(f"**Highest Risk Decision:** {highest_risk['decision_text'][:60]}... ({highest_risk['risk_score']:.1f}/10)")
        
        with col2:
            # Best opportunity
            if 'opportunity_score' in df and len(df) > 0:
                best_opp = df.loc[df['opportunity_score'].idxmax()]
                st.success(f"**Best Opportunity:** {best_opp['decision_text'][:60]}... ({best_opp['opportunity_score']:.1f}/10)")
            
            # Decision frequency
            days_active = (df['created_at'].max() - df['created_at'].min()).days + 1
            decisions_per_day = len(df) / days_active if days_active > 0 else 0
            st.metric("Decision Frequency", f"{decisions_per_day:.1f} per day")
    
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")
        import traceback
        st.code(traceback.format_exc())



def render_compare_page():
    """Render decision comparison page."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import pandas as pd
    from ..history import HistoryManager
    
    st.markdown("""
        <div class="main-header">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">⚖️ Compare Decisions</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                Compare multiple decisions side-by-side
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get current user
    user = st.session_state.get('user')
    if not user:
        st.error("Please log in to compare decisions")
        return
    
    user_id = user.get('id')
    if not user_id:
        st.error("User ID not found. Please log in again.")
        return
    
    # Get all decisions
    try:
        decisions = HistoryManager.get_user_history(user_id, limit=100)
        
        if len(decisions) < 2:
            st.info("📭 You need at least 2 decisions to compare. Create more analyses first!")
            return
        
        # Create decision options for selection
        decision_options = {
            f"{d['decision_text'][:60]}... ({d['created_at'].strftime('%Y-%m-%d')})": d
            for d in decisions
        }
        
        st.markdown("### Select Decisions to Compare")
        st.markdown("Choose 2-3 decisions to compare side-by-side")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            decision1_key = st.selectbox(
                "Decision 1",
                options=list(decision_options.keys()),
                key="compare_d1"
            )
        
        with col2:
            decision2_key = st.selectbox(
                "Decision 2",
                options=[k for k in decision_options.keys() if k != decision1_key],
                key="compare_d2"
            )
        
        with col3:
            decision3_key = st.selectbox(
                "Decision 3 (Optional)",
                options=["None"] + [k for k in decision_options.keys() if k not in [decision1_key, decision2_key]],
                key="compare_d3"
            )
        
        # Get selected decisions
        selected_decisions = [
            decision_options[decision1_key],
            decision_options[decision2_key]
        ]
        
        if decision3_key != "None":
            selected_decisions.append(decision_options[decision3_key])
        
        if st.button("🔍 Compare Decisions", type="primary", use_container_width=True):
            st.markdown("---")
            st.markdown("### 📊 Comparison Results")
            
            # Create comparison DataFrame
            comparison_data = []
            for i, d in enumerate(selected_decisions, 1):
                comparison_data.append({
                    'Decision': f"Decision {i}",
                    'Text': d['decision_text'][:50] + "...",
                    'Recommendation': d['recommendation'],
                    'Risk Score': d['risk_score'] or 0,
                    'Opportunity Score': d['opportunity_score'] or 0,
                    'Confidence': (d['confidence_level'] or 0) * 100,
                    'Date': d['created_at'].strftime('%Y-%m-%d')
                })
            
            df = pd.DataFrame(comparison_data)
            
            # Determine winner
            df['Overall Score'] = df['Opportunity Score'] - df['Risk Score']
            winner_idx = df['Overall Score'].idxmax()
            winner = df.loc[winner_idx, 'Decision']
            
            # Display winner
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                            padding: 2rem; border-radius: 16px; color: white; text-align: center; margin: 2rem 0;">
                    <h2 style="margin: 0; color: white;">🏆 Winner: {winner}</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem;">
                        Best Risk-Opportunity Balance
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Score comparison chart
            st.markdown("### Score Comparison")
            
            fig = go.Figure()
            
            # Add bars for each decision
            fig.add_trace(go.Bar(
                name='Risk Score',
                x=df['Decision'],
                y=df['Risk Score'],
                marker_color='#ef4444',
                text=df['Risk Score'].round(1),
                textposition='auto',
            ))
            
            fig.add_trace(go.Bar(
                name='Opportunity Score',
                x=df['Decision'],
                y=df['Opportunity Score'],
                marker_color='#10b981',
                text=df['Opportunity Score'].round(1),
                textposition='auto',
            ))
            
            fig.add_trace(go.Bar(
                name='Confidence %',
                x=df['Decision'],
                y=df['Confidence'],
                marker_color='#3b82f6',
                text=df['Confidence'].round(0),
                textposition='auto',
                yaxis='y2'
            ))
            
            fig.update_layout(
                barmode='group',
                title='Score Comparison',
                xaxis_title='Decision',
                yaxis_title='Score (0-10)',
                yaxis2=dict(
                    title='Confidence (%)',
                    overlaying='y',
                    side='right',
                    range=[0, 100]
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk vs Opportunity scatter
            st.markdown("### Risk vs Opportunity Matrix")
            
            fig = go.Figure()
            
            for i, row in df.iterrows():
                fig.add_trace(go.Scatter(
                    x=[row['Risk Score']],
                    y=[row['Opportunity Score']],
                    mode='markers+text',
                    name=row['Decision'],
                    text=[row['Decision']],
                    textposition='top center',
                    marker=dict(
                        size=row['Confidence'] / 2,
                        line=dict(width=2, color='white')
                    )
                ))
            
            # Add quadrant lines
            fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)
            
            fig.update_layout(
                xaxis_title='Risk Score',
                yaxis_title='Opportunity Score',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=500,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed comparison table
            st.markdown("### Detailed Comparison")
            
            # Create styled table
            for i, d in enumerate(selected_decisions, 1):
                with st.expander(f"**Decision {i}: {d['decision_text'][:60]}...**", expanded=True):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Recommendation", d['recommendation'] or "N/A")
                    
                    with col2:
                        st.metric("Risk Score", f"{d['risk_score']:.1f}/10" if d['risk_score'] else "N/A")
                    
                    with col3:
                        st.metric("Opportunity", f"{d['opportunity_score']:.1f}/10" if d['opportunity_score'] else "N/A")
                    
                    with col4:
                        st.metric("Confidence", f"{(d['confidence_level'] or 0)*100:.0f}%")
                    
                    if d.get('context'):
                        st.markdown("**Context:**")
                        st.write(d['context'])
                    
                    if d.get('tags'):
                        tags = d['tags'] if isinstance(d['tags'], list) else d['tags'].split(',')
                        st.markdown("**Tags:** " + " ".join([f"`{tag}`" for tag in tags if tag]))
            
            # Summary insights
            st.markdown("---")
            st.markdown("### 💡 Comparison Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                highest_opp = df.loc[df['Opportunity Score'].idxmax()]
                st.success(f"**Highest Opportunity:** {highest_opp['Decision']} ({highest_opp['Opportunity Score']:.1f}/10)")
                
                lowest_risk = df.loc[df['Risk Score'].idxmin()]
                st.info(f"**Lowest Risk:** {lowest_risk['Decision']} ({lowest_risk['Risk Score']:.1f}/10)")
            
            with col2:
                highest_conf = df.loc[df['Confidence'].idxmax()]
                st.success(f"**Highest Confidence:** {highest_conf['Decision']} ({highest_conf['Confidence']:.0f}%)")
                
                avg_risk = df['Risk Score'].mean()
                avg_opp = df['Opportunity Score'].mean()
                st.metric("Average Risk/Opportunity", f"{avg_risk:.1f} / {avg_opp:.1f}")
    
    except Exception as e:
        st.error(f"Error loading comparison: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
