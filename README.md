# 🔮 FutureSelf AI - Decision Intelligence Platform

A production-grade multi-agent AI system that helps you make better decisions through comprehensive risk and opportunity analysis.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Features

### Core Capabilities
- **🤖 Multi-Agent AI System** - 5 specialized agents working together
- **📊 Comprehensive Analysis** - Risk, opportunity, and strategic insights
- **🎯 Smart Scoring** - Deterministic evaluation with weighted factors
- **💡 Strategic Recommendations** - Clear, actionable guidance
- **🔐 User Authentication** - Secure login and registration
- **🎨 Beautiful UI** - Modern, professional interface with animations

### AI Agents
1. **Planner Agent** - Breaks decisions into evaluation factors
2. **Research Agent** - Analyzes context and gathers insights
3. **Risk Agent** - Scores risks (0-10 scale)
4. **Opportunity Agent** - Scores opportunities (0-10 scale)
5. **Strategist Agent** - Synthesizes final recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/futureself-ai.git
cd futureself-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key (free):
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
```

Get a free Groq API key at: https://console.groq.com

5. **Run the application**
```bash
streamlit run run.py
```

The app will open at `http://localhost:8501`

## 📖 Usage

1. **Register/Login** - Create an account or sign in
2. **Enter Decision** - Describe the decision you're evaluating
3. **Add Context** - Provide relevant background (optional)
4. **Analyze** - Let the AI agents analyze your decision
5. **Review Results** - Get comprehensive insights and recommendations

## 🏗️ Architecture

```
futureself-ai/
├── src/
│   ├── agents/          # 5 AI agents
│   ├── auth/            # Authentication system
│   ├── schemas/         # Pydantic models
│   ├── workflow/        # LangGraph orchestration
│   ├── scoring/         # Scoring engine
│   ├── utils/           # Utilities
│   └── ui/              # Streamlit interface
├── config/              # Configuration
├── data/                # Database (auto-created)
├── tests/               # Test suite
└── requirements.txt     # Dependencies
```

## 🔧 Configuration

### LLM Providers

**Groq (Recommended - Free)** ⭐
- 14,400 requests/day free
- Very fast inference
- No credit card required
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
MODEL_NAME=llama-3.3-70b-versatile
```

**OpenAI (Paid)**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4
```

**Ollama (Local)**
```bash
LLM_PROVIDER=ollama
MODEL_NAME=llama3.2
```

## 📊 Performance

- **Analysis Time**: 1-2 minutes (with Groq)
- **Accuracy**: High-quality insights from Llama 3.3 70B
- **Cost**: Free with Groq (14,400 requests/day)

## 🛣️ Roadmap

See [FEATURE_ROADMAP.md](FEATURE_ROADMAP.md) for planned features:

### Coming Soon
- ✅ Decision History
- ✅ Export to PDF
- ✅ Decision Dashboard
- ✅ Templates
- ✅ Comparison Mode
- ✅ Team Collaboration

### Revenue Potential
- **Free**: 5 decisions/month
- **Pro ($9.99/mo)**: Unlimited decisions, history, export
- **Team ($29.99/mo)**: Collaboration, API access
- **Enterprise**: Custom pricing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- UI powered by [Streamlit](https://streamlit.io/)
- Free AI inference by [Groq](https://groq.com/)

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ and AI**
