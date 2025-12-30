# PromptPilot AI

PromptPilot AI is a human-first AI interaction system that automatically converts casual human intent into professional AI execution, without requiring users to write prompts.

---

## 1. How to Run PromptPilot AI

This section explains exactly how to install, configure, and run the project.

---

### 1.1 Prerequisites

- Python 3.10 or higher
- Internet connection (for language model and voice services)
- Optional GPU (recommended for faster image generation, but not required)

PromptPilot AI runs on:
- Windows
- macOS
- Linux

---

### 1.2 Install Dependencies

Run the following commands in your terminal:

bash
pip install fastapi uvicorn langdetect groq elevenlabs python-multipart
pip install diffusers torch accelerate safetensors pillow pypdf python-docx

1.3 API Key Setup (Required)
For security reasons, API keys are not included in the source code and must be provided via environment variables.
Windows (PowerShell)
setx GROQ_API_KEY "your_groq_api_key_here"
setx ELEVENLABS_API_KEY "your_elevenlabs_api_key_here"

After setting the keys:
Close PowerShell completely
Open a new terminal session

macOS / Linux
export GROQ_API_KEY="your_groq_api_key_here"
export ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"

1.4 Run the Application
uvicorn promptpilot_ai:app --reload
Open your browser and navigate to:
http://127.0.0.1:8000

2. Core Concept
Most AI systems require users to learn prompt engineering to achieve good results.
PromptPilot AI removes this requirement entirely.
Users interact using natural human language.
PromptPilot internally:
Interprets user intent
Constructs professional AI execution prompts
Maintains conversational context
Executes AI reliably and consistently
The professional prompt exists only inside the system, not in the user interface.


3. Key Advancements
This section lists all major advancements implemented from the initial idea to the final system.

3.1 Promptless Interaction Layer
Casual human input is transformed into structured AI instructions
Prompt engineering is handled entirely by the system
Users never need to understand or write prompts

3.2 Conversational Intelligence
Two-way conversation between user and AI
Multi-turn memory per session
Context-aware responses
Chat-style interaction familiar to global users

3.3 Multilingual Intelligence
Automatic language detection (80+ languages)
No manual language selection required
Default fallback to English when detection confidence is low
Language consistency across text and voice output

3.4 Voice Output
High-quality speech synthesis using ElevenLabs
Language-aware voice responses
Supports hands-free and accessibility use cases
Voice treated as a first-class output modality

3.5 Image Generation (Diffusers-Ready)
Integration with local, open-source diffusion models
Unlimited image generation (limited only by hardware)
CPU-safe execution with automatic GPU acceleration if available
PromptPilot internally generates optimized image prompts

3.6 Document Intelligence
Supports PDF and DOC/DOCX uploads
Automatic text extraction
Documents treated as human intent
AI can summarize, explain, or analyze documents conversationally

3.7 User Context Awareness
Optional onboarding information:
First name
Age group (range-based, not exact age)
Role (student, working professional, other)
AI adapts explanation depth and tone accordingly
No sensitive personal data collected

3.8 Prompt Transparency (Optional)
Advanced users can view internally generated prompts
Prompts can be edited and re-executed
Default experience remains fully promptless

3.9 Personalization and Settings
Adjustable font size
Font style selection
Text color themes
Preferences stored locally in the browser

3.10 Responsive and Cross-Platform Design
Mobile-first user interface
Tablet, laptop, and desktop support
Modern blue-black aesthetic
Fast startup and low operational overhead
Single-file Python architecture

4. Architecture Overview

Human Input (Text / Voice / Document / Image Intent)
               ↓
      PromptPilot Interpretation Layer
               ↓
      Structured AI Execution
               ↓
     Text / Voice / Image Output

##     PromptPilot functions as an AI orchestration and interpretation layer rather than a traditional chatbot.

5. Security and Responsible AI
No API keys stored in source code
Secrets managed via environment variables
No training or fine-tuning on user data
No biometric or sensitive personal information collected
Session data is temporary and resettable

