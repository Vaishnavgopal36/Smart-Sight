import os
import subprocess
import sys
import torch
import json

failed_packages = []

def check_and_install_package(package):
    package_name = package.split("==")[0] if "==" in package else package
    try:
        installed_version = subprocess.run([sys.executable, "-m", "pip", "show", package_name], capture_output=True, text=True).stdout
        if installed_version and f"Version: {package.split('==')[1]}" in installed_version:
            print(f"✅ {package} is already installed.")
            return
        print(f"🔄 Updating {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package_name])
    except Exception:
        print(f"📦 Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        failed_packages.append(package)

def detect_torch_version():
    try:
        if torch.cuda.is_available():
            print("🔍 GPU detected! Installing PyTorch with CUDA support...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "--index-url", "https://download.pytorch.org/whl/cu124"])
        else:
            print("🔍 No GPU detected. Installing CPU version of PyTorch...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "torch"])
    except subprocess.CalledProcessError:
        print("⚠️ Error detecting or installing PyTorch. Defaulting to CPU version...")
        failed_packages.append("torch")

def ensure_dependencies():
    required_packages = [
        "clip==1.0", "faiss-cpu==1.9.0.post1", "fastapi==0.115.11", "langchain==0.3.21", 
        "langchain_google_genai==2.1.1", "numpy==2.2.4", "Pillow==11.1.0", "python-dotenv==1.0.1", "tqdm==4.66.4"
    ]
    print("🔍 Checking and installing required Python packages...")
    for package in required_packages:
        check_and_install_package(package)
    detect_torch_version()
    print("✅ All required packages are installed and ready!")

def ensure_env():
    env_path = "backend/.env"
    if not os.path.exists(env_path):
        with open(env_path, "w") as f:
            f.write("GEMINI_API_KEY=\n")
    with open(env_path, "r") as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if line.startswith("GEMINI_API_KEY=") and line.strip() == "GEMINI_API_KEY=":
            api_key = input("🔑 Enter your GEMINI_API_KEY: ")
            lines[i] = f"GEMINI_API_KEY={api_key}\n"
            with open(env_path, "w") as f:
                f.writelines(lines)
            print("✅ GEMINI_API_KEY set successfully.")
            break

def check_npm():
    try:
        result = subprocess.run(["npm", "-v"], check=True, capture_output=True, text=True)
        print(f"✅ npm is already installed (version {result.stdout.strip()}).")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 npm is not found in PATH, trying alternative methods...")
        try:
            if sys.platform == "win32":
                result = subprocess.run(["where", "npm"], check=True, capture_output=True, text=True)
            else:
                result = subprocess.run(["which", "npm"], check=True, capture_output=True, text=True)
            print(f"✅ npm found at: {result.stdout.strip()}")
        except subprocess.CalledProcessError:
            print("❌ npm is not installed or not found in PATH.")
            if sys.platform.startswith("linux") or sys.platform == "darwin":
                subprocess.run(["sudo", "apt", "install", "npm", "-y"], check=True)
            elif sys.platform == "win32":
                print("⚠️ Please install npm manually from https://nodejs.org/")
                sys.exit(1)

def run_commands():
    backend_command = [sys.executable, "-m", "uvicorn", "main:app", "--reload"]
    frontend_command = ["npm", "install"] if not os.path.exists("frontend/node_modules") else ["npm", "run", "dev"]
    
    # Open backend terminal
    if sys.platform == "win32":
        subprocess.Popen(["start", "cmd", "/k", "cd backend\\server\\app && " + " ".join(backend_command)], shell=True)
    else:
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "cd backend/server/app && " + " ".join(backend_command)])
    
    # Open frontend terminal
    if sys.platform == "win32":
        subprocess.Popen(["start", "cmd", "/k", "cd frontend && " + " ".join(frontend_command)], shell=True)
    else:
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "cd frontend && " + " ".join(frontend_command)])


def list_and_fix_frontend_packages():
    frontend_path = os.path.abspath("frontend")
    print(f"📦 Checking frontend dependencies in: {frontend_path}")

    missing_packages = []

    try:
        # Get installed packages as JSON
        result = subprocess.run(["npm.cmd", "ls", "--depth=0", "--json"], cwd=frontend_path, capture_output=True, text=True, encoding="utf-8")
        installed_packages = json.loads(result.stdout).get("dependencies", {})

        # Read package.json to get required dependencies
        with open(os.path.join(frontend_path, "package.json"), "r", encoding="utf-8") as f:
            package_json = json.load(f)
            required_packages = package_json.get("dependencies", {})

        print("\n📋 **Frontend Package Status:**")
        for package, version in required_packages.items():
            if package in installed_packages:
                # Check if it's an unmet dependency
                if installed_packages[package].get("missing", False):
                    print(f"❌ {package}@{version} (UNMET DEPENDENCY) - Will be installed")
                    missing_packages.append(f"{package}@{version}")
                else:
                    print(f"✅ {package}@{installed_packages[package].get('version', 'unknown')}")
            else:
                print(f"❌ {package}@{version} (MISSING) - Will be installed")
                missing_packages.append(f"{package}@{version}")

        # Install missing/unmet dependencies
        if missing_packages:
            print("\n📦 Installing missing/unmet dependencies...\n")
            install_command = ["npm.cmd", "install"] + missing_packages
            subprocess.run(install_command, cwd=frontend_path)
            print("✅ Installation complete!")

    except Exception as e:
        print(f"⚠️ Error checking or installing frontend dependencies: {e}")


def main():
    list_and_fix_frontend_packages()
    ensure_env()
    ensure_dependencies()
    check_npm()
    run_commands()
    
    if failed_packages:
        print("\n❌ The following packages failed to install:")
        for pkg in failed_packages:
            print(f"   - {pkg}")
    else:
        print("✅ All packages installed successfully!")
    
    print("🚀 Frontend and backend launched in separate terminals!")

if __name__ == "__main__":
    main()
