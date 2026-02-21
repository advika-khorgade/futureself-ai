"""Pre-download HuggingFace model before running the app."""
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def download_model():
    """Download the model with progress tracking."""
    model_name = os.getenv("MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    
    print(f"🤗 Downloading model: {model_name}")
    print("This is a one-time download. Please wait...\n")
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        print("📥 Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("✅ Tokenizer downloaded!\n")
        
        print("📥 Downloading model (this may take 10-30 minutes)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            low_cpu_mem_usage=True
        )
        print("✅ Model downloaded!\n")
        
        print("=" * 60)
        print("🎉 SUCCESS! Model is ready to use.")
        print("=" * 60)
        print("\nYou can now run the app with:")
        print("  streamlit run run.py")
        print("\nThe model is cached and won't need to download again.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Download interrupted!")
        print("You can resume by running this script again.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Ensure you have ~3GB free disk space")
        print("3. Try a smaller model by editing .env:")
        print("   MODEL_NAME=microsoft/phi-1_5")

if __name__ == "__main__":
    download_model()
