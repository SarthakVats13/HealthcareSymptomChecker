import os
import json
from typing import Optional
import google.generativeai as genai

# Initialize Gemini client
# Set your API key as environment variable: export GEMINI_API_KEY='your-key-here'
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_symptom_analysis(
    symptoms: str,
    age: Optional[int] = None,
    gender: Optional[str] = None
) -> dict:
    """
    Use Gemini LLM to analyze symptoms and provide educational information.
    
    Args:
        symptoms: User's symptom description
        age: Optional patient age
        gender: Optional patient gender
    
    Returns:
        dict with 'conditions' and 'recommendations' lists
    """
    
    # Build context information
    context = f"Symptoms: {symptoms}"
    if age:
        context += f"\nAge: {age}"
    if gender:
        context += f"\nGender: {gender}"
    
    # Construct prompt for LLM
    prompt = f"""You are a medical education assistant helping to explain possible conditions based on symptoms. 

{context}

Based on these symptoms, please provide:

1. A list of 3-5 POSSIBLE conditions that could be associated with these symptoms (from most to least likely)
2. A list of 5-7 recommended next steps

IMPORTANT GUIDELINES:
- Be educational and informative, not diagnostic
- Always emphasize the need for professional medical evaluation
- Consider common conditions before rare ones
- Mention red flags that require immediate medical attention
- Be clear and easy to understand for general audiences
- DO NOT provide definitive diagnoses
- Focus on general medical education

Format your response as a JSON object with this exact structure:
{{
    "conditions": [
        "Condition 1 name: Brief explanation (1-2 sentences)",
        "Condition 2 name: Brief explanation (1-2 sentences)",
        ...
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        ...
    ]
}}

Ensure your response is ONLY the JSON object, with no additional text before or after."""

    try:
        # Configure generation parameters
        generation_config = genai.GenerationConfig(
            temperature=0.3,  # Lower temperature for more consistent medical info
            max_output_tokens=1500,
        )
        
        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Extract response text
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith('```'):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove trailing ```
        response_text = response_text.strip()
        
        # Parse JSON response
        analysis = json.loads(response_text)
        
        # Validate response structure
        if "conditions" not in analysis or "recommendations" not in analysis:
            raise ValueError("Invalid response structure from LLM")
        
        # Ensure lists are not empty
        if not analysis["conditions"]:
            analysis["conditions"] = ["Unable to determine specific conditions. Please consult a healthcare provider."]
        if not analysis["recommendations"]:
            analysis["recommendations"] = ["Consult with a healthcare professional for proper evaluation."]
        
        return analysis
        
    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text if 'response_text' in locals() else 'No response'}")
        return {
            "conditions": [
                "Analysis could not be completed. The symptoms you described may have multiple possible causes."
            ],
            "recommendations": [
                "Schedule an appointment with your primary care physician",
                "Keep a symptom diary noting when symptoms occur and their severity",
                "Seek immediate medical attention if symptoms worsen or you experience severe pain, difficulty breathing, or other concerning signs"
            ]
        }
    
    except Exception as e:
        print(f"LLM API error: {e}")
        return {
            "conditions": [
                "Unable to analyze symptoms at this time due to a technical error."
            ],
            "recommendations": [
                "Please try again later or consult directly with a healthcare provider",
                "If experiencing severe symptoms, seek immediate medical attention"
            ]
        }