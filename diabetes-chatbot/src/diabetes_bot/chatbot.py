from collections import defaultdict
from typing import Dict, List

from .config import settings
from .retriever import Retriever
from . import safety

SYSTEM_PROMPT = """You are a supportive assistant that answers patient questions about diabetes.

Rules:
- Answer ONLY using the provided context passages. If they don't contain the answer, say you don't have reliable information on that and suggest contacting their healthcare provider.
- Never diagnose, never recommend or change medication/insulin doses.
- Use plain, kind, non-judgmental language at about an 8th-grade reading level.
- Keep answers concise (under 150 words) and use short lists when helpful.
- If symptoms sound urgent, advise seeking emergency care.
- End with a brief reminder to confirm personal decisions with their care team when relevant."""

NO_CONTEXT_MESSAGE = (
    "I don't have reliable information on that. Please check with your doctor, "
    "diabetes educator, or pharmacist."
)


class DiabetesChatbot:
    def __init__(self, retriever: Retriever | None = None, client=None):
        self.retriever = retriever or Retriever(settings.knowledge_dir)
        self._client = client
        self.history: Dict[str, List[dict]] = defaultdict(list)

    @property
    def client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=settings.api_key)
        return self._client

    def respond(self, session_id: str, message: str) -> dict:
        triage = safety.check(message)
        if triage.blocks_llm:
            return {"answer": triage.message, "sources": [], "escalated": True}

        passages = self.retriever.search(message, k=settings.top_k)
        if not passages:
            return {"answer": NO_CONTEXT_MESSAGE, "sources": [], "escalated": False}

        context = "\n\n".join(f"[{p.source}]\n{p.text}" for p in passages)
        user_content = f"Context passages:\n{context}\n\nPatient question: {message}"

        turns = self.history[session_id][-settings.max_history_turns * 2:]
        messages = turns + [{"role": "user", "content": user_content}]

        resp = self.client.messages.create(
            model=settings.model_name,
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        answer = "".join(b.text for b in resp.content if b.type == "text")

        # store the plain question (not the context) to keep history compact
        self.history[session_id] += [
            {"role": "user", "content": message},
            {"role": "assistant", "content": answer},
        ]
        return {"answer": answer, "sources": [p.source for p in passages], "escalated": False}
