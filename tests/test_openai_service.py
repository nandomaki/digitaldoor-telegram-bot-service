import builtins
from unittest.mock import patch, MagicMock
from scripts.openai_services import OpenAIService


def test_validate_answer_true():
    service = OpenAIService(api_key="test")
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "TRUE"
    mock_response.choices = [mock_choice]

    with patch.object(service.client.chat.completions, "create", return_value=mock_response):
        result = service.validate_answer(1, "Fulano de Tal")
        assert result == "TRUE"
