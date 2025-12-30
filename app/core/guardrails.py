import re
from dataclasses import dataclass

MAX_QUESTION_CHARS = 800
MAX_RESPONSE_CHARS = 4000

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(\+?\d{1,2}[\s-]?)?(\(?\d{3}\)?[\s-]?)\d{3}[\s-]?\d{4}\b")

@dataclass
class GuardrailResult:
    ok: bool
    reason: str | None = None
    flags: list[str] | None = None

def validate_input(question: str) -> GuardrailResult:
    q = (question or "").strip()
    flags: list[str] = []

    if not q:
        return GuardrailResult(False, "Question is empty.", ["empty"])

    if len(q) > MAX_QUESTION_CHARS:
        return GuardrailResult(False, f"Question too long (>{MAX_QUESTION_CHARS} chars).", ["too_long"])

    if EMAIL_RE.search(q):
        flags.append("pii_email")
    if PHONE_RE.search(q):
        flags.append("pii_phone")

    if flags:
        return GuardrailResult(False, "Potential PII detected. Remove personal info and retry.", flags)

    return GuardrailResult(True, None, flags)

def validate_output(answer: str) -> GuardrailResult:
    a = (answer or "").strip()

    if not a:
        return GuardrailResult(False, "Model returned empty output.", ["empty_output"])

    if len(a) > MAX_RESPONSE_CHARS:
        return GuardrailResult(False, f"Response too long (>{MAX_RESPONSE_CHARS} chars).", ["too_long_output"])

    lowered = a.lower()
    red_flags = ["kill yourself", "how to make a bomb", "credit card number"]
    if any(x in lowered for x in red_flags):
        return GuardrailResult(False, "Unsafe content detected in output.", ["unsafe_output"])

    return GuardrailResult(True, None, [])
