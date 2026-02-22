"""Test all backend features."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.auth.database import init_db, User, DecisionHistory
from src.auth.auth_manager import AuthManager
from src.history.history_manager import HistoryManager
from src.export.pdf_exporter import PDFExporter
from src.chat.chat_assistant import ChatAssistant
from src.schemas import (
    DecisionInput,
    AgentState,
    PlannerOutput,
    EvaluationFactor,
    ResearchOutput,
    FactorAnalysis,
    RiskOutput,
    RiskScore,
    OpportunityOutput,
    OpportunityScore,
    Recommendation,
    ActionItem
)


def test_database():
    """Test database initialization."""
    print("\n🧪 Testing Database...")
    try:
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False


def test_authentication():
    """Test user authentication."""
    print("\n🧪 Testing Authentication...")
    
    try:
        # Test registration
        success, message = AuthManager.register_user(
            username="testuser123",
            email="test@example.com",
            password="TestPass123"
        )
        
        if not success:
            print(f"⚠️ Registration: {message}")
        else:
            print(f"✅ Registration successful: {message}")
        
        # Test login
        success, message, user_data = AuthManager.login_user(
            username="testuser123",
            password="TestPass123"
        )
        
        if success:
            print(f"✅ Login successful: {message}")
            print(f"   User ID: {user_data['id']}")
            print(f"   Username: {user_data['username']}")
            print(f"   Email: {user_data['email']}")
            return True, user_data['id']
        else:
            print(f"❌ Login failed: {message}")
            return False, None
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False, None


def create_mock_state():
    """Create a mock decision state for testing."""
    decision_input = DecisionInput(
        decision="Should I switch careers from software engineering to AI research?",
        context="10 years experience in backend development",
        timeframe="1 year"
    )
    
    planner_output = PlannerOutput(
        factors=[
            EvaluationFactor(
                name="Financial Impact",
                description="Salary changes and financial stability",
                category="financial"
            ),
            EvaluationFactor(
                name="Career Growth",
                description="Long-term career prospects",
                category="professional"
            ),
            EvaluationFactor(
                name="Work-Life Balance",
                description="Impact on personal time and stress levels",
                category="personal"
            )
        ],
        decision_summary="Career transition from software engineering to AI research"
    )
    
    research_output = ResearchOutput(
        analyses=[
            FactorAnalysis(
                factor_name="Financial Impact",
                insights="Potential salary decrease initially but higher ceiling long-term",
                data_points=["Average AI researcher salary: $120k-180k"]
            ),
            FactorAnalysis(
                factor_name="Career Growth",
                insights="AI research is a rapidly growing field with high demand",
                data_points=["AI job postings up 74% year-over-year"]
            ),
            FactorAnalysis(
                factor_name="Work-Life Balance",
                insights="Research roles often offer flexible schedules",
                data_points=["Many research positions allow remote work"]
            )
        ],
        overall_context="Strong market demand for AI expertise"
    )
    
    risk_output = RiskOutput(
        risk_scores=[
            RiskScore(
                factor_name="Financial Impact",
                score=6.5,
                reasoning="Initial salary decrease and transition costs",
                severity="medium"
            ),
            RiskScore(
                factor_name="Career Growth",
                score=3.0,
                reasoning="Low risk given market demand",
                severity="low"
            ),
            RiskScore(
                factor_name="Work-Life Balance",
                score=4.0,
                reasoning="Research can be demanding but flexible",
                severity="low"
            )
        ],
        overall_risk_level=4.5,
        risk_summary="Moderate financial risk, low career and lifestyle risk"
    )
    
    opportunity_output = OpportunityOutput(
        opportunity_scores=[
            OpportunityScore(
                factor_name="Financial Impact",
                score=7.5,
                reasoning="Higher long-term earning potential",
                potential="high"
            ),
            OpportunityScore(
                factor_name="Career Growth",
                score=8.5,
                reasoning="Cutting-edge field with massive growth",
                potential="high"
            ),
            OpportunityScore(
                factor_name="Work-Life Balance",
                score=7.0,
                reasoning="Flexible work arrangements common in research",
                potential="high"
            )
        ],
        overall_opportunity_level=7.7,
        opportunity_summary="High opportunity across all factors"
    )
    
    recommendation = Recommendation(
        decision="Should I switch careers from software engineering to AI research?",
        recommendation="Proceed with Caution",
        confidence_level=0.75,
        key_insights=[
            "AI research offers significant long-term growth potential",
            "Initial financial impact requires planning",
            "Strong market demand reduces career risk"
        ],
        risk_reward_balance="Opportunities outweigh risks with proper planning",
        next_steps=[
            ActionItem(
                action="Build AI portfolio with side projects",
                priority="high",
                timeframe="3 months"
            ),
            ActionItem(
                action="Network with AI researchers",
                priority="medium",
                timeframe="Ongoing"
            )
        ],
        critical_assumptions=[
            "Market demand for AI continues to grow",
            "You can maintain financial stability during transition"
        ],
        watch_signals=[
            "Changes in AI job market",
            "Personal financial situation"
        ],
        overall_risk_score=4.5,
        overall_opportunity_score=7.7
    )
    
    state = AgentState(
        decision_input=decision_input,
        planner_output=planner_output,
        research_output=research_output,
        risk_output=risk_output,
        opportunity_output=opportunity_output,
        recommendation=recommendation,
        current_step="complete"
    )
    
    return state


def test_history_manager(user_id):
    """Test decision history management."""
    print("\n🧪 Testing History Manager...")
    
    try:
        # Create mock state
        print("   Creating mock state...")
        state = create_mock_state()
        print("   ✅ Mock state created")
        
        # Test saving decision
        print("   Saving decision to database...")
        decision_id = HistoryManager.save_decision(
            user_id=user_id,
            state=state,
            tags=["career", "ai", "important"]
        )
        print(f"✅ Decision saved with ID: {decision_id}")
        
        # Test retrieving history
        print("   Retrieving history...")
        history = HistoryManager.get_user_history(user_id=user_id)
        print(f"✅ Retrieved {len(history)} decisions from history")
        
        if history:
            print(f"   Latest decision: {history[0]['decision_text'][:50]}...")
            print(f"   Tags: {history[0]['tags']}")
        
        # Test search
        print("   Testing search...")
        search_results = HistoryManager.get_user_history(
            user_id=user_id,
            search="career"
        )
        print(f"✅ Search found {len(search_results)} results")
        
        # Test tag filter
        print("   Testing tag filter...")
        tag_results = HistoryManager.get_user_history(
            user_id=user_id,
            tags=["career"]
        )
        print(f"✅ Tag filter found {len(tag_results)} results")
        
        # Test get all tags
        print("   Getting all tags...")
        all_tags = HistoryManager.get_all_tags(user_id=user_id)
        print(f"✅ User has {len(all_tags)} unique tags: {all_tags}")
        
        # Test get by ID
        print("   Getting decision by ID...")
        decision = HistoryManager.get_decision_by_id(decision_id)
        if decision:
            print(f"✅ Retrieved decision by ID")
            print(f"   Recommendation: {decision['recommendation']}")
            print(f"   Confidence: {decision['confidence_level']:.0%}")
        
        return True, decision_id
        
    except Exception as e:
        print(f"❌ History manager test failed: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False, None


def test_pdf_export():
    """Test PDF export."""
    print("\n🧪 Testing PDF Export...")
    
    try:
        # Create mock state
        print("   Creating mock state...")
        state = create_mock_state()
        print("   ✅ Mock state created")
        
        # Export to PDF
        print("   Generating PDF...")
        pdf_buffer = PDFExporter.export_decision(state, username="testuser123")
        print("   ✅ PDF buffer created")
        
        # Check buffer
        pdf_size = len(pdf_buffer.getvalue())
        print(f"✅ PDF generated successfully")
        print(f"   Size: {pdf_size / 1024:.2f} KB")
        
        # Save to file for manual inspection
        print("   Saving PDF to file...")
        with open("test_export.pdf", "wb") as f:
            f.write(pdf_buffer.getvalue())
        print(f"✅ PDF saved to test_export.pdf for inspection")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF export test failed: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False


def test_chat_assistant():
    """Test AI chat assistant."""
    print("\n🧪 Testing AI Chat Assistant...")
    
    try:
        # Create mock state
        print("   Creating mock state...")
        state = create_mock_state()
        print("   ✅ Mock state created")
        
        # Initialize chat assistant
        print("   Initializing chat assistant...")
        chat = ChatAssistant()
        print("   ✅ Chat assistant initialized")
        
        # Test questions
        questions = [
            "What are the main risks of this decision?",
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n   Question {i}: {question}")
            try:
                print("   Sending to AI...")
                answer = chat.ask(question, state)
                print(f"   Answer: {answer[:100]}...")
                print(f"   ✅ Chat response received")
            except Exception as e:
                print(f"   ⚠️ Chat failed: {e}")
                print("   This is expected if API key is invalid or missing")
                import traceback
                print("\nFull traceback:")
                traceback.print_exc()
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Chat assistant test failed: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all backend tests."""
    print("=" * 60)
    print("🚀 BACKEND TESTING SUITE")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Database
    results['database'] = test_database()
    
    # Test 2: Authentication
    auth_success, user_id = test_authentication()
    results['authentication'] = auth_success
    
    if not user_id:
        print("\n⚠️ Skipping remaining tests (need user_id)")
        return results
    
    # Test 3: History Manager
    history_success, decision_id = test_history_manager(user_id)
    results['history'] = history_success
    
    # Test 4: PDF Export
    results['pdf_export'] = test_pdf_export()
    
    # Test 5: Chat Assistant
    results['chat'] = test_chat_assistant()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n🎯 Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is ready.")
    else:
        print("\n⚠️ Some tests failed. Check errors above.")
    
    return results


if __name__ == "__main__":
    run_all_tests()
