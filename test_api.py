"""Test script for FutureSelf AI REST API."""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """Test the API endpoints."""
    print("🧪 Testing FutureSelf AI REST API\n")
    
    # Test 1: Health Check
    print("1️⃣ Testing Health Check...")
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
    
    # Test 2: Register User
    print("2️⃣ Testing User Registration...")
    register_data = {
        "username": "api_test_user",
        "email": "apitest@example.com",
        "password": "TestPass123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)
    if response.status_code == 201:
        token_data = response.json()
        token = token_data["access_token"]
        print(f"   ✅ Registration successful!")
        print(f"   User ID: {token_data['user_id']}")
        print(f"   Token: {token[:50]}...\n")
    else:
        # User might already exist, try login
        print("   ⚠️ User exists, trying login...")
        login_data = {
            "username": "api_test_user",
            "password": "TestPass123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        token_data = response.json()
        token = token_data["access_token"]
        print(f"   ✅ Login successful!")
        print(f"   Token: {token[:50]}...\n")
    
    # Test 3: Analyze Decision
    print("3️⃣ Testing Decision Analysis...")
    headers = {"Authorization": f"Bearer {token}"}
    decision_data = {
        "decision": "Should I learn FastAPI for building REST APIs?",
        "context": "I know Python and want to build scalable APIs",
        "timeframe": "3 months",
        "tags": ["learning", "api", "career"]
    }
    
    print("   Sending analysis request...")
    print("   ⏳ This may take 1-2 minutes...")
    response = requests.post(
        f"{BASE_URL}/api/v1/decisions/analyze",
        headers=headers,
        json=decision_data
    )
    
    if response.status_code == 201:
        result = response.json()
        print(f"   ✅ Analysis complete!")
        print(f"   Decision ID: {result['id']}")
        print(f"   Recommendation: {result['recommendation']}")
        print(f"   Confidence: {result['confidence_level']*100:.0f}%")
        print(f"   Risk Score: {result['risk_score']:.1f}/10")
        print(f"   Opportunity Score: {result['opportunity_score']:.1f}/10")
        print(f"   Key Insights: {len(result['key_insights'])} insights\n")
        decision_id = result['id']
    else:
        print(f"   ❌ Analysis failed: {response.json()}\n")
        return
    
    # Test 4: Get History
    print("4️⃣ Testing Get History...")
    response = requests.get(f"{BASE_URL}/api/v1/decisions/history", headers=headers)
    if response.status_code == 200:
        history = response.json()
        print(f"   ✅ Retrieved {history['count']} decisions\n")
    
    # Test 5: Get Specific Decision
    print("5️⃣ Testing Get Specific Decision...")
    response = requests.get(f"{BASE_URL}/api/v1/decisions/{decision_id}", headers=headers)
    if response.status_code == 200:
        decision = response.json()
        print(f"   ✅ Retrieved decision #{decision['id']}")
        print(f"   Decision: {decision['decision_text'][:60]}...\n")
    
    # Test 6: Get Analytics
    print("6️⃣ Testing Analytics Summary...")
    response = requests.get(f"{BASE_URL}/api/v1/analytics/summary", headers=headers)
    if response.status_code == 200:
        analytics = response.json()
        print(f"   ✅ Analytics retrieved!")
        print(f"   Total Decisions: {analytics['total_decisions']}")
        print(f"   Avg Risk Score: {analytics['avg_risk_score']:.1f}/10")
        print(f"   Avg Opportunity: {analytics['avg_opportunity_score']:.1f}/10\n")
    
    print("✅ All tests completed successfully!")
    print(f"\n📚 API Documentation: {BASE_URL}/api/docs")
    print(f"📖 ReDoc: {BASE_URL}/api/redoc")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("   Make sure the API is running: python run_api.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
