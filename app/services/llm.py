from openai import OpenAI
from app.core.config import settings

_client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are an enterprise assistant.
Be accurate and concise.
If the user asks for something unsafe or illegal, refuse briefly and suggest a safe alternative.
If you lack info, say what you need instead of guessing."""

def build_prompt(question: str) -> str:
    return f"""User question:
{question}

Return a helpful answer with clear steps when appropriate.
"""

def ask_llm(question: str) -> str:
    resp = _client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(question)},
        ],
    )
    return resp.output_text
