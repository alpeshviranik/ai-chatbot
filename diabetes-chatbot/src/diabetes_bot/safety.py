"""Rule-based triage that runs BEFORE the LLM."""
import re
from dataclasses import dataclass
from typing import Optional

EMERGENCY_PATTERNS = [
    r"\b(unconscious|passed out|unresponsive|not waking up|won'?t wake)\b",
    r"\bseizure|convulsion",
    r"\b(can'?t|cannot|trouble|difficulty) breath",
    r"\bchest pain\b",
    r"\bfruity (smell|breath)\b",
    r"\b(vomiting|throwing up).{0,40}(ketone|can'?t keep|diabet)",
    r"\bketones?\b.{0,30}\b(high|large|moderate)\b",
    r"\b(severe|extreme) (confusion|drowsiness)\b",
    r"\bglucose.{0,15}\b(under|below|<)\s*(40)\b",
]

SELF_HARM_PATTERNS = [
    r"\b(kill myself|end my life|suicid|want to die|hurt myself)\b",
    r"\b(overdose|take all my insulin).{0,30}(on purpose|to die)\b",
]

DOSING_PATTERNS = [
    r"\b(how (much|many)|what).{0,30}\b(units?|dose|dosage)\b",
    r"\b(change|increase|decrease|adjust|skip|stop|double)\b.{0,30}\b(insulin|metformin|medication|medicine|dose)\b",
]

EMERGENCY_MESSAGE = (
    "This could be a medical emergency. Please call your local emergency number "
    "(911 in the US) or go to the nearest emergency department right now. "
    "If someone is unconscious or having a seizure, do not give food or drink by mouth. "
    "Do not wait for an online answer."
)

SELF_HARM_MESSAGE = (
    "I'm really sorry you're feeling this way. You deserve support right now. "
    "If you're in immediate danger, call your local emergency number. In the US you can "
    "call or text 988 (Suicide & Crisis Lifeline). If you can, reach out to someone you "
    "trust or your care team too."
)

DOSING_MESSAGE = (
    "I can't recommend or change medication or insulin doses, as the right dose depends "
    "on your personal situation. Please contact your doctor, diabetes educator, or "
    "pharmacist. Meanwhile, I can share general educational information if you'd like."
)


@dataclass
class SafetyResult:
    level: str  # "ok" | "emergency" | "self_harm" | "dosing"
    message: Optional[str] = None

    @property
    def blocks_llm(self) -> bool:
        return self.level != "ok"


def _match(patterns, text) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check(text: str) -> SafetyResult:
    if _match(SELF_HARM_PATTERNS, text):
        return SafetyResult("self_harm", SELF_HARM_MESSAGE)
    if _match(EMERGENCY_PATTERNS, text):
        return SafetyResult("emergency", EMERGENCY_MESSAGE)
    if _match(DOSING_PATTERNS, text):
        return SafetyResult("dosing", DOSING_MESSAGE)
    return SafetyResult("ok")
