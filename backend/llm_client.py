import json
from typing import Optional
import ollama

# The model we downloaded
MODEL_NAME = "llama3:8b"

async def get_symptom_analysis(
    symptoms: str,
    age: Optional[int] = None,
    gender: Optional[str] = None
) -> dict:
    """
    Use a local Ollama LLM to analyze symptoms and provide educational information.
    """
    
    context = f"Patient Symptoms: {symptoms}"
    if age:
        context += f", Age: {age}"
    if gender:
        context += f", Gender: {gender}"
    
    prompt = f"""You are a helpful medical education assistant. Your task is to analyze the user's symptoms and provide a structured JSON response.

Based on the following information: '{context}'

1.  List 3 to 5 possible conditions, from most to least likely, each with a brief 1-2 sentence explanation.
2.  Provide a list of 5 to 7 recommended next steps.

IMPORTANT RULES:
- Your response MUST be ONLY a valid JSON object.
- The JSON object must have two keys: "conditions" (a list of strings) and "recommendations" (a list of strings).
- DO NOT include any text, greetings, or markdown formatting like ```json before or after the JSON object.
- This is for educational purposes only. Do not provide a diagnosis. Emphasize consulting a real doctor."""

    try:
        # Call the local Ollama model and ask for a JSON response
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
        
        analysis = json.loads(response['message']['content'])
        
        if "conditions" not in analysis or "recommendations" not in analysis:
            raise ValueError("Invalid response structure from local LLM")
            
        return analysis

    except Exception as e:
        print(f"Local LLM error: {e}")
        return {
            "conditions": ["Unable to analyze symptoms due to a local technical error."],
            "recommendations": [
                "Ensure the Ollama application is running and the 'gemma3:27b' model is downloaded.",
                "If the problem persists, consult a healthcare provider directly."
            ]
        }