# 🚀 PromptPilot AI

PromptPilot AI automatically converts **casual human input into professional AI prompts as an internal execution step**, then runs the AI and returns accurate results with **multilingual voice output**.

Users never need to know how to write prompts.

---

## ✨ What Problem Does This Solve?

Most people don’t know how to prompt AI properly.  
Bad prompts lead to bad results.

PromptPilot fixes this by adding an **internal prompt-optimization layer** that works automatically during execution.

---

## 🧠 How It Works (Internally)
The professional prompt is an **intermediate process inside the system**, not something the user has to write.

---

## 🌍 Key Features

- Casual input → professional AI prompt (automatic)
- Prompt optimization happens internally during execution
- Supports **80+ languages** (auto-detection + translation)
- Real-time **voice output using ElevenLabs**
- Mobile-first **Gen-Z friendly UI**
- Datadog-style observability (latency & health)
- Single-file Python application (easy to run)

---

## 🛠️ Tech Stack

- Python
- FastAPI
- ElevenLabs (Text → Speech)
- Language Detection & Translation
- Event-style observability logging

---

## 🔐 API Key Setup (Required)

For security reasons, **API keys are NOT included** in this repository.

### Get ElevenLabs API Key
1. Sign up at https://elevenlabs.io  
2. Go to **Profile → API Keys**
3. Create a new API key  

### Set Environment Variable

#### Windows (PowerShell)
**Poweshell**
**setx ELEVENLABS_API_KEY "your_api_key_here"**  

### **macOS / Linux**

**export ELEVENLABS_API_KEY="your_api_key_here"**  

**Restart the terminal after setting the key.**  

**Run the code :**  
**pip install fastapi uvicorn langdetect deep-translator elevenlabs python-multipart**  
**uvicorn promptpilot_all_in_one:app --reload**  

**Open in browser:**  
**http://127.0.0.1:8000**
