import os
import uvicorn
import time
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import base64
from io import BytesIO

# --- AI CLIENTS ---
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from diffusers import StableDiffusionPipeline
import torch
from PyPDF2 import PdfReader
from docx import Document

# --- CONFIGURATION ---
app = FastAPI(title="PromptPilot AI", version="GenZ-V5-Final")

# !!! KEYS (Keep these safe) !!!
GOOGLE_API_KEY = "Request to paste the Key" 
ELEVENLABS_API_KEY = "Request to paste the Key"

# --- FAILSAFE MODEL SELECTOR ---
ACTIVE_GOOGLE_MODEL = None

def setup_google_ai():
    global ACTIVE_GOOGLE_MODEL
    if not GOOGLE_API_KEY: return
    
    genai.configure(api_key=GOOGLE_API_KEY)
    print("🔍 Scanning for ANY working Google Model...")
    
    try:
        # Get all models available to your key
        all_models = genai.list_models()
        valid_models = []
        
        for m in all_models:
            # We only want models that can generate text (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                valid_models.append(m.name)
        
        if not valid_models:
            print("❌ CRITICAL: No text generation models found for this API key.")
            return

        # Priority Preference List (Try these first)
        preferences = [
            "models/gemini-1.5-pro-latest",
            "models/gemini-1.5-pro",
            "models/gemini-pro",
            "models/gemini-1.5-flash-latest",
            "models/gemini-1.5-flash"
        ]

        # 1. Try to find a preferred model
        for pref in preferences:
            if pref in valid_models:
                ACTIVE_GOOGLE_MODEL = pref
                print(f"✅ Connected to Preferred Model: {ACTIVE_GOOGLE_MODEL}")
                return
        
        # 2. If no preferred model, JUST PICK THE FIRST ONE that works
        if valid_models:
            ACTIVE_GOOGLE_MODEL = valid_models[0]
            print(f"⚠️ Preferred models missing. Using available fallback: {ACTIVE_GOOGLE_MODEL}")
        else:
             ACTIVE_GOOGLE_MODEL = "gemini-pro" # Absolute fallback

    except Exception as e:
        print(f"❌ Connection Setup Error: {e}")
        # Last resort fallback (standard stable name)
        ACTIVE_GOOGLE_MODEL = "gemini-pro"

# Run setup immediately
setup_google_ai()

elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY else None
image_pipe = None

def get_image_pipe():
    global image_pipe
    if image_pipe is None:
        print("Loading Vision Engine...")
        model_id = "runwayml/stable-diffusion-v1-5"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        image_pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
        image_pipe = image_pipe.to(device)
    return image_pipe

# --- DATA MODELS ---
class ChatRequest(BaseModel):
    user_input: str
    user_profile: Optional[dict] = None
    use_voice: bool = False
    generate_image: bool = False

# --- CORE INTELLIGENCE ---

def interpret_intent(casual_input: str, profile: dict) -> str:
    name = profile.get('name', 'User')
    role = profile.get('role', 'Student')
    
    style_instruction = "Keep the tone helpful and friendly."
    if role == "Kid":
        style_instruction = "The user is a child. Rewrite the prompt to ask for an explanation that uses simple words, fun analogies, emoji, and short sentences. No complex jargon."
    elif role == "Student":
        style_instruction = "The user is a student. Rewrite the prompt to ask for a structured explanation with clear headings, bullet points, and an encouraging tone."
    elif role == "Professional":
        style_instruction = "The user is a professional. Rewrite the prompt to ask for a concise, executive-summary style answer with actionable steps and data-driven tone."

    system_instruction = (
        "You are the PromptPilot Kernel. Your goal is to rewrite the user's raw input into the PERFECT prompt for an AI LLM. "
        "Do not answer the question yourself. Just output the rewritten prompt. "
        f"Context: User is {name}, a {role}. "
        f"{style_instruction}"
    )
    
    try:
        # Failsafe: If setup failed, try 'gemini-pro'
        model_name = ACTIVE_GOOGLE_MODEL if ACTIVE_GOOGLE_MODEL else "gemini-pro"
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f"{system_instruction}\n\nUser Input: {casual_input}")
        return response.text.strip()
    except Exception as e:
        print(f"Interpretation Error: {e}")
        return casual_input

def execute_ai(professional_prompt: str, role: str) -> str:
    try:
        model_name = ACTIVE_GOOGLE_MODEL if ACTIVE_GOOGLE_MODEL else "gemini-pro"
        model = genai.GenerativeModel(model_name)
        format_instruction = " Use clear Markdown formatting (bolding, bullet points) to make the text easy to read."
        response = model.generate_content(professional_prompt + format_instruction)
        return response.text
    except Exception as e:
        return f"Connection Error: {str(e)}"

