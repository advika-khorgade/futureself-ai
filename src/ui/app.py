"""Streamlit dashboard for FutureSelf AI."""
import streamlit as st
from config import settings
from ..schemas import DecisionInput
from ..workflow import DecisionWorkflowRunner
from .components import (
    render_header,
    render_input_form,
    render_results,
    render_error,
    render_history_page,
    render_analytics_page,
    render_compare_page
)
from .auth_ui import render_auth_page, check_authentication, render_user_menu


def main():
    """Main Streamlit application."""
    # Page config
    st.set_page_config(
        page_title="FutureSelf AI - Decision Intelligence Platform",
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for professional look
    st.markdown("""
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Smooth animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        /* Apply animations to main content */
        .main .block-container {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Professional header styling with glassmorphism */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2.5rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            backdrop-filter: blur(10px);
            animation: slideIn 0.8s ease-out;
        }
        
        /* Enhanced card styling with depth */
        .stAlert {
            border-radius: 12px;
            border-left: 4px solid #6366f1;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Modern button styling with hover effects */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        
        .stButton>button:active {
            transform: translateY(-1px);
        }
        
        /* Enhanced input styling */
        .stTextArea textarea, .stTextInput input {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
            transform: translateY(-2px);
        }
        
        /* Smooth progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }
        
        /* Enhanced metric cards with glassmorphism */
        [data-testid="stMetricValue"] {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stMetric {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.18);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stMetric:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
        
        /* Modern tabs with smooth transitions */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: rgba(241, 245, 249, 0.8);
            backdrop-filter: blur(10px);
            padding: 8px;
            border-radius: 16px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Enhanced expander with smooth animation */
        .streamlit-expanderHeader {
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
        }
        
        .streamlit-expanderHeader:hover {
            background: rgba(102, 126, 234, 0.1);
            transform: translateX(5px);
        }
        
        /* Loading skeleton animation */
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        
        .loading-skeleton {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 1000px 100%;
            animation: shimmer 2s infinite;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
            backdrop-filter: blur(10px);
        }
        
        /* Radio button styling */
        .stRadio > label {
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        /* Enhanced selectbox */
        .stSelectbox > div > div {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        render_auth_page()
        return
    
    # Render user menu
    render_user_menu()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 📊 Navigation")
        page = st.radio(
            "Go to",
            ["🔮 New Analysis", "📚 History", "📈 Analytics", "⚖️ Compare"],
            label_visibility="collapsed"
        )
    
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        st.error("⚙️ Configuration Required")
        st.info(str(e))
        st.stop()
    
    # Route to appropriate page
    if page == "📚 History":
        render_history_page()
        return
    
    if page == "📈 Analytics":
        render_analytics_page()
        return
    
    if page == "⚖️ Compare":
        render_compare_page()
        return
    
    # Header
    render_header()
    
    # Main content
    decision_input = render_input_form()
    
    # Check if we have a stored analysis result (for chat persistence)
    if 'current_analysis_result' in st.session_state and not decision_input:
        result = st.session_state['current_analysis_result']
        if not result.error:
            render_results(result)
            return
    
    if decision_input:
        # Clear previous decision saved flag and chat history for new analysis
        if 'decision_saved' in st.session_state:
            del st.session_state['decision_saved']
        if 'chat_history' in st.session_state:
            del st.session_state['chat_history']
        if 'current_analysis_state' in st.session_state:
            del st.session_state['current_analysis_state']
        
        # Store decision input in session state
        st.session_state['current_decision_input'] = decision_input
        
        # Show expected time
        st.info("⏱️ Analysis typically completes in 1-2 minutes")
        
        # Initialize workflow with progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            runner = DecisionWorkflowRunner(
                model_name=settings.MODEL_NAME,
                temperature=settings.TEMPERATURE
            )
            
            # Execute workflow with progress updates
            status_text.text("🎯 Step 1/5: Planning evaluation factors...")
            progress_bar.progress(10)
            
            result = runner.run(
                decision_input,
                progress_callback=lambda step, progress: update_progress(
                    step, progress, status_text, progress_bar
                )
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Store result in session state
            st.session_state['current_analysis_result'] = result
            
            # Check for errors
            if result.error:
                render_error(result.error)
            else:
                # Render results
                render_results(result)
                
        except Exception as e:
            render_error(str(e))
        finally:
            # Clean up progress indicators
            progress_bar.empty()
            status_text.empty()


def update_progress(step: str, progress: int, status_text, progress_bar):
    """Update progress indicators."""
    status_text.text(step)
    progress_bar.progress(progress)


if __name__ == "__main__":
    main()
