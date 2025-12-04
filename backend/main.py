from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schema import ChatRequest, ChatResponse
from memory_extraction import MemoryExtractor
from personality_engine import PersonalityEngine
from llm_client import LLMClient

app = FastAPI(title="Assignment-Ready Memory AI")

# CORS for Render backend + Netlify frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend domain later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core engines
memory_engine = MemoryExtractor()
persona_engine = PersonalityEngine()
llm = LLMClient()

@app.post("/process", response_model=ChatResponse)
def process(req: ChatRequest):

    # Extract memory from messages
    memory = memory_engine.run(req.messages)

    # Build LLM prompt
    prompt = f"""
User memory: {memory}
User query: {req.query}
"""

    # Generate reply using OpenAI / Groq
    raw_reply = llm.generate(prompt)

    # Apply selected personality
    final_reply = persona_engine.apply(req.persona, raw_reply)

    # Send result to frontend
    return {
        "reply": final_reply,
        "memory": memory
    }
