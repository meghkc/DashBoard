#!/usr/bin/env python3
"""
Advanced US Freight Analytics Dashboard - Setup Script

This script helps set up the development environment and run basic tests
to ensure the dashboard works correctly.

Author: Megh KC
Created: 2025
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 70)
    print("🚛 Advanced US Freight Analytics Dashboard - Setup")
    print("=" * 70)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_required_files():
    """Check if required files exist"""
    print("\n📁 Checking required files...")
    
    required_files = [
        "streamlit_app.py",
        "requirements.txt",
        "Data/Rail_Carloadings_originated.csv",
        "Data/port_dataset.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_data_integrity():
    """Basic data integrity checks"""
    print("\n🔍 Checking data integrity...")
    
    try:
        import pandas as pd
        import json
        
        # Check rail data
        rail_df = pd.read_csv("Data/Rail_Carloadings_originated.csv")
        print(f"✅ Rail data: {len(rail_df):,} records")
        
        # Check port data  
        with open("Data/port_dataset.json", 'r') as f:
            port_data = json.load(f)
        print(f"✅ Port data: {len(port_data)} records")
        
        return True
    except Exception as e:
        print(f"❌ Data check failed: {e}")
        return False

def create_launcher_script():
    """Create platform-specific launcher script"""
    print("\n🚀 Creating launcher script...")
    
    if platform.system() == "Windows":
        launcher_content = """@echo off
echo Starting Advanced Freight Analytics Dashboard...
echo Dashboard will open at: http://localhost:8501
echo Press Ctrl+C to stop
echo.
streamlit run streamlit_app.py
pause"""
        with open("launch_dashboard.bat", "w") as f:
            f.write(launcher_content)
        print("✅ Created launch_dashboard.bat")
    else:
        launcher_content = """#!/bin/bash
echo "Starting Advanced Freight Analytics Dashboard..."
echo "Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop"
echo
streamlit run streamlit_app.py"""
        with open("launch_dashboard.sh", "w") as f:
            f.write(launcher_content)
        os.chmod("launch_dashboard.sh", 0o755)
        print("✅ Created launch_dashboard.sh")

def run_test():
    """Run basic functionality test"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test imports
        import streamlit
        import pandas
        import plotly
        import matplotlib
        import numpy
        print("✅ All imports successful")
        
        # Test data loading
        import pandas as pd
        rail_df = pd.read_csv("Data/Rail_Carloadings_originated.csv")
        if len(rail_df) > 0:
            print("✅ Rail data loads correctly")
        
        with open("Data/port_dataset.json", 'r') as f:
            import json
            port_data = json.load(f)
        if len(port_data) > 0:
            print("✅ Port data loads correctly")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 70)
    print("🎉 Setup Complete! Next Steps:")
    print("=" * 70)
    print()
    print("1️⃣  Run the dashboard locally:")
    if platform.system() == "Windows":
        print("    Double-click: launch_dashboard.bat")
        print("    Or run: streamlit run streamlit_app.py")
    else:
        print("    Run: ./launch_dashboard.sh")
        print("    Or run: streamlit run streamlit_app.py")
    print()
    print("2️⃣  Open your browser to: http://localhost:8501")
    print()
    print("3️⃣  For deployment:")
    print("    - Commit changes to GitHub")
    print("    - Deploy on Streamlit Cloud (share.streamlit.io)")
    print()
    print("4️⃣  For development:")
    print("    - Read CONTRIBUTING.md")
    print("    - Check out the Script/ folder for additional files")
    print()
    print("📚 Documentation: README.md")
    print("🐛 Issues: https://github.com/meghkc/DashBoard/issues")
    print()
    print("Happy analyzing! 🚛📊")

def main():
    """Main setup function"""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Run setup checks
    if not check_python_version():
        sys.exit(1)
    
    if not check_required_files():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not check_data_integrity():
        sys.exit(1)
    
    create_launcher_script()
    
    if not run_test():
        print("\n⚠️  Some tests failed, but setup is mostly complete")
        print("   Try running the dashboard manually to see specific errors")
    
    print_next_steps()

if __name__ == "__main__":
    main()
