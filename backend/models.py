from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class SymptomInput(BaseModel):
    """Model for symptom input validation"""
    symptoms: str = Field(
        ..., 
        min_length=3, 
        max_length=1000,
        description="Description of symptoms experienced"
    )
    age: Optional[int] = Field(
        None, 
        ge=0, 
        le=120,
        description="Patient age in years"
    )
    gender: Optional[str] = Field(
        None,
        description="Patient gender (male, female, other)"
    )
    
    @validator('symptoms')
    def symptoms_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Symptoms description cannot be empty or only whitespace')
        return v.strip()
    
    @validator('gender')
    def gender_must_be_valid(cls, v):
        if v is not None:
            valid_genders = ['male', 'female', 'other', 'm', 'f']
            if v.lower() not in valid_genders:
                raise ValueError('Gender must be male, female, or other')
            return v.lower()
        return v

class Condition(BaseModel):
    """Model for a medical condition"""
    name: str = Field(..., description="Name of the condition")
    description: str = Field(..., description="Brief description of the condition")
    likelihood: Optional[str] = Field(None, description="Likelihood assessment")

class Recommendation(BaseModel):
    """Model for a medical recommendation"""
    action: str = Field(..., description="Recommended action")
    priority: Optional[str] = Field(None, description="Priority level (low, medium, high, urgent)")

class AnalysisResult(BaseModel):
    """Model for the complete analysis result"""
    conditions: List[str] = Field(..., description="List of possible conditions")
    recommendations: List[str] = Field(..., description="List of recommended actions")
    disclaimer: str = Field(..., description="Medical disclaimer")
    timestamp: datetime = Field(default_factory=datetime.now)
    query_id: Optional[int] = Field(None, description="Database query ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "conditions": [
                    "Common Cold: A viral infection affecting the upper respiratory tract...",
                    "Seasonal Allergies: An immune response to environmental allergens..."
                ],
                "recommendations": [
                    "Monitor symptoms for 48-72 hours",
                    "Stay hydrated and get adequate rest",
                    "Consult a healthcare provider if symptoms worsen"
                ],
                "disclaimer": "This is for educational purposes only...",
                "timestamp": "2025-10-16T10:30:00",
                "query_id": 1
            }
        }

class QueryHistory(BaseModel):
    """Model for stored query history"""
    id: int
    symptoms: str
    age: Optional[int]
    gender: Optional[str]
    conditions: List[str]
    recommendations: List[str]
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "symptoms": "Headache and fever for 2 days",
                "age": 35,
                "gender": "female",
                "conditions": ["Viral infection: ...", "Tension headache: ..."],
                "recommendations": ["Rest and hydration", "Monitor temperature"],
                "timestamp": "2025-10-16T10:30:00"
            }
        }