# 🔮 FutureSelf AI - Multi-Agent Decision Intelligence Platform

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**An AI-powered decision intelligence platform that uses 5 specialized agents to analyze decisions across multiple dimensions, providing strategic insights and actionable recommendations.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [API](#-rest-api) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 📸 Screenshots

### Main Dashboard
> *Screenshot: Add screenshot of main analysis page here*
<!-- ![Main Dashboard](screenshots/dashboard.png) -->

### Analytics Dashboard
> *Screenshot: Add screenshot of analytics page with charts here*
<!-- ![Analytics](screenshots/analytics.png) -->

### Decision Comparison
> *Screenshot: Add screenshot of comparison feature here*
<!-- ![Comparison](screenshots/comparison.png) -->

### API Documentation (Swagger UI)
> *Screenshot: Add screenshot of Swagger UI here*
<!-- ![API Docs](screenshots/api-docs.png) -->

---

## ✨ Features

### 🤖 Multi-Agent AI System
- **5 Specialized Agents** working in orchestrated workflow
- **Planner Agent** - Breaks decisions into evaluation factors
- **Research Agent** - Analyzes context and gathers insights  
- **Risk Agent** - Quantifies risks (0-10 scale)
- **Opportunity Agent** - Identifies opportunities (0-10 scale)
- **Strategist Agent** - Synthesizes final recommendations

### 📊 Comprehensive Analysis
- Multi-dimensional decision evaluation
- Risk-reward balance assessment
- Confidence scoring
- Strategic next steps with priorities
- Key insights and critical assumptions

### 🎨 Beautiful User Interface
- Modern, responsive design with glassmorphism effects
- Smooth animations and transitions
- Interactive charts and visualizations (Plotly)
- Dark-themed professional aesthetic
- Intuitive navigation

### 📈 Analytics Dashboard
- Decision timeline visualization
- Risk vs Opportunity matrix
- Recommendation breakdown (pie charts)
- Tag analysis and trends
- Personal insights and statistics

### ⚖️ Decision Comparison
- Compare 2-3 decisions side-by-side
- Visual score comparison charts
- Winner determination algorithm
- Detailed metrics comparison

### 🚀 REST API
- **FastAPI** backend with automatic documentation
- **JWT authentication** for secure access
- **9 endpoints** for full functionality
- **Swagger UI** for interactive testing
- **RESTful** design principles

### 🔐 Security & Authentication
- Secure user registration and login
- Password hashing with bcrypt
- JWT token-based authentication
- Session management
- User data isolation

### 📚 Additional Features
- **Decision History** - Save and review all analyses
- **Search & Filter** - Find decisions by text or tags
- **Decision Tags** - Categorize and organize decisions
- **AI Chat Assistant** - Ask follow-up questions about your analysis
- **PDF Export** - Download professional PDF reports of your analyses
- **Export Options** - PDF (available), CSV/JSON (planned)

---

## 🆕 Recent Updates

### Latest Release (v1.1.0)

**Bug Fixes & Improvements:**
- ✅ **PDF Export Fixed** - Download button now works correctly, generates professional PDF reports
- ✅ **Chat Interface Enhanced** - Follow-up questions now work properly with state persistence
- ✅ **Session Management** - Better handling of analysis state across page interactions
- ✅ **Error Handling** - Improved error messages for rate limits and API issues

**What's New:**
- PDF export generates timestamped files with complete analysis
- Chat assistant maintains conversation history during analysis session
- Automatic chat history clearing when starting new analysis
- Better rate limit handling with user-friendly messages

**Installation Note:**
If you're updating from a previous version, make sure to install the reportlab dependency:
```bash
pip install reportlab
```

---

## 🎯 Use Cases

- **Career Decisions** - Job changes, education, skill development
- **Financial Decisions** - Investments, major purchases, budgeting
- **Business Decisions** - Strategy, hiring, product development
- **Personal Decisions** - Relationships, health, lifestyle changes
- **Strategic Planning** - Long-term goals, risk assessment

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Streamlit / REST API)                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Workflow Orchestration                      │
│                  (LangGraph)                             │
└─────┬──────┬──────┬──────┬──────┬─────────────────────┘
      │      │      │      │      │
┌─────▼──┐ ┌─▼────┐ ┌▼────┐ ┌▼───┐ ┌▼─────────┐
│Planner │ │Research│ │Risk│ │Opp.│ │Strategist│
│ Agent  │ │ Agent  │ │Agt.│ │Agt.│ │  Agent   │
└────────┘ └────────┘ └────┘ └────┘ └──────────┘
      │         │        │      │         │
      └─────────┴────────┴──────┴─────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              LLM Provider (Groq)                         │
│           llama-3.3-70b-versatile                        │
└──────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **Python 3.10+** - Core language
- **FastAPI** - REST API framework
- **LangGraph** - Agent orchestration
- **LangChain** - LLM integration
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation

