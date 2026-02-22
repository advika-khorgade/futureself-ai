# FutureSelf AI - REST API Documentation

## 🚀 Overview

The FutureSelf AI REST API provides programmatic access to our multi-agent decision intelligence platform. Built with FastAPI, it offers high performance, automatic API documentation, and JWT authentication.

## 📍 Base URL

```
http://localhost:8000
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## 📚 API Endpoints

### Authentication

#### Register User
```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "john_doe"
}
```

#### Login
```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "john_doe"
}
```

### Decisions

#### Analyze Decision
```http
POST /api/v1/decisions/analyze
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "decision": "Should I switch careers from software engineering to AI research?",
  "context": "10 years experience in backend development",
  "timeframe": "1 year",
  "tags": ["career", "ai", "important"]
}
```

**Response:**
```json
{
  "id": 1,
  "decision": "Should I switch careers...",
  "recommendation": "Proceed with Caution",
  "confidence_level": 0.75,
  "risk_score": 6.5,
  "opportunity_score": 7.8,
  "key_insights": [
    "High potential for growth in AI field",
    "Significant learning curve required"
  ],
  "risk_reward_balance": "The opportunity outweighs the risks...",
  "next_steps": [
    {
      "action": "Research AI programs",
      "priority": "high",
      "timeframe": "1 month"
    }
  ]
}
```

#### Get Decision History
```http
GET /api/v1/decisions/history?limit=50&search=career
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (optional): Number of decisions to return (default: 50)
- `search` (optional): Search term to filter decisions

**Response:**
```json
{
  "decisions": [
    {
      "id": 1,
      "decision_text": "Should I switch careers...",
      "recommendation": "Proceed with Caution",
      "risk_score": 6.5,
      "opportunity_score": 7.8,
      "confidence_level": 0.75,
      "tags": ["career", "ai"],
      "created_at": "2024-02-22T10:30:00"
    }
  ],
  "count": 1
}
```

#### Get Specific Decision
```http
GET /api/v1/decisions/{decision_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "decision_text": "Should I switch careers...",
  "context": "10 years experience...",
  "timeframe": "1 year",
  "recommendation": "Proceed with Caution",
  "confidence_level": 0.75,
  "risk_score": 6.5,
  "opportunity_score": 7.8,
  "tags": ["career", "ai"],
  "created_at": "2024-02-22T10:30:00",
  "full_analysis": {
    "planner": {...},
    "research": {...},
    "risk": {...},
    "opportunity": {...},
    "recommendation": {...}
  }
}
```

#### Delete Decision
```http
DELETE /api/v1/decisions/{decision_id}
Authorization: Bearer <token>
```

**Response:** 204 No Content

### Analytics

#### Get Analytics Summary
```http
GET /api/v1/analytics/summary
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_decisions": 15,
  "avg_risk_score": 5.8,
  "avg_opportunity_score": 6.9,
  "avg_confidence": 0.72
}
```

### Health Check

#### Health Status
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-22T10:30:00"
}
```

## 🔧 Running the API

### Start the API Server

```bash
python run_api.py
```

The API will be available at `http://localhost:8000`

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 💻 Example Usage

### Python Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Register/Login
response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
    "username": "john_doe",
    "password": "SecurePass123"
})
token = response.json()["access_token"]

# Analyze Decision
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/api/v1/decisions/analyze",
    headers=headers,
    json={
        "decision": "Should I invest in cryptocurrency?",
        "context": "Have $10k savings",
        "timeframe": "6 months",
        "tags": ["finance", "investment"]
    }
)
result = response.json()
print(f"Recommendation: {result['recommendation']}")
print(f"Risk Score: {result['risk_score']}/10")
print(f"Opportunity Score: {result['opportunity_score']}/10")

# Get History
response = requests.get(
    f"{BASE_URL}/api/v1/decisions/history",
    headers=headers
)
decisions = response.json()["decisions"]
print(f"Total decisions: {len(decisions)}")
```

### cURL Example

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","password":"SecurePass123"}'

# Analyze Decision
curl -X POST http://localhost:8000/api/v1/decisions/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "Should I start a business?",
    "context": "Have business idea and some savings",
    "tags": ["business", "entrepreneurship"]
  }'

# Get History
curl -X GET http://localhost:8000/api/v1/decisions/history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Login
const login = async () => {
  const response = await axios.post(`${BASE_URL}/api/v1/auth/login`, {
    username: 'john_doe',
    password: 'SecurePass123'
  });
  return response.data.access_token;
};

// Analyze Decision
const analyzeDecision = async (token) => {
  const response = await axios.post(
    `${BASE_URL}/api/v1/decisions/analyze`,
    {
      decision: 'Should I learn a new programming language?',
      context: 'Currently know Python and JavaScript',
      tags: ['career', 'learning']
    },
    {
      headers: { Authorization: `Bearer ${token}` }
    }
  );
  return response.data;
};

// Usage
(async () => {
  const token = await login();
  const result = await analyzeDecision(token);
  console.log('Recommendation:', result.recommendation);
  console.log('Risk Score:', result.risk_score);
})();
```

## 🔒 Security

- All passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes
- CORS is enabled (configure for production)
- Use HTTPS in production
- Store JWT_SECRET_KEY securely in environment variables

## ⚠️ Error Responses

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

**Common Status Codes:**
- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

## 📊 Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production use.

## 🚀 Deployment

### Environment Variables

Create a `.env` file:

```env
JWT_SECRET_KEY=your-super-secret-key-change-this
GROQ_API_KEY=your-groq-api-key
LLM_PROVIDER=groq
MODEL_NAME=llama-3.3-70b-versatile
```

### Production Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn (production)
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 Notes

- The API uses the same backend as the Streamlit UI
- All decisions are stored in the SQLite database
- Analysis uses the multi-agent AI system with Groq
- Tokens are stateless (JWT)

## 🤝 Support

For issues or questions, please open an issue on GitHub.

---

**Made with ❤️ by the FutureSelf AI team**
