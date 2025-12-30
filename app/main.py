import time
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.guardrails import validate_input, validate_output
from app.core.logging import write_jsonl, utc_ts
from app.services.llm import ask_llm

app = FastAPI(title="Enterprise AI Assistant (Guardrailed)")

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)

class AskResponse(BaseModel):
    answer: str
    guardrails: dict
    latency_ms: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    start = time.time()

    in_result = validate_input(req.question)
    if not in_result.ok:
        write_jsonl(settings.log_path, {
            "ts": utc_ts(),
            "event": "blocked_input",
            "question": req.question,
            "flags": in_result.flags or [],
            "reason": in_result.reason,
        })
        return AskResponse(
            answer=in_result.reason or "Blocked by guardrails.",
            guardrails={"stage": "input", "ok": False, "flags": in_result.flags or []},
            latency_ms=int((time.time() - start) * 1000),
        )

    answer = ask_llm(req.question)

    out_result = validate_output(answer)
    if not out_result.ok:
        write_jsonl(settings.log_path, {
            "ts": utc_ts(),
            "event": "blocked_output",
            "question": req.question,
            "raw_answer": answer,
            "flags": out_result.flags or [],
            "reason": out_result.reason,
        })
        return AskResponse(
            answer=out_result.reason or "Blocked output.",
            guardrails={"stage": "output", "ok": False, "flags": out_result.flags or []},
            latency_ms=int((time.time() - start) * 1000),
        )

    latency_ms = int((time.time() - start) * 1000)

    write_jsonl(settings.log_path, {
        "ts": utc_ts(),
        "event": "interaction",
        "question": req.question,
        "answer": answer,
        "latency_ms": latency_ms,
        "guardrails": {"input_flags": in_result.flags or [], "output_flags": out_result.flags or []},
        "model": settings.openai_model,
        "env": settings.app_env,
    })

    return AskResponse(
        answer=answer,
        guardrails={"stage": "none", "ok": True, "flags": []},
        latency_ms=latency_ms,
    )