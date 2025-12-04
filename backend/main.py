from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schema import ChatRequest, ChatResponse
from memory_extraction import MemoryExtractor
from personality_engine import PersonalityEngine
from llm_client import LLMClient

app = FastAPI(title="Assignment-Ready Memory AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


memory_engine = MemoryExtractor()
persona_engine = PersonalityEngine()
llm = LLMClient()

@app.post("/process", response_model=ChatResponse)
def process(req: ChatRequest):


    memory = memory_engine.run(req.messages)


    prompt = f"""
User memory: {memory}
User query: {req.query}
"""

   
    raw_reply = llm.generate(prompt)

    
    final_reply = persona_engine.apply(req.persona, raw_reply)

  
    return {
        "reply": final_reply,
        "memory": memory
    }
