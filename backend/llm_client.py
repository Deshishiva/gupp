import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load .env ONLY for local development
# In production (Render), env vars are injected automatically
load_dotenv()


class LLMClient:
    def __init__(self):
        # Read environment variables
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        self.groq_key = os.environ.get("GROQ_API_KEY")

        # Debug logs (safe – no secrets printed)
        print("OPENAI KEY FOUND:", bool(self.openai_key))
        print("GROQ KEY FOUND:", bool(self.groq_key))

        # Initialize OpenAI client if key exists
        self.openai = OpenAI(api_key=self.openai_key) if self.openai_key else None

    # -------------------------
    # OpenAI provider
    # -------------------------
    def _openai(self, prompt: str):
        if not self.openai:
            return None

        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=8
            )

            return response.choices[0].message.content

        except Exception as e:
            print("OpenAI ERROR:", e)
            return None

    # -------------------------
    # Groq provider (fallback)
    # -------------------------
    def _groq(self, prompt: str):
        if not self.groq_key:
            return None

        try:
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            headers = {
                "Authorization": f"Bearer {self.groq_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=8
            )

            data = response.json()
            print("GROQ RESPONSE STATUS:", response.status_code)

            if "choices" in data:
                return data["choices"][0]["message"]["content"]

            return None

        except Exception as e:
            print("Groq ERROR:", e)
            return None

    # -------------------------
    # Public method
    # -------------------------
    def generate(self, prompt: str) -> str:
        # Try OpenAI first
        out = self._openai(prompt)
        if out:
            return out

        # Fallback to Groq
        print("Falling back to Groq...")
        out = self._groq(prompt)
        if out:
            return out

        # Final failure
        return "LLM error: no valid API keys or provider unavailable"
