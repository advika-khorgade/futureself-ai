# Fixing "Out of Memory" Error

Your laptop doesn't have enough RAM for TinyLlama. Here are your options:

## Option 1: Use Ollama (RECOMMENDED) ⭐

Ollama is optimized for low-memory systems and will work much better:

### Step 1: Install Ollama
- Download: https://ollama.com/download
- Install and it will start automatically

### Step 2: Download a lightweight model
```bash
ollama pull tinyllama
```

This downloads a memory-optimized version (~637MB).

### Step 3: Update your .env file
```
LLM_PROVIDER=ollama
MODEL_NAME=tinyllama
```

### Step 4: Restart the app
```bash
streamlit run run.py
```

**Memory usage**: ~1GB RAM (vs 2GB+ with HuggingFace)

---

## Option 2: Install Quantization Library

Try to reduce TinyLlama's memory usage:

### Step 1: Install bitsandbytes
```bash
pip install bitsandbytes
```

### Step 2: Restart the app
```bash
streamlit run run.py
```

This will use 8-bit quantization, reducing memory from 2GB to ~1GB.

**Note**: bitsandbytes may not work on all Windows systems.

---

## Option 3: Use Groq API (Free, Fast)

Groq offers FREE API access to fast models:

### Step 1: Get free API key
- Go to: https://console.groq.com
- Sign up (free)
- Get API key

### Step 2: Install Groq support
```bash
pip install langchain-groq
```

### Step 3: Update .env
```
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
MODEL_NAME=llama3-8b-8192
```

### Step 4: Update llm_factory.py
Add Groq support (I can help with this)

**Benefits**:
- ✅ Completely FREE
- ✅ Very fast (faster than OpenAI)
- ✅ No local memory needed
- ✅ 14,400 requests per day free tier

---

## Option 4: Use Google Colab (Free Cloud)

Run the entire system in Google's free cloud:

1. Go to: https://colab.research.google.com
2. Upload your project
3. Run with free GPU/RAM
4. Access via public URL

---

## Comparison

| Option | RAM Needed | Speed | Setup | Cost |
|--------|------------|-------|-------|------|
| Ollama | ~1GB | Fast | 5 min | Free |
| Quantization | ~1GB | Slow | 2 min | Free |
| Groq API | 0GB | Very Fast | 5 min | Free |
| Google Colab | 0GB | Fast | 10 min | Free |

## My Recommendation

**Use Ollama** - It's specifically designed for your use case:
- Optimized for low-memory systems
- Fast inference
- Easy to install
- Works offline
- Completely free

Just follow Option 1 above. It should work perfectly on your laptop!

---

## Still Having Issues?

If none of these work, your laptop may have less than 2GB available RAM. Check:

```bash
# Windows
wmic OS get FreePhysicalMemory

# Shows available RAM in KB
```

If you have less than 2GB free, you'll need to:
1. Close other applications
2. Use Groq API (no local memory needed)
3. Use a more powerful machine
