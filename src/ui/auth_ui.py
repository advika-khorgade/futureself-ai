"""Authentication UI components."""
import streamlit as st
from ..auth import AuthManager, init_db


def render_auth_page():
    """Render login/register page with stunning design."""
    # Initialize database
    init_db()
    
    # Custom CSS for beautiful auth page
    st.markdown("""
        <style>
        /* Animated gradient background */
        .stApp {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Auth container with glassmorphism */
        .auth-container {
            max-width: 480px;
            margin: 3rem auto;
            padding: 3rem;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.18);
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Header styling */
        .auth-header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        
        .auth-logo {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
            display: inline-block;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .auth-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -1px;
        }
        
        .auth-subtitle {
            color: #64748b;
            font-size: 1.1rem;
            margin: 0.5rem 0 0 0;
            font-weight: 500;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: #f1f5f9;
            padding: 8px;
            border-radius: 12px;
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            border-radius: 8px;
            padding: 0 24px;
            font-weight: 600;
            font-size: 1rem;
            background: transparent;
            border: none;
            color: #64748b;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        /* Input styling */
        .stTextInput input, .stTextArea textarea {
            border-radius: 12px !important;
            border: 2px solid #e2e8f0 !important;
            padding: 14px 16px !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            background: white !important;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
            transform: translateY(-2px);
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 16px 32px !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
            text-transform: uppercase !important;
        }
        
        .stButton button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        }
        
        .stButton button:active {
            transform: translateY(-1px) !important;
        }
        
        /* Alert styling */
        .stAlert {
            border-radius: 12px !important;
            border: none !important;
            padding: 16px 20px !important;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* Success alert */
        [data-baseweb="notification"][kind="success"] {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: white !important;
        }
        
        /* Error alert */
        [data-baseweb="notification"][kind="error"] {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
            color: white !important;
        }
        
        /* Info alert */
        [data-baseweb="notification"][kind="info"] {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
        }
        
        /* Form section headers */
        .form-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        /* Feature badges */
        .feature-badge {
            display: inline-block;
            padding: 8px 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 4px;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        /* Decorative elements */
        .decorative-circle {
            position: fixed;
            border-radius: 50%;
            opacity: 0.1;
            pointer-events: none;
        }
        
        .circle-1 {
            width: 300px;
            height: 300px;
            background: #667eea;
            top: -100px;
            right: -100px;
        }
        
        .circle-2 {
            width: 200px;
            height: 200px;
            background: #764ba2;
            bottom: -50px;
            left: -50px;
        }
        </style>
        
        <!-- Decorative circles -->
        <div class="decorative-circle circle-1"></div>
        <div class="decorative-circle circle-2"></div>
    """, unsafe_allow_html=True)
    
    # Header with animation
    st.markdown("""
        <div class="auth-header">
            <div class="auth-logo">🔮</div>
            <h1 class="auth-title">FutureSelf AI</h1>
            <p class="auth-subtitle">AI-Powered Decision Intelligence Platform</p>
            <div style="margin-top: 1.5rem;">
                <span class="feature-badge">🚀 Multi-Agent Analysis</span>
                <span class="feature-badge">🎯 Strategic Insights</span>
                <span class="feature-badge">⚡ Real-time Results</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs for login/register
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Register"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_register_form()
    
    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; color: rgba(255,255,255,0.8); font-size: 0.9rem;">
            <p>🔒 Your data is secure and encrypted</p>
            <p style="margin-top: 0.5rem;">© 2024 FutureSelf AI. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)


def render_login_form():
    """Render login form."""
    with st.form("login_form", clear_on_submit=False):
        st.markdown('<div class="form-header">👋 Welcome Back!</div>', unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username",
            label_visibility="collapsed"
        )
        st.caption("👤 Username")
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
            label_visibility="collapsed"
        )
        st.caption("🔑 Password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 Login",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            if not username or not password:
                st.error("⚠️ Please fill in all fields")
            else:
                with st.spinner("🔄 Logging in..."):
                    success, message, user_data = AuthManager.login_user(username, password)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        # Store user data in session state
                        st.session_state.authenticated = True
                        st.session_state.user = user_data
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")


def render_register_form():
    """Render registration form."""
    with st.form("register_form", clear_on_submit=True):
        st.markdown('<div class="form-header">✨ Create Your Account</div>', unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            placeholder="Choose a unique username",
            key="register_username",
            label_visibility="collapsed"
        )
        st.caption("👤 Username (min 3 characters)")
        
        email = st.text_input(
            "Email",
            placeholder="your.email@example.com",
            key="register_email",
            label_visibility="collapsed"
        )
        st.caption("📧 Email Address")
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
            key="register_password",
            label_visibility="collapsed"
        )
        st.caption("🔒 Password (min 8 chars, 1 uppercase, 1 lowercase, 1 number)")
        
        password_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="register_password_confirm",
            label_visibility="collapsed"
        )
        st.caption("✅ Confirm Password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "✨ Create Account",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            if not all([username, email, password, password_confirm]):
                st.error("⚠️ Please fill in all fields")
            elif password != password_confirm:
                st.error("❌ Passwords do not match")
            else:
                with st.spinner("🔄 Creating your account..."):
                    success, message = AuthManager.register_user(username, email, password)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.info("👉 Please switch to the Login tab to sign in")
                    else:
                        st.error(f"❌ {message}")


def render_user_menu():
    """Render user menu in sidebar."""
    if "user" in st.session_state:
        user = st.session_state.user
        
        with st.sidebar:
            st.markdown("---")
            
            # User profile card
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1rem;">
                    <div style="font-size: 2rem; text-align: center; margin-bottom: 0.5rem;">👤</div>
                    <div style="font-size: 1.2rem; font-weight: 700; text-align: center;">{user['username']}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9; text-align: center; margin-top: 0.3rem;">
                        📧 {user['email']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True, type="primary"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()


def check_authentication():
    """Check if user is authenticated."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    return st.session_state.authenticated
