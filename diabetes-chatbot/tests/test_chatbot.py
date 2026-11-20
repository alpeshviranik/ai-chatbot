from types import SimpleNamespace
from diabetes_bot.chatbot import DiabetesChatbot
from diabetes_bot.retriever import Retriever


class FakeClient:
    def __init__(self):
        self.messages = self
    def create(self, **kw):
        return SimpleNamespace(content=[SimpleNamespace(type="text", text="fake answer")])


def make_bot():
    return DiabetesChatbot(retriever=Retriever("data/knowledge"), client=FakeClient())


def test_emergency_skips_llm():
    out = make_bot().respond("s", "he is unconscious")
    assert out["escalated"] and not out["sources"]


def test_grounded_answer_has_sources():
    out = make_bot().respond("s", "How do I treat low blood sugar?")
    assert out["answer"] == "fake answer" and out["sources"]
