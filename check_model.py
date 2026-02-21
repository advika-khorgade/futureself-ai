"""Check if model is already downloaded."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def check_model_cached():
    """Check if the model is already in cache."""
    model_name = os.getenv("MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    
    # HuggingFace cache location
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    
    # Convert model name to cache format
    model_cache_name = "models--" + model_name.replace("/", "--")
    model_path = cache_dir / model_cache_name
    
    print(f"🔍 Checking for model: {model_name}")
    print(f"📁 Cache location: {cache_dir}\n")
    
    if model_path.exists():
        # Check if model files exist
        snapshots = model_path / "snapshots"
        if snapshots.exists() and any(snapshots.iterdir()):
            print("✅ Model is already downloaded!")
            print(f"📍 Location: {model_path}")
            
            # Calculate size
            total_size = sum(
                f.stat().st_size 
                for f in model_path.rglob('*') 
                if f.is_file()
            )
            size_gb = total_size / (1024**3)
            print(f"💾 Size: {size_gb:.2f} GB")
            print("\n✨ You can run the app directly:")
            print("   streamlit run run.py")
            return True
        else:
            print("⚠️ Model folder exists but incomplete")
            print("Run: python download_model.py")
            return False
    else:
        print("❌ Model not found in cache")
        print("\n📥 To download the model, run:")
        print("   python download_model.py")
        print("\nThis will take 10-30 minutes depending on your internet speed.")
        return False

if __name__ == "__main__":
    check_model_cached()
