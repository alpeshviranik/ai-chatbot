from diabetes_bot.retriever import Retriever


def test_retrieves_hypoglycemia():
    r = Retriever("data/knowledge")
    results = r.search("what is the 15-15 rule for low blood sugar")
    assert results and "Hypoglycemia" in results[0].source


def test_irrelevant_query_returns_nothing():
    r = Retriever("data/knowledge")
    assert r.search("quantum chromodynamics lagrangian") == []
