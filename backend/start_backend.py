#!/usr/bin/env python3
"""
Simple startup script for Healthcare Symptom Checker backend
This script checks requirements and starts the server
"""

import sys
import os
import subprocess

def check_and_install_dependencies():
    """Check and install required packages."""
    print("\n" + "="*60)
    print("Checking Dependencies...")
    print("="*60)
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'google-generativeai'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        response = input("\nInstall missing packages? (y/n): ").lower()
        if response == 'y':
            print("\nInstalling packages...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'fastapi', 'uvicorn[standard]', 'pydantic',
                'google-generativeai', 'python-multipart', 'aiofiles'
            ])
            print("✓ Packages installed successfully")
        else:
            print("✗ Cannot start without required packages")
            return False
    
    return True

def check_api_key():
    """Check if GEMINI_API_KEY is set."""
    print("\n" + "="*60)
    print("Checking API Key...")
    print("="*60)
    
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("✗ GEMINI_API_KEY not set\n")
        print("Please set your Gemini API key:")
        print("\nWindows Command Prompt:")
        print("  set GEMINI_API_KEY=your_api_key_here")
        print("\nWindows PowerShell:")
        print("  $env:GEMINI_API_KEY=\"your_api_key_here\"")
        print("\nMac/Linux:")
        print("  export GEMINI_API_KEY=your_api_key_here")
        print("\nGet your API key at:")
        print("  https://makersuite.google.com/app/apikey")
        print("\nAfter setting the key, run this script again.")
        return False
    
    masked = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
    print(f"✓ GEMINI_API_KEY is set ({masked})")
    return True

def check_file_structure():
    """Verify required files exist."""
    print("\n" + "="*60)
    print("Checking File Structure...")
    print("="*60)
    
    required_files = [
        'backend/app.py',
        'backend/llm_client.py',
        'backend/database.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_exist = False
    
    if not all_exist:
        print("\n✗ Missing required files")
        print("Make sure you're in the project root directory")
        return False
    
    return True

def start_server():
    """Start the FastAPI server."""
    print("\n" + "="*60)
    print("Starting Backend Server...")
    print("="*60)
    print("\nServer will start on: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop the server\n")
    print("="*60 + "\n")
    
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.getcwd(), 'backend')
        if os.path.exists(backend_dir):
            os.chdir(backend_dir)
        
        # Run the app
        import uvicorn
        from app import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main startup routine."""
    print("\n" + "="*60)
    print("Healthcare Symptom Checker - Backend Startup")
    print("="*60)
    
    # Run checks
    if not check_file_structure():
        print("\n✗ Startup failed - file structure check failed")
        return False
    
    if not check_and_install_dependencies():
        print("\n✗ Startup failed - dependency check failed")
        return False
    
    if not check_api_key():
        print("\n✗ Startup failed - API key not set")
        return False
    
    print("\n✅ All checks passed! Starting server...\n")
    
    # Start the server
    return start_server()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)