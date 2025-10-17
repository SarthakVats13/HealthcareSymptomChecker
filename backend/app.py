from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import sys
import os

# --- Module Imports ---
# This block ensures that the necessary modules can be found and provides clear error messages.
try:
    from llm_client import get_symptom_analysis
    from database import save_query, get_recent_queries
    print("✓ Successfully imported llm_client and database modules")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure llm_client.py and database.py are in the same folder as app.py")
    sys.exit(1)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Healthcare Symptom Checker API",
    description="Educational tool for symptom analysis using a local LLM",
    version="1.1.0"
)

# --- CORS Middleware ---
# Allows the frontend (running on any origin) to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Data Models ---
# These define the structure of the data for API requests and responses.
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

# --- API Endpoints ---
@app.get("/")
async def root():
    """Root endpoint to welcome users and provide basic API info."""
    return {
        "message": "Healthcare Symptom Checker API is running!",
        "status": "operational",
        "llm_backend": "Local Ollama",
        "version": "1.1.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint to confirm the server is running."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze", response_model=SymptomResponse)
async def analyze_symptoms(request: SymptomRequest):
    """Analyzes symptoms using the local LLM and returns potential conditions."""
    print(f"\n{'='*60}\nNew Analysis Request: {request.symptoms[:100]}...")
    
    try:
        # Call the local LLM for analysis
        print("Calling local Ollama model for analysis...")
        analysis = await get_symptom_analysis(
            symptoms=request.symptoms,
            age=request.age,
            gender=request.gender
        )
        print("✓ Local LLM analysis completed")
        
        # Save the query and analysis to the database
        query_id = save_query(
            symptoms=request.symptoms,
            age=request.age,
            gender=request.gender,
            conditions=analysis["conditions"],
            recommendations=analysis["recommendations"]
        )
        print(f"✓ Saved to database with ID: {query_id}")
        
        # Prepare and return the final response
        return SymptomResponse(
            conditions=analysis["conditions"],
            recommendations=analysis["recommendations"],
            disclaimer=(
                "⚠️ IMPORTANT MEDICAL DISCLAIMER: This tool is for educational purposes only "
                "and is not a substitute for professional medical advice. Always consult "
                "with a qualified healthcare provider."
            ),
            timestamp=datetime.now().isoformat(),
            query_id=query_id
        )
        
    except Exception as e:
        print(f"✗ Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/history")
async def get_history(limit: int = 10):
    """Retrieves recent symptom queries from the database."""
    try:
        queries = get_recent_queries(limit=limit)
        return {"queries": queries}
    except Exception as e:
        print(f"✗ Error retrieving history: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve history: {str(e)}"
        )

# --- Server Startup ---
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("Starting Healthcare Symptom Checker Backend (Local Ollama)")
    print("="*60)
    print(f"API Documentation: http://localhost:8000/docs")
    print(f"Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)