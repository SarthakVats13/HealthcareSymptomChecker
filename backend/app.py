from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from llm_client import get_symptom_analysis
    from database import save_query, get_recent_queries
    print("✓ Successfully imported llm_client and database modules")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure llm_client.py and database.py are in the backend folder")
    sys.exit(1)

# Check for API key
if not os.environ.get("GEMINI_API_KEY"):
    print("\n" + "="*60)
    print("ERROR: GEMINI_API_KEY environment variable not set!")
    print("="*60)
    print("\nPlease set your API key before running:")
    print("  Windows CMD:  set GEMINI_API_KEY=your_key_here")
    print("  Windows PS:   $env:GEMINI_API_KEY=\"your_key_here\"")
    print("  Mac/Linux:    export GEMINI_API_KEY=your_key_here")
    print("\nGet your API key at: https://makersuite.google.com/app/apikey")
    print("="*60 + "\n")
    sys.exit(1)

print("✓ GEMINI_API_KEY is set")

app = FastAPI(
    title="Healthcare Symptom Checker API",
    description="Educational tool for symptom analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomRequest(BaseModel):
    symptoms: str = Field(..., min_length=3, max_length=1000)
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[str] = None

class SymptomResponse(BaseModel):
    conditions: List[str]
    recommendations: List[str]
    disclaimer: str
    timestamp: str
    query_id: Optional[int] = None

@app.get("/")
async def root():
    return {
        "message": "Healthcare Symptom Checker API is running!",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Analyze symptoms",
            "GET /history": "View recent queries",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_set": bool(os.environ.get("GEMINI_API_KEY"))
    }

@app.post("/analyze", response_model=SymptomResponse)
async def analyze_symptoms(request: SymptomRequest):
    """Analyze symptoms and return probable conditions with recommendations."""
    
    print(f"\n{'='*60}")
    print(f"New Analysis Request")
    print(f"{'='*60}")
    print(f"Symptoms: {request.symptoms[:100]}...")
    print(f"Age: {request.age}")
    print(f"Gender: {request.gender}")
    
    try:
        # Validate input
        if not request.symptoms.strip():
            raise HTTPException(status_code=400, detail="Symptoms cannot be empty")
        
        print("Calling LLM for analysis...")
        
        # Get LLM analysis
        analysis = get_symptom_analysis(
            symptoms=request.symptoms,
            age=request.age,
            gender=request.gender
        )
        
        print(f"✓ LLM analysis completed")
        print(f"  - Conditions found: {len(analysis['conditions'])}")
        print(f"  - Recommendations: {len(analysis['recommendations'])}")
        
        # Save to database
        try:
            query_id = save_query(
                symptoms=request.symptoms,
                age=request.age,
                gender=request.gender,
                conditions=analysis["conditions"],
                recommendations=analysis["recommendations"]
            )
            print(f"✓ Saved to database with ID: {query_id}")
        except Exception as db_error:
            print(f"⚠ Database save failed: {db_error}")
            query_id = None
        
        # Prepare response
        response = SymptomResponse(
            conditions=analysis["conditions"],
            recommendations=analysis["recommendations"],
            disclaimer=(
                "⚠️ IMPORTANT MEDICAL DISCLAIMER: This tool is for educational purposes only "
                "and should NOT be used as a substitute for professional medical advice, diagnosis, "
                "or treatment. Always seek the advice of your physician or other qualified health "
                "provider with any questions you may have regarding a medical condition. "
                "If you are experiencing a medical emergency, call emergency services immediately."
            ),
            timestamp=datetime.now().isoformat(),
            query_id=query_id
        )
        
        print(f"✓ Request completed successfully")
        print(f"{'='*60}\n")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error during analysis: {str(e)}")
        print(f"{'='*60}\n")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/history")
async def get_history(limit: int = 10):
    """Retrieve recent symptom queries."""
    try:
        queries = get_recent_queries(limit=limit)
        return {
            "queries": queries, 
            "count": len(queries),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve history: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("Starting Healthcare Symptom Checker Backend")
    print("="*60)
    print(f"API Documentation: http://localhost:8000/docs")
    print(f"Health Check: http://localhost:8000/health")
    print(f"Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info"
        )
    except Exception as e:
        print(f"\n✗ Failed to start server: {e}")
        print("Make sure port 8000 is not already in use")
        sys.exit(1)