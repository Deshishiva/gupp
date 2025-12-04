import os, requests
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

class LLMClient:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")

        self.openai = OpenAI(api_key=self.openai_key) if self.openai_key else None

   
    def _openai(self, prompt):
        if not self.openai:
            return None
        try:
            res = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return res.choices[0].message.content
        except Exception as e:
            print("OpenAI ERROR:", e)
            return None

  
    def _groq(self, prompt):
        if not self.groq_key:
            return None
        try:
            payload = {
                "model": "llama3-8b-8192-finetuned",  
                "messages": [{"role": "user", "content": prompt}]
            }

            headers = {
                "Authorization": f"Bearer {self.groq_key}",
                "Content-Type": "application/json"
            }

            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=8
            )

            data = r.json()
            print("GROQ RESPONSE:", data)

          
            if "choices" in data:
                return data["choices"][0]["message"]["content"]

            return None

        except Exception as e:
            print("Groq ERROR:", e)
            return None

    
    def generate(self, prompt):
        out = self._openai(prompt)
        if out:
            return out

        out = self._groq(prompt)
        if out:
            return out

        return "LLM error: check API keys"
