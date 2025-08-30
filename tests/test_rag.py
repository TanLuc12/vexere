import pytest
from src.rag.pipeline import VexereRAGPipeline

@pytest.mark.parametrize("question", [
    "Làm thế nào để đặt vé?"
])
def test_rag_query(question):
    rag = VexereRAGPipeline()
    result = rag.query(question)

    assert isinstance(result, dict)
    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0
