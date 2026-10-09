import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
key = os.getenv("GROQ_API_KEY")
if not key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=key)

resp = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[{"role": "user", "content": "Reply with exactly: Groq working"}],
    temperature=0,
    max_tokens=20,
)

print(resp.choices[0].message.content)