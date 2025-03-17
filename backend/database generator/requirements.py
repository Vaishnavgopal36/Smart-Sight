import subprocess
import sys

# List of required packages with specific versions to ensure compatibility
REQUIRED_PACKAGES = [
    "torch",               # PyTorch (ensure GPU support if available)
    "faiss-cpu",           # FAISS for efficient similarity search (use "faiss-gpu" if CUDA is available)
    "numpy",               # Numerical computations
    "Pillow",              # Image handling
    "tqdm",                # Progress bars
    "transformers",        # Transformers for LLM
    "matplotlib",          # For displaying images
    "langchain_google_genai",  # LangChain Google Gemini API Wrapper
    "langchain",           # Core LangChain functionalities
    "clip-by-openai",      # CLIP model from OpenAI
]

def install_package(package):
    """Install a package using pip if it's not already installed."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}. Please check manually.")

def check_and_install():
    """Check for missing packages and install them."""
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package.split("-")[0])  # Import module name (handling dashes in package names)
            print(f"✅ {package} is already installed.")
        except ImportError:
            print(f"📦 Installing {package}...")
            install_package(package)

if __name__ == "__main__":
    print("🔍 Checking and installing required packages...")
    check_and_install()
    print("✅ All required packages are installed and ready!")
