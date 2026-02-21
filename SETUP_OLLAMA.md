# Setting Up Ollama (Free Local LLM)

Ollama allows you to run powerful language models locally on your machine for FREE - no API keys required!

## Installation

### Windows
1. Download Ollama from: https://ollama.com/download
2. Run the installer
3. Ollama will start automatically

### Mac
```bash
brew install ollama
ollama serve
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

## Download a Model

After installing Ollama, download a model (this is a one-time download):

### Recommended Models

**For lightweight/fast performance (requires ~2GB RAM) - RECOMMENDED:**
```bash
ollama pull gemma:2b
```

**For balanced performance (requires ~3GB RAM):**
```bash
ollama pull phi3
```

**For best quality (requires ~4GB RAM):**
```bash
ollama pull llama3.2
```

**For high-end quality (requires ~8GB RAM):**
```bash
ollama pull mistral
```

## Verify Installation

Test that Ollama is working:
```bash
ollama list
```

You should see your downloaded models.

## Configure FutureSelf AI

1. Edit your `.env` file:
```bash
LLM_PROVIDER=ollama
MODEL_NAME=gemma:2b
OLLAMA_BASE_URL=http://localhost:11434
```

2. Run the application:
```bash
streamlit run run.py
```

That's it! You're now using a completely free, local LLM with no API costs.

## Available Models

- **gemma:2b** - Google's lightweight model, very fast (~2GB RAM) ⭐ RECOMMENDED
- **phi3** - Microsoft's efficient model (~3GB RAM)
- **llama3.2** - Latest Llama model, excellent quality (~4GB RAM)
- **llama3.1** - Previous Llama version, very capable (~4GB RAM)
- **mistral** - High quality model (~8GB RAM)
- **mixtral** - Very high quality, larger model (~16GB RAM)
- **gemma2** - Google's larger model (~5GB RAM)

## Troubleshooting

**"Connection refused" error:**
- Make sure Ollama is running: `ollama serve`
- Check the URL in `.env` matches your Ollama server

**Model not found:**
- Download the model first: `ollama pull gemma:2b`
- Check available models: `ollama list`

**Slow performance:**
- Try a smaller model like `phi3`
- Close other applications to free up RAM
- Consider using a GPU if available

## Switching Between OpenAI and Ollama

You can easily switch between providers by changing the `.env` file:

**Use Ollama (Free):**
```
LLM_PROVIDER=ollama
MODEL_NAME=gemma:2b
```

**Use OpenAI (Paid):**
```
LLM_PROVIDER=openai
MODEL_NAME=gpt-4
OPENAI_API_KEY=your_key_here
```

No code changes needed!