**Frontend:**
- **Streamlit** - Web interface
- **Plotly** - Interactive visualizations
- **Custom CSS** - Styling and animations

**AI/ML:**
- **Groq API** - LLM inference (free tier)
- **Llama 3.3 70B** - Language model
- **Multi-agent system** - Specialized agents

**Database:**
- **SQLite** - Local database
- **bcrypt** - Password hashing

**Authentication:**
- **JWT** - Token-based auth
- **python-jose** - JWT handling

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/advika-khorgade/futureself-ai.git
cd futureself-ai
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_api_key_here
```

5. **Run the application**

**Option A: Web Interface (Streamlit)**
```bash
streamlit run run.py
```
Access at: `http://localhost:8501`

**Option B: REST API**
```bash
python run_api.py
```
Access at: `http://localhost:8000`
API Docs: `http://localhost:8000/api/docs`

---

## 🔌 REST API

### Quick Start

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Register/Login
response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
    "username": "your_username",
    "password": "your_password"
})
token = response.json()["access_token"]

# 2. Analyze Decision
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/api/v1/decisions/analyze",
    headers=headers,
    json={
        "decision": "Should I switch careers to AI/ML?",
        "context": "5 years in web development",
        "tags": ["career", "ai"]
    }
)

result = response.json()
print(f"Recommendation: {result['recommendation']}")
print(f"Risk Score: {result['risk_score']}/10")
print(f"Opportunity Score: {result['opportunity_score']}/10")
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get JWT token |
| POST | `/api/v1/decisions/analyze` | Analyze a decision |
| GET | `/api/v1/decisions/history` | Get decision history |
| GET | `/api/v1/decisions/{id}` | Get specific decision |
| DELETE | `/api/v1/decisions/{id}` | Delete decision |
| GET | `/api/v1/analytics/summary` | Get analytics summary |
| GET | `/api/v1/health` | Health check |

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

---

## 📖 Usage

### Web Interface

1. **Register/Login** - Create account or sign in
2. **Enter Decision** - Describe your decision (min 10 characters)
3. **Add Context** - Provide background information (optional)
4. **Add Tags** - Categorize with tags (optional)
5. **Analyze** - Click "Analyze Decision" (takes 1-2 minutes)
6. **Review Results** - Explore comprehensive analysis with:
   - Strategic recommendation with confidence level
   - Risk and opportunity scores
   - Key insights and next steps
   - Detailed factor analysis
7. **Export PDF** - Click "📥 Download PDF" to save analysis report
8. **Ask Questions** - Use AI chat assistant for follow-up questions
9. **View History** - Access past analyses with search and filter
10. **Analytics** - See decision-making patterns and trends
11. **Compare** - Compare multiple decisions side-by-side

### Command Line

```bash
# Run web interface
streamlit run run.py

# Run API server
python run_api.py

# Run tests
python tests/test_backend.py

# Test API
python test_api.py
```

---

## 📁 Project Structure

```
futureself-ai/
├── src/
│   ├── agents/              # AI agents
│   │   ├── base.py         # Base agent class
│   │   ├── planner.py      # Planner agent
│   │   ├── research.py     # Research agent
│   │   ├── risk.py         # Risk agent
│   │   ├── opportunity.py  # Opportunity agent
│   │   ├── strategist.py   # Strategist agent
│   │   └── llm_factory.py  # LLM provider factory
│   ├── api/                 # REST API
│   │   ├── main.py         # FastAPI application
│   │   └── __init__.py
│   ├── auth/                # Authentication
│   │   ├── auth_manager.py # Auth logic
│   │   ├── database.py     # Database models
│   │   └── __init__.py
│   ├── chat/                # AI chat assistant
│   │   ├── chat_assistant.py
│   │   └── __init__.py
│   ├── export/              # Export functionality
│   │   ├── pdf_exporter.py
│   │   └── __init__.py
│   ├── history/             # Decision history
│   │   ├── history_manager.py
│   │   └── __init__.py
│   ├── schemas/             # Pydantic models
│   │   ├── decision.py
│   │   ├── analysis.py
│   │   ├── factors.py
│   │   ├── recommendation.py
│   │   ├── state.py
│   │   └── __init__.py
│   ├── scoring/             # Scoring engine
│   │   ├── engine.py
│   │   ├── validators.py
│   │   └── __init__.py
│   ├── ui/                  # Streamlit UI
│   │   ├── app.py          # Main app
│   │   ├── components.py   # UI components
│   │   ├── auth_ui.py      # Auth pages
│   │   └── __init__.py
│   ├── utils/               # Utilities
│   │   ├── formatters.py
│   │   └── __init__.py
│   └── workflow/            # LangGraph workflow
│       ├── graph.py        # Workflow definition
│       ├── runner.py       # Workflow runner
│       └── __init__.py
├── config/                  # Configuration
│   ├── settings.py
│   └── __init__.py
├── data/                    # Database (auto-created)
│   └── futureself.db
├── tests/                   # Test suite
│   ├── test_backend.py
│   └── __init__.py
├── .env.example             # Environment template
├── .gitignore              # Git ignore rules
├── API_DOCUMENTATION.md    # API reference
├── LICENSE                 # MIT License
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── run.py                  # Streamlit entry point
├── run_api.py             # API entry point
└── test_api.py            # API test script
```

