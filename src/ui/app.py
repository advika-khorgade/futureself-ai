"""Streamlit dashboard for FutureSelf AI."""
import streamlit as st
from config import settings
from ..schemas import DecisionInput
from ..workflow import DecisionWorkflowRunner
from .components import (
    render_header,
    render_input_form,
    render_results,
    render_error
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
        
        /* Professional header styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Card styling */
        .stAlert {
            border-radius: 8px;
            border-left: 4px solid #6366f1;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Input styling */
        .stTextArea textarea, .stTextInput input {
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            transition: border-color 0.3s ease;
        }
        
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 12px 24px;
            font-weight: 600;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            border-radius: 8px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        render_auth_page()
        return
    
    # Render user menu
    render_user_menu()
    
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        st.error("⚙️ Configuration Required")
        st.info(str(e))
        st.stop()
    
    # Header
    render_header()
    
    # Main content
    decision_input = render_input_form()
    
    if decision_input:
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
