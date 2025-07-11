#!/usr/bin/env python3
"""
Setup script for Document Summarizer
Helps users install dependencies and set up the environment
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("📄 Document Summarizer - Setup Script")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file template"""
    print("\n🔧 Setting up environment...")
    
    env_file = ".env"
    if os.path.exists(env_file):
        print("⚠️  .env file already exists")
        return True
    
    try:
        with open(env_file, "w") as f:
            f.write("# OpenAI API Configuration\n")
            f.write("# Get your API key from: https://platform.openai.com/api-keys\n")
            f.write("OPENAI_API_KEY=your-api-key-here\n")
            f.write("\n")
            f.write("# Optional: Customize application settings\n")
            f.write("# DEFAULT_MODEL=gpt-3.5-turbo\n")
            f.write("# DEFAULT_STORAGE=sqlite\n")
        
        print("✅ Created .env file template")
        print("   📝 Please edit .env and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def create_sample_files():
    """Create sample files for testing"""
    print("\n📄 Creating sample files...")
    
    try:
        # Run the sample data generator
        subprocess.check_call([sys.executable, "sample_data.py"])
        print("✅ Sample files created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating sample files: {e}")
        return False

def run_tests():
    """Run application tests"""
    print("\n🧪 Running tests...")
    
    try:
        subprocess.check_call([sys.executable, "test_app.py"])
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Some tests failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. 🔑 Add your OpenAI API key to the .env file")
    print("2. 🚀 Start the application: streamlit run app.py")
    print("3. 🌐 Open your browser to: http://localhost:8501")
    print("4. 📁 Upload sample files from the 'sample_files' directory")
    print()
    print("📚 Useful Commands:")
    print("   • Start app: streamlit run app.py")
    print("   • Run tests: python test_app.py")
    print("   • Create samples: python sample_data.py")
    print()
    print("🔗 Resources:")
    print("   • OpenAI API: https://platform.openai.com/api-keys")
    print("   • Streamlit: https://docs.streamlit.io")
    print("   • Project README: README.md")
    print()
    print("💡 Tips:")
    print("   • Use GPT-3.5-turbo for faster, cheaper processing")
    print("   • Start with small documents to test the system")
    print("   • Check the sidebar for configuration options")
    print()
    print("Happy Document Summarizing! 📚✨")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create environment file
    if not create_env_file():
        return False
    
    # Create sample files
    if not create_sample_files():
        print("⚠️  Sample files creation failed, but setup can continue")
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but setup can continue")
    
    # Print next steps
    print_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error during setup: {e}")
        sys.exit(1) 