---

## 🧪 Testing

### Run Backend Tests
```bash
python tests/test_backend.py
```

Tests cover:
- ✅ Database initialization
- ✅ User authentication
- ✅ Decision history CRUD
- ✅ PDF export generation
- ✅ AI chat assistant

### Test API
```bash
# Start API server first
python run_api.py

# In another terminal, run tests
python test_api.py
```

---

## 🔒 Security

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: 30-minute expiration
- **API Keys**: Stored in `.env` (not in git)
- **SQL Injection**: Protected via SQLAlchemy ORM
- **CORS**: Configurable for production
- **User Isolation**: Data separated by user_id

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
# LLM Provider
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
TEMPERATURE=0.0

# API Security
JWT_SECRET_KEY=your-secret-key-change-in-production

# Optional: Other providers
OPENAI_API_KEY=your_openai_key
HUGGINGFACE_API_KEY=your_hf_key
```

### LLM Providers

**Groq (Recommended - Free)** ⭐
- 14,400 requests/day free
- Very fast inference
- No credit card required
- Get key at: https://console.groq.com

**OpenAI (Paid)**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
MODEL_NAME=gpt-4
```

**Ollama (Local)**
```env
LLM_PROVIDER=ollama
MODEL_NAME=llama3.2
```

---

## 📊 Performance

- **Analysis Time**: 1-2 minutes (with Groq)
- **Accuracy**: High-quality insights from Llama 3.3 70B
- **Cost**: Free with Groq (14,400 requests/day)
- **Scalability**: Async API, can handle concurrent requests
- **Database**: SQLite (suitable for 1000s of decisions)

---

## 📚 Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[API_IMPLEMENTATION_SUMMARY.md](API_IMPLEMENTATION_SUMMARY.md)** - Technical overview
- **[NEW_FEATURES_GUIDE.md](NEW_FEATURES_GUIDE.md)** - Feature documentation
- **[TEST_GUIDE.md](TEST_GUIDE.md)** - Testing instructions
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - User guide

---

## 🛣️ Roadmap

### Completed ✅
- Multi-agent AI system with 5 specialized agents
- Decision history with search & filter
- Analytics dashboard with visualizations
- Decision comparison (2-3 decisions)
- REST API with JWT authentication
- AI chat assistant for follow-up questions
- PDF export for analysis reports
- User authentication & authorization
- Tag-based organization
- Interactive Plotly charts

### Planned 🚧
- [ ] Decision templates
- [ ] Email notifications
- [ ] Decision outcome tracking
- [ ] Export to CSV/JSON
- [ ] Collaborative decisions
- [ ] Mobile app
- [ ] GraphQL API
- [ ] Webhooks

---

## 🔧 Troubleshooting

### Common Issues

**1. Rate Limit Errors**
```
Error: Rate limit reached for model llama-3.3-70b-versatile
```
**Solution**: Groq free tier has 100,000 tokens/day limit. Wait 24 hours or create a new API key with a different account.

**2. PDF Export Not Working**
```
ModuleNotFoundError: No module named 'reportlab'
```
**Solution**: Install reportlab:
```bash
pip install reportlab
# or run: install_missing_deps.bat
```

**3. Chat Not Responding**
- Make sure analysis is complete (see "✅ Analysis Complete!" message)
- Check if you've hit rate limits
- Scroll to bottom of page to see chat input
- Try refreshing the page (F5)

**4. Database Errors**
```
Error: database is locked
```
**Solution**: Close all instances of the app and restart

**5. Authentication Issues**
- Clear browser cache and cookies
- Try logging out and back in
- Check if `.env` file has `JWT_SECRET_KEY` set

### Getting Help

If you encounter issues:
1. Check terminal/console for error messages
2. Review the troubleshooting section above
3. Open an issue on GitHub with error details

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain & LangGraph** - Agent orchestration framework
- **FastAPI** - Modern web framework
- **Streamlit** - Beautiful UI framework
- **Groq** - Free, fast LLM inference
- **Plotly** - Interactive visualizations

---

## 📧 Contact

**Advika Khorgade**
- GitHub: [@advika-khorgade](https://github.com/advika-khorgade)
- Project Link: [https://github.com/advika-khorgade/futureself-ai](https://github.com/advika-khorgade/futureself-ai)

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Built with ❤️ using Python, FastAPI, LangGraph, and Streamlit**

[⬆ Back to Top](#-futureself-ai---multi-agent-decision-intelligence-platform)

</div>
