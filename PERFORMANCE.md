# Performance Guide

## Expected Analysis Times

The multi-agent workflow runs 5 agents sequentially. Here's what to expect:

### HuggingFace (TinyLlama)
- **First Run**: 3-7 minutes
  - Model download: 1-2 minutes (one-time)
  - Model loading: 30-60 seconds
  - Analysis: 2-5 minutes
- **Subsequent Runs**: 2-5 minutes
  - Model already cached
  - Analysis: 2-5 minutes

### Ollama (gemma:2b)
- **First Run**: 2-4 minutes
  - Model already downloaded via `ollama pull`
  - Analysis: 2-4 minutes
- **Subsequent Runs**: 1-2 minutes
  - Faster inference
  - Optimized execution

### OpenAI (GPT-4)
- **Every Run**: 30-60 seconds
  - Cloud-based, no local processing
  - Fastest option
  - Costs per request

## Why Does It Take Time?

The workflow runs 5 AI agents in sequence:

1. **Planner Agent** (~20-60s) - Breaks decision into factors
2. **Research Agent** (~20-60s) - Analyzes each factor
3. **Risk Agent** (~20-60s) - Scores risks
4. **Opportunity Agent** (~20-60s) - Scores opportunities
5. **Strategist Agent** (~20-60s) - Synthesizes recommendation

**Total**: 5 agents × ~30-60s each = 2-5 minutes (local models)

## Performance Tips

### For Faster Results:

1. **Use OpenAI** (if budget allows)
   - Fastest: 30-60 seconds total
   - Costs ~$0.10-0.30 per analysis

2. **Use Ollama instead of HuggingFace**
   - 2x faster than HuggingFace
   - Requires more RAM (3GB vs 2GB)

3. **Close other applications**
   - Free up RAM and CPU
   - Especially important for HuggingFace

4. **Use temperature=0.0**
   - Already default
   - Faster than higher temperatures

5. **Upgrade hardware**
   - More RAM = faster
   - SSD = faster model loading
   - GPU = much faster (if available)

### For Lower Resource Usage:

1. **Use TinyLlama (HuggingFace)**
   - Lowest RAM: 2GB
   - Smallest model: 1.1GB
   - Works on any laptop

2. **Lower temperature**
   - Already at 0.0 (optimal)

3. **Run one analysis at a time**
   - Don't open multiple tabs

## Troubleshooting Slow Performance

### HuggingFace is very slow (>10 minutes):

**Possible causes:**
- First run downloading model
- Insufficient RAM (swapping to disk)
- Other apps using resources
- CPU throttling (laptop on battery)

**Solutions:**
- Check download progress in terminal
- Close other applications
- Plug in laptop (disable power saving)
- Use smaller model or switch to Ollama
- Add more RAM if possible

### Ollama is slow (>5 minutes):

**Possible causes:**
- Model not fully loaded
- Insufficient RAM
- CPU throttling

**Solutions:**
- Restart Ollama: `ollama serve`
- Use smaller model: `gemma:2b` instead of `llama3.2`
- Close other applications
- Check Ollama logs for errors

### Process seems stuck:

**What to check:**
1. Look at progress bar - is it moving?
2. Check terminal for errors
3. Check system resources (Task Manager/Activity Monitor)
4. Wait at least 5 minutes before canceling

**If truly stuck:**
1. Stop the app (Ctrl+C)
2. Restart: `streamlit run run.py`
3. Try again with simpler decision text

## Optimization Roadmap

Future improvements planned:

- [ ] Parallel agent execution (Risk + Opportunity together)
- [ ] Streaming responses (show partial results)
- [ ] Model quantization (smaller, faster models)
- [ ] Caching (reuse results for similar decisions)
- [ ] Batch processing (multiple decisions at once)

## Comparison Table

| Provider | First Run | Subsequent | RAM | Storage | Cost |
|----------|-----------|------------|-----|---------|------|
| HuggingFace (TinyLlama) | 3-7 min | 2-5 min | 2GB | 2GB | Free |
| Ollama (gemma:2b) | 2-4 min | 1-2 min | 3GB | 2GB | Free |
| OpenAI (GPT-4) | 30-60s | 30-60s | 0GB | 0GB | ~$0.20 |

## Recommendations by Use Case

### Low-spec laptop (2GB RAM):
→ Use HuggingFace with TinyLlama
- Slowest but works on any machine
- Completely free

### Normal laptop (4GB+ RAM):
→ Use Ollama with gemma:2b
- Good balance of speed and resources
- Completely free

### Production/frequent use:
→ Use OpenAI
- Fastest and most reliable
- Pay per use (~$0.20 per analysis)

### Development/testing:
→ Use Ollama
- Fast enough for iteration
- Free for unlimited testing