# --- ENDPOINTS ---

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if request.generate_image:
        try:
            pipe = get_image_pipe()
            image = pipe(request.user_input).images[0]
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return {"response": "Image generated.", "image_data": f"data:image/png;base64,{img_str}", "professional_prompt": request.user_input}
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    professional_prompt = interpret_intent(request.user_input, request.user_profile)
    role = request.user_profile.get('role', 'Student')
    response_text = execute_ai(professional_prompt, role)
    
    audio_data = None
    if request.use_voice and elevenlabs_client:
        try:
            audio = elevenlabs_client.generate(text=response_text[:400], voice="Rachel", model="eleven_turbo_v2")
            audio_data = base64.b64encode(b"".join(audio)).decode()
        except: pass

    return {
        "response": response_text,
        "professional_prompt": professional_prompt,
        "audio_data": audio_data
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    return {"filename": file.filename, "full_content": "Document processing placeholder"}

# --- GEN Z UI ---
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PromptPilot AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
        :root { --bg: #050505; --accent: #3b82f6; --glass: rgba(255,255,255,0.05); }
        body { background: var(--bg); color: #e2e8f0; font-family: 'Outfit', sans-serif; overflow: hidden; }
        .grid-layout { display: grid; grid-template-columns: 260px 1fr; height: 100vh; }
        .sidebar { background: #0a0a0a; border-right: 1px solid #1f1f1f; display: flex; flex-direction: column; }
        .chat-area { display: flex; flex-direction: column; background: radial-gradient(circle at top right, #1e1b4b 0%, #000 40%); height: 100vh; position: relative; }
        #chat { flex: 1; overflow-y: auto; padding-bottom: 120px; scroll-behavior: smooth; }
        .bubble { padding: 16px 20px; border-radius: 18px; max-width: 80%; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); animation: fade 0.3s; line-height: 1.6; }
        .user { align-self: flex-end; background: linear-gradient(135deg, #3b82f6, #2563eb); margin-left: auto; color: white; }
        .ai { align-self: flex-start; background: rgba(30, 30, 30, 0.6); border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
        .ai strong { color: #60a5fa; font-weight: 700; }
        .ai ul { list-style-type: disc; margin-left: 20px; margin-top: 5px; }
        .ai h1, .ai h2, .ai h3 { font-weight: bold; color: white; margin-top: 10px; margin-bottom: 5px; }
        .input-box { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 800px; background: rgba(20,20,20,0.9); backdrop-filter: blur(10px); border: 1px solid #333; border-radius: 20px; padding: 12px; display: flex; align-items: flex-end; gap: 10px; z-index: 10; }
        textarea { background: transparent; border: none; color: white; width: 100%; resize: none; outline: none; padding: 10px; max-height: 100px; }
        .prompt-box { display: none; margin-top: 10px; padding: 10px; background: #000; border-radius: 8px; font-family: monospace; font-size: 0.85rem; color: #4ade80; border: 1px solid #1f2937; }
        .modal { position: fixed; inset: 0; background: rgba(0,0,0,0.9); display: flex; align-items: center; justify-content: center; z-index: 50; }
    </style>
</head>
<body>
    <div id="modal" class="modal">
        <div class="bg-gray-900 p-8 rounded-2xl border border-gray-700 w-96 text-center shadow-2xl shadow-blue-900/20">
            <div class="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">P</div>
            <h2 class="text-2xl font-bold mb-2">Who are you?</h2>
            <p class="text-gray-400 text-sm mb-6">PromptPilot adapts its personality to match you.</p>
            <input id="u-name" type="text" placeholder="Your Name" class="w-full bg-black border border-gray-700 p-3 rounded-lg mb-4 text-white focus:border-blue-500 outline-none">
            <div class="grid grid-cols-3 gap-2 mb-6">
                <button onclick="selectRole('Kid')" class="role-btn p-3 rounded-lg border border-gray-700 hover:bg-blue-600 hover:border-blue-500 transition text-sm">👶 Kid</button>
                <button onclick="selectRole('Student')" class="role-btn p-3 rounded-lg border border-gray-700 hover:bg-blue-600 hover:border-blue-500 transition text-sm">🎓 Student</button>
                <button onclick="selectRole('Professional')" class="role-btn p-3 rounded-lg border border-gray-700 hover:bg-blue-600 hover:border-blue-500 transition text-sm">💼 Pro</button>
            </div>
            <button onclick="launchApp()" class="w-full bg-white text-black hover:bg-gray-200 py-3 rounded-xl font-bold transition">Start Engine</button>
        </div>
    </div>
    <div class="grid-layout">
        <aside class="sidebar p-5">
            <div class="flex items-center gap-3 mb-8 text-white font-bold text-xl tracking-wide">
                <div class="w-8 h-8 bg-blue-600 rounded flex items-center justify-center">P</div> PromptPilot
            </div>
            <div id="history" class="space-y-2 text-sm text-gray-400 overflow-y-auto flex-1"></div>
            <div class="mt-auto pt-4 border-t border-gray-800">
                <div id="user-display" class="font-bold text-white">Guest</div>
                <div id="role-display" class="text-xs text-blue-400">Visitor</div>
            </div>
        </aside>
        <main class="chat-area p-5">
            <div id="chat" class="flex flex-col">
                <div class="bubble ai"><strong>System Online.</strong><br>I am ready to help. I will automatically format my answers based on your age and role.</div>
            </div>
            <div class="input-box">
                <button onclick="document.getElementById('f-up').click()" class="text-gray-400 hover:text-white p-2 transition"><i class="fas fa-paperclip"></i></button>
                <input type="file" id="f-up" class="hidden">
                <button onclick="toggleFeature('img')" id="img-btn" class="text-gray-400 hover:text-white p-2 transition"><i class="fas fa-image"></i></button>
                <button onclick="toggleVoice()" id="v-btn" class="text-gray-400 hover:text-white p-2 transition"><i class="fas fa-microphone"></i></button>
                <textarea id="inp" rows="1" placeholder="Type a message..."></textarea>
                <button onclick="send()" class="bg-blue-600 w-10 h-10 rounded-xl flex items-center justify-center text-white hover:scale-110 transition shadow-lg shadow-blue-600/20"><i class="fas fa-paper-plane"></i></button>
            </div>
        </main>
    </div>
    <script>
        let userProfile = { name: "Guest", role: "Student" };
        let useVoice = false;
        let genImage = false;
        let selectedRoleTemp = "Student";
        function selectRole(role) { selectedRoleTemp = role; document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('bg-blue-600', 'border-blue-500')); event.target.classList.add('bg-blue-600', 'border-blue-500'); }
        function launchApp() { const name = document.getElementById('u-name').value || "Friend"; userProfile = { name: name, role: selectedRoleTemp }; document.getElementById('user-display').innerText = name; document.getElementById('role-display').innerText = selectedRoleTemp; document.getElementById('modal').style.display = 'none'; }
        function toggleVoice() { useVoice = !useVoice; const btn = document.getElementById('v-btn'); btn.style.color = useVoice ? '#ef4444' : '#9ca3af'; if(useVoice) btn.classList.add('animate-pulse'); else btn.classList.remove('animate-pulse'); }
        function toggleFeature(feat) { if(feat === 'img') { genImage = !genImage; document.getElementById('img-btn').style.color = genImage ? '#a855f7' : '#9ca3af'; } }
        function togglePrompt(id) { const el = document.getElementById(id); el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none'; }
        document.getElementById('inp').addEventListener('keydown', (e) => { if(e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } });
        async function send() {
            const txt = document.getElementById('inp').value; if(!txt) return;
            document.getElementById('inp').value = '';
            const chatBox = document.getElementById('chat');
            const uDiv = document.createElement('div'); uDiv.className = 'bubble user'; uDiv.innerText = txt; chatBox.appendChild(uDiv); chatBox.scrollTo(0, chatBox.scrollHeight);
            const loadDiv = document.createElement('div'); loadDiv.className = 'bubble ai animate-pulse'; loadDiv.innerText = "Thinking..."; chatBox.appendChild(loadDiv);
            try {
                const res = await fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ user_input: txt, user_profile: userProfile, use_voice: useVoice, generate_image: genImage }) });
                const data = await res.json();
                chatBox.removeChild(loadDiv);
                const aDiv = document.createElement('div'); aDiv.className = 'bubble ai';
                if(data.image_data) { aDiv.innerHTML = `<img src="${data.image_data}" class="rounded-lg w-full mb-2">`; genImage = false; document.getElementById('img-btn').style.color = '#9ca3af'; }
                else {
                    const cleanHtml = marked.parse(data.response); const promptId = 'p-' + Date.now();
                    aDiv.innerHTML = `<div>${cleanHtml}</div><div class='mt-3 pt-3 border-t border-gray-700'><button onclick="togglePrompt('${promptId}')" class="text-xs text-blue-400 hover:text-white flex items-center gap-1 transition"><i class="fas fa-terminal"></i> View Backend Prompt</button><div id="${promptId}" class="prompt-box">${data.professional_prompt}</div></div>`;
                }
                chatBox.appendChild(aDiv); chatBox.scrollTo(0, chatBox.scrollHeight);
                if(data.audio_data) { new Audio("data:audio/mp3;base64," + data.audio_data).play(); }
            } catch (e) { loadDiv.innerText = "Error: " + e; }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_ui(): return html_content

if __name__ == "__main__":
    uvicorn.run("promptpilot_ai:app", host="127.0.0.1", port=8000, reload=True)