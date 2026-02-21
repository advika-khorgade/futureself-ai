# Free Cloud LLM Setup (No Installation Required!)

Perfect for low-spec machines - runs in the cloud, uses ZERO local resources!

## Option 1: Groq (RECOMMENDED) ⭐

**Why Groq?**
- ✅ Completely FREE (14,400 requests/day)
- ✅ VERY FAST (faster than OpenAI)
- ✅ No credit card required
- ✅ No installation needed
- ✅ Uses 0GB local RAM/storage
- ✅ High quality (Llama 3 models)

### Setup (2 minutes):

**Step 1: Get FREE API Key**
1. Go to: https://console.groq.com
2. Click "Sign Up" (use Google/GitHub)
3. Go to "API Keys" section
4. Click "Create API Key"
5. Copy the key

**Step 2: Configure**
Edit your `.env` file:
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_key_here
MODEL_NAME=llama3-8b-8192
```

**Step 3: Run**
```bash
pip install langchain-groq
streamlit run run.py
```

Done! Your app will now use Groq's cloud servers.

### Available Models:
- `llama3-8b-8192` - Best balance (RECOMMENDED)
- `llama3-70b-8192` - Highest quality
- `mixtral-8x7b-32768` - Good for long context
- `gemma-7b-it` - Fastest

---

## Option 2: HuggingFace Inference API

**Why HuggingFace API?**
- ✅ Completely FREE (1000 requests/day)
- ✅ No credit card required
- ✅ No installation needed
- ✅ Uses 0GB local RAM/storage
- ⚠️ Slower than Groq
- ⚠️ Lower rate limits

### Setup (2 minutes):

**Step 1: Get FREE API Key**
1. Go to: https://huggingface.co/settings/tokens
2. Sign up (free)
3. Click "New token"
4. Name it "futureself-ai"
5. Select "Read" access
6. Copy the token

**Step 2: Configure**
Edit your `.env` file:
```bash
LLM_PROVIDER=huggingface_api
HUGGINGFACE_API_KEY=hf_your_actual_key_here
MODEL_NAME=meta-llama/Llama-2-7b-chat-hf
```

**Step 3: Run**
```bash
streamlit run run.py
```

### Available Models:
- `meta-llama/Llama-2-7b-chat-hf` - Good quality
- `mistralai/Mistral-7B-Instruct-v0.2` - Fast
- `google/flan-t5-xxl` - Lightweight

---

## Comparison

| Provider | Speed | Free Limit | Quality | Setup Time |
|----------|-------|------------|---------|------------|
| **Groq** ⭐ | Very Fast | 14,400/day | Excellent | 2 min |
| HuggingFace API | Slow | 1,000/day | Good | 2 min |
| OpenAI | Fast | $0 (paid) | Excellent | 2 min |

---

## Troubleshooting

### "API key is required" error:
- Make sure you copied the full API key
- Check there are no extra spaces
- Ensure the key is in `.env` file, not `.env.example`

### "Rate limit exceeded":
- Groq: Wait 24 hours or use HuggingFace
- HuggingFace: Wait 24 hours or use Groq
- Both: Create multiple accounts (allowed)

### Slow responses:
- Groq is fastest (use this)
- HuggingFace API can be slow during peak hours
- Try different models

### "Model not found":
- Check model name spelling
- Ensure model is available on the platform
- Try a different model from the list above

---

## My Recommendation

**Use Groq with llama3-8b-8192**

It's:
- The fastest free option
- Better quality than HuggingFace free tier
- More generous rate limits (14,400 vs 1,000)
- Easier to use
- More reliable

Perfect for your low-spec laptop since everything runs in the cloud!

---

## Cost Comparison

| Provider | Cost | Local Resources |
|----------|------|-----------------|
| Groq | $0 | 0GB RAM, 0GB storage |
| HuggingFace API | $0 | 0GB RAM, 0GB storage |
| Ollama | $0 | 1-3GB RAM, 2GB storage |
| HuggingFace Local | $0 | 2-4GB RAM, 2GB storage |
| OpenAI | ~$0.20/analysis | 0GB RAM, 0GB storage |

For your situation, Groq is the clear winner! 🏆
