# Setting Up HuggingFace Models (Free, Ultra-Lightweight)

Perfect for laptops with limited RAM and storage! HuggingFace models run directly on your machine with no external dependencies.

## Why HuggingFace for Low-Spec Machines?

✅ **Ultra-lightweight** - TinyLlama is only ~1.1GB
✅ **Low RAM usage** - Works with as little as 2GB RAM
✅ **No installation** - No Ollama or Docker needed
✅ **Completely free** - No API costs
✅ **Auto-download** - Models download automatically on first use
✅ **Works offline** - After first download

## Quick Setup (3 Steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `transformers` - HuggingFace library
- `torch` - PyTorch (CPU version is fine)
- `accelerate` - Optimization library

### 2. Configure

```bash
cp .env.example .env
```

The `.env` file is already configured for TinyLlama:
```
LLM_PROVIDER=huggingface
MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

### 3. Run

```bash
streamlit run run.py
```

On first run, the model will download automatically (~1.1GB). This is a one-time download.

## Recommended Models for Low-Spec Machines

### TinyLlama 1.1B (BEST for limited resources) ⭐
- **Size**: ~1.1GB download
- **RAM**: ~2GB required
- **Speed**: Very fast
- **Model ID**: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

### Microsoft Phi-2 (Better quality, needs more resources)
- **Size**: ~2.7GB download
- **RAM**: ~4GB required
- **Speed**: Moderate
- **Model ID**: `microsoft/phi-2`

### Google Gemma 2B (Balanced)
- **Size**: ~2GB download
- **RAM**: ~3GB required
- **Speed**: Moderate
- **Model ID**: `google/gemma-2b`

### StableLM 1.6B (Alternative)
- **Size**: ~1.6GB download
- **RAM**: ~2.5GB required
- **Speed**: Fast
- **Model ID**: `stabilityai/stablelm-2-zephyr-1_6b`

## System Requirements

### Minimum (TinyLlama):
- **RAM**: 2GB available
- **Storage**: 2GB free space
- **CPU**: Any modern CPU (no GPU needed)
- **OS**: Windows, Mac, or Linux

### Recommended:
- **RAM**: 4GB available
- **Storage**: 5GB free space
- **CPU**: Multi-core processor

## First Run

The first time you run the app:
1. Model will download automatically (~1-3 minutes depending on internet)
2. Model will load into memory (~10-30 seconds)
3. Then it's ready to use!

Subsequent runs are much faster (no download needed).

## Troubleshooting

### "Out of memory" error:
- Use TinyLlama (smallest model)
- Close other applications
- Restart your computer to free up RAM

### Slow performance:
- TinyLlama is the fastest option
- First response is slower (model loading)
- Subsequent responses are faster

### Download fails:
- Check internet connection
- Ensure you have enough disk space
- Try again (downloads resume automatically)

### Model not found:
- Check the model ID is correct
- Ensure you have internet for first download
- Check HuggingFace is accessible (not blocked by firewall)

## Switching Models

Edit `.env` file:
```bash
MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

Or change in the Streamlit sidebar dropdown.

## Comparison: HuggingFace vs Ollama

### HuggingFace (Recommended for low-spec):
- ✅ Smaller models available (1.1GB)
- ✅ Lower RAM usage (2GB)
- ✅ No external dependencies
- ✅ Direct Python integration
- ⚠️ Slower than Ollama (but still usable)

### Ollama:
- ✅ Faster inference
- ✅ Better model management
- ⚠️ Requires installation
- ⚠️ Larger models (2GB minimum)
- ⚠️ More RAM needed (3GB+)

## Storage Locations

Models are cached in:
- **Windows**: `C:\Users\YourName\.cache\huggingface\hub`
- **Mac/Linux**: `~/.cache/huggingface/hub`

You can delete these to free up space when not needed.

## Tips for Best Performance

1. **Use TinyLlama** - Best for limited resources
2. **Close other apps** - Free up RAM
3. **Be patient on first run** - Model needs to download
4. **Lower temperature** - Use 0.0 for faster, deterministic responses
5. **Restart if slow** - Sometimes helps clear memory

## Need Even Lighter?

If TinyLlama is still too heavy, you can:
1. Use OpenAI API (cloud-based, no local resources)
2. Use a smaller quantized model
3. Run on a more powerful machine

But TinyLlama is already one of the smallest viable models!
