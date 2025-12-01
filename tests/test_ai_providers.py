import pytest
from unittest.mock import MagicMock, patch
from utils.ai import GeminiProvider, OllamaProvider, get_provider

@pytest.fixture
def mock_genai():
    with patch('utils.ai.genai') as mock:
        yield mock

@pytest.fixture
def mock_requests():
    with patch('utils.ai.requests') as mock:
        yield mock

@pytest.fixture
def mock_env():
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'fake_key'}):
        yield

def test_gemini_provider_init(mock_env, mock_genai):
    provider = GeminiProvider()
    mock_genai.configure.assert_called_with(api_key='fake_key')
    assert provider.model is not None

def test_gemini_get_suggestion(mock_env, mock_genai):
    provider = GeminiProvider()
    mock_response = MagicMock()
    mock_response.text = "ls -la"
    provider.model.generate_content.return_value = mock_response
    
    result = provider.get_command_suggestion("list files")
    assert result == "ls -la"
    provider.model.generate_content.assert_called_once()

def test_ollama_provider_init():
    provider = OllamaProvider()
    assert provider.api_url == "http://localhost:11434/api/generate"

def test_ollama_get_suggestion(mock_requests):
    provider = OllamaProvider()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "ls -la"}
    mock_requests.post.return_value = mock_response
    
    result = provider.get_command_suggestion("list files")
    assert result == "ls -la"
    mock_requests.post.assert_called_once()

def test_get_provider(mock_env, mock_genai):
    assert isinstance(get_provider("gemini"), GeminiProvider)
    assert isinstance(get_provider("ollama"), OllamaProvider)
    # Default
    assert isinstance(get_provider("unknown"), GeminiProvider)
