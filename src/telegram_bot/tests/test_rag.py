import pytest
from src.telegram_bot.rag import get_explanation

def test_get_explanation():
    explanation = get_explanation('../../sample_data/sample_signal.json')
    assert explanation is not None
    assert isinstance(explanation, str)
    assert len(explanation) > 10
