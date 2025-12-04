from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schema import ChatRequest, ChatResponse
from memory_extraction import MemoryExtractor
from personality_engine import PersonalityEngine
from llm_client import LLMClient

app = FastAPI(title="Assignment-Ready Memory AI")

# ------------------------------
# CORS FIX FOR RENDER + NETLIFY
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with "https://gupp.netlify.app"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Call language model
    raw_reply = llm.generate(prompt)

    # Apply personality
    final_reply = persona_engine.apply(req.persona, raw_reply)

    # Return to frontend
    return {
        "reply": final_reply,
        "memory": memory
    }
