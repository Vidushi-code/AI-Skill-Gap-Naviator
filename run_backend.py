"""
Startup script for AI Skill Gap Navigator backend
Run this from the project root directory
"""
import uvicorn
import sys
import os
from pathlib import Path

if __name__ == "__main__":
    # Ensure the root directory is in Python path
    root_dir = Path(__file__).parent.absolute()
    sys.path.insert(0, str(root_dir))
    
    # Set PYTHONPATH environment variable for uvicorn subprocesses
    os.environ['PYTHONPATH'] = str(root_dir)
    
    print("=" * 70)
    print("  AI Skill Gap Navigator - Backend Server")
    print("=" * 70)
    print()
    print("  Starting FastAPI server...")
    print("  Server URL: http://localhost:8000")
    print("  API Docs: http://localhost:8000/docs")
    print("  Health Check: http://localhost:8000/health")
    print()
    print("  Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
