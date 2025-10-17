# Demo Script - Healthcare Symptom Checker

## Demo Video Guide

This document provides a step-by-step script for creating your demo video.

---

## Introduction (30 seconds)

**[Show title slide or application homepage]**

"Hello! Today I'm demonstrating the Healthcare Symptom Checker, an AI-powered educational tool that helps users understand possible conditions based on their symptoms. This is a full-stack application built with FastAPI backend and vanilla JavaScript frontend, integrated with Claude AI by Anthropic."

---

## Part 1: Project Overview (1 minute)

**[Show project structure in file explorer or IDE]**

"Let me show you the project structure. We have:
- A **backend** folder with Python FastAPI server, LLM integration, and SQLite database
- A **frontend** folder with HTML, CSS, and JavaScript
- Complete documentation including README and this demo script

The application follows a clean architecture with clear separation of concerns."

---

## Part 2: Backend Demonstration (2 minutes)

**[Show terminal/command prompt]**

### Starting the Backend

"First, let's start the backend server. I've already set my Anthropic API key as an environment variable."

```bash
# Show the command
python backend/app.py
```

**[Show server starting up]**

"The FastAPI server is now running on port 8000. Let's check the API documentation."

**[Open browser to http://localhost:8000/docs]**

"FastAPI automatically generates interactive API documentation. We have three main endpoints:
1. **/analyze** - POST endpoint for symptom analysis
2. **/history** - GET endpoint to retrieve past queries
3. **/health** - GET endpoint for health checks"

**[Click on /analyze endpoint and show the schema]**

"The analyze endpoint accepts symptoms, and optional age and gender fields. It returns possible conditions, recommendations, and a medical disclaimer."

---

## Part 3: Frontend Demonstration (3 minutes)

**[Open frontend/index.html in browser]**

"Now let's use the web interface. Notice the clean, professional design with a prominent medical disclaimer at the top."

### Test Case 1: Common Symptoms

**[Fill in the form]**

"Let me enter some common symptoms:"

- **Symptoms**: "I have been experiencing a persistent headache for 3 days, along with fatigue and mild fever around 100°F. I also feel body aches."
- **Age**: 28
- **Gender**: Female

**[Click "Analyze Symptoms"]**

"The application is now sending the request to our backend, which uses Claude AI to analyze the symptoms."

**[Wait for results]**

"Great! We received the analysis. Let's look at the results:

1. **Possible Conditions**: The AI has identified several potential conditions with explanations, ranked from most to least likely. Notice how each condition includes educational information.

2. **Recommendations**: We get specific, actionable next steps like monitoring symptoms, staying hydrated, and when to seek medical attention.

3. **Medical Disclaimer**: A comprehensive disclaimer is displayed, emphasizing this is for educational purposes only."

### Test Case 2: Different Symptoms

**[Click "Start New Search"]**

"Let me try another example with different symptoms:"

- **Symptoms**: "Sore throat for 2 days, difficulty swallowing, and swollen neck glands. No fever."
- **Age**: 45
- **Gender**: Male

**[Click "Analyze Symptoms" and show results]**

"Again, we get relevant possible conditions and practical recommendations tailored to these specific symptoms."

---

## Part 4: Code Walkthrough (2 minutes)

**[Show code in IDE/editor]**

### Backend Code

**[Open backend/app.py]**

"Let's look at the key components:

1. **FastAPI Application**: Clean RESTful API with proper error handling and CORS configuration for frontend communication.

2. **Input Validation**: Using Pydantic models for request validation with constraints like minimum/maximum length and age ranges."

**[Open backend/llm_client.py]**

"Here's the LLM integration:
- We use Claude Sonnet 4 for analysis
- The prompt is carefully crafted to prioritize safety and education
- Temperature is set to 0.3 for consistent responses
- We request structured JSON output for easy parsing
- Robust error handling with fallback responses"

**[Open backend/database.py]**

"The database layer:
- Simple SQLite implementation
- Stores all queries with timestamps
- Conditions and recommendations are stored as JSON
- Automatic database initialization"

### Frontend Code

**[Open frontend/index.html]**

"The frontend:
- Clean, accessible HTML structure
- Real-time character counter
- Async JavaScript for API communication
- Loading states and error handling
- Responsive design"

---

## Part 5: API Testing (1 minute)

**[Open browser to http://localhost:8000/history]**

"We can also access the query history directly through the API. This shows all previous symptom analyses stored in our database."

**[Show JSON response]**

"Each query includes the original symptoms, analysis results, and timestamp."

---

## Part 6: Key Features Highlight (1 minute)

**[Switch between browser tabs showing the app]**

"Let me highlight the key features that meet the assignment requirements:

✅ **LLM Integration**: Claude AI analyzes symptoms with intelligent reasoning

✅ **Symptom Input**: Text-based symptom description with optional demographic info

✅ **Condition Suggestions**: Multiple possible conditions with educational explanations

✅ **Recommendations**: Actionable next steps for users

✅ **Safety Disclaimers**: Prominent warnings throughout the user journey

✅ **Database Storage**: All queries logged in SQLite for history tracking

✅ **Clean Code Design**: Modular architecture with separation of concerns

✅ **Professional UI**: User-friendly interface with responsive design

✅ **Error Handling**: Graceful error management at all levels"

---

## Part 7: Safety & Ethics (30 seconds)

**[Show disclaimer on screen]**

"Most importantly, this application prioritizes user safety:
- Medical disclaimers are shown prominently
- The LLM is instructed to educate, not diagnose
- Users are consistently directed to healthcare professionals
- The application emphasizes its educational purpose"

---

## Conclusion (30 seconds)

**[Show homepage]**

"In summary, the Healthcare Symptom Checker successfully demonstrates:
- Full-stack development with Python and JavaScript
- LLM integration for intelligent analysis
- Database management for query history
- Professional UI/UX design
- Strong emphasis on safety and medical ethics

All code is available in the GitHub repository with comprehensive documentation. Thank you for watching!"

---

## Recording Tips

1. **Preparation**:
   - Test everything before recording
   - Have sample symptoms ready
   - Close unnecessary applications
   - Use screen recording software (OBS, QuickTime, etc.)

2. **Recording Settings**:
   - 1080p resolution minimum
   - Clear audio (use a decent microphone)
   - 15-20 FPS is sufficient for code demos
   - Include cursor highlighting if possible

3. **During Recording**:
   - Speak clearly and at a moderate pace
   - Pause briefly between sections
   - Show code and results clearly
   - Avoid long silent periods

4. **Editing**:
   - Trim any mistakes or long pauses
   - Add text overlays for key points if desired
   - Total length: 8-12 minutes is ideal
   - Export in MP4 format for compatibility

5. **Upload**:
   - YouTube (unlisted or public)
   - Google Drive with public link
   - Include link in README.md

---

## Troubleshooting Common Demo Issues

### Backend won't start
- Check API key is set correctly
- Verify all dependencies are installed
- Check port 8000 is not in use

### Frontend can't connect
- Ensure backend is running
- Check CORS configuration
- Verify API_BASE_URL in index.html

### LLM returns errors
- Verify API key validity
- Check internet connection
- Ensure Anthropic API is accessible

### Database errors
- Check write permissions in backend folder
- Delete symptom_checker.db and restart to reset

Good luck with your demo!