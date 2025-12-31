# 🚀 PromptPilot AI
> **The AI Orchestration Layer.** Don't learn to prompt. Just pilot.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Pro-4285F4?style=for-the-badge&logo=google)
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Turbo%20V2-000000?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-success?style=for-the-badge)

PromptPilot AI is a **human-first AI interaction system** that automatically converts casual human intent into professional, optimized AI prompts. Users never need to learn "prompt engineering"—the system handles the complexity internally, delivering high-precision text, voice, and image outputs.

---

## ✨ Key Features

### 🧠 1. The Interpretation Layer (The Brain)
Most users don't know how to talk to LLMs. PromptPilot sits between the user and the AI.
* **Casual Input:** "Help me study physics."
* **PromptPilot Core:** Detects user persona (e.g., Student), rewrites the request into a structured pedagogical prompt with learning objectives and tone guidelines.
* **Execution:** Sends the *perfect* prompt to Google Gemini for the best possible result.

### 🗣️ 2. Native Multilingual Voice (ElevenLabs)
* **Talk to it:** Integrated microphone support for hands-free interaction.
* **It talks back:** Uses **ElevenLabs Turbo V2** for ultra-low latency, realistic voice synthesis.
* **80+ Languages:** Speak in Hindi, Spanish, French, or Tamil—PromptPilot detects the language and responds fluently with the correct accent.

### 🎨 3. Gen Z / Modern UI
* **Glassmorphism Design:** A beautiful, dark-mode interface with neon accents and blur effects.
* **Adaptive Persona:** The UI asks "Who are you?" (Kid, Student, Pro) and the AI changes its entire explaining style to match.
* **Markdown Rendering:** Beautifully formatted responses with bolding, lists, and headers (powered by `marked.js`).
* **Prompt Transparency:** Curious how it works? Click the "✨ View Backend Prompt" button on any message to see exactly what the AI sent to the model.

### 🖼️ 4. Multi-Modal Generation
* **Image Generation:** Integrated `Stable Diffusion` pipeline. Just toggle the Image icon, describe what you want, and generate art locally (or via CPU fallback).
* **Document Context:** Upload `.pdf` or `.docx` files. The system reads them instantly and lets you chat with your documents.

### ⚡ 5. Failsafe Architecture
* **Smart Model Selector:** Automatically scans your Google API key permissions to find the best available model (Gemini 1.5 Pro, Flash, or 1.0), preventing "404 Model Not Found" errors.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.10 or higher
* A Google Cloud API Key (for Gemini)
* An ElevenLabs API Key (for Voice)

### 1. Clone the Repository
``bash
**git clone [https://github.com/AYYAPPANAYYANAN/promptpilot-ai.git](https://github.com/AYYAPPANAYYANAN/promptpilot-ai.git)
cd promptpilot-ai**


### 2. Install Dependencies
### pip install fastapi uvicorn google-generativeai elevenlabs diffusers torch accelerate pypdf python-docx

### 3. Set API Keys
*** You must set your API keys inside the promptpilot_ai.py file or export them as environment variables.
GOOGLE_API_KEY = "your_actual_google_key_here"
ELEVENLABS_API_KEY = "your_actual_elevenlabs_key_here"

### 🚀 How to Run
*** python promptpilot_ai.py ***
Once the server starts, open your browser and navigate to:
👉 http://127.0.0.1:8000

### ***⚠️ SECURITY WARNING:** For security reasons, the API keys in this repository have been removed/redacted. You must use your own keys to run the application. Never commit your `promptpilot_ai.py` file to GitHub if it contains your real keys! ***
