from abc import ABC, abstractmethod
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from utils.logger import get_logger

load_dotenv()
logger = get_logger("ai")

class AIProvider(ABC):
    @abstractmethod
    def get_command_suggestion(self, query: str, context: str = "") -> str:
        pass

    @abstractmethod
    def fix_command(self, command: str, error_output: str, context: str = "") -> str:
        pass
    
    @abstractmethod
    def explain_command(self, command: str, context: str = "") -> str:
        pass

class GeminiProvider(AIProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in .env")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')

    def _build_prompt(self, base_prompt: str, context: str) -> str:
        if context:
            return f"[Context]\n{context}\n\n[Request]\n{base_prompt}"
        return base_prompt

    def get_command_suggestion(self, query: str, context: str = "") -> str:
        if not hasattr(self, 'model'):
            return "Error: Gemini API key not configured."
            
        base_prompt = (
            "You are a shell command expert. Translate the user's request into a single, "
            "executable shell command for Linux. Return ONLY the command, no markdown, "
            "no explanations, no code blocks. "
            f"Request: {query}"
        )
        prompt = self._build_prompt(base_prompt, context)
        
        try:
            logger.info(f"Gemini suggestion requested for: {query}")
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return f"Error calling Gemini API: {str(e)}"

    def fix_command(self, command: str, error_output: str, context: str = "") -> str:
        if not hasattr(self, 'model'):
            return "Error: Gemini API key not configured."

        base_prompt = (
            f"The command `{command}` failed with the following error:\n"
            f"{error_output}\n"
            "Provide a corrected shell command to fix this error. "
            "Return ONLY the corrected command, no markdown, no explanations."
        )
        prompt = self._build_prompt(base_prompt, context)

        try:
            logger.info(f"Gemini fix requested for command: {command}")
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return f"Error calling Gemini API: {str(e)}"

    def explain_command(self, command: str, context: str = "") -> str:
        if not hasattr(self, 'model'):
            return "Error: Gemini API key not configured."

        base_prompt = (
            f"Explain the following shell command concisely:\n"
            f"`{command}`\n"
            "Explain what it does and what the flags mean."
        )
        prompt = self._build_prompt(base_prompt, context)

        try:
            logger.info(f"Gemini explanation requested for command: {command}")
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return f"Error calling Gemini API: {str(e)}"

class OllamaProvider(AIProvider):
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def _generate(self, prompt: str) -> str:
        try:
            logger.info(f"Ollama request (model={self.model_name})")
            response = requests.post(self.api_url, json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            
            logger.error(f"Ollama error status: {response.status_code}")
            return f"Error: Ollama returned status {response.status_code}"
        except Exception as e:
            logger.error(f"Ollama exception: {e}")
            return f"Error calling Ollama: {str(e)}"

    def _build_prompt(self, base_prompt: str, context: str) -> str:
        if context:
            return f"[Context]\n{context}\n\n[Request]\n{base_prompt}"
        return base_prompt

    def get_command_suggestion(self, query: str, context: str = "") -> str:
        base_prompt = (
            "You are a shell command expert. Translate the user's request into a single, "
            "executable shell command for Linux. Return ONLY the command, no markdown, "
            "no explanations, no code blocks. "
            f"Request: {query}"
        )
        return self._generate(self._build_prompt(base_prompt, context))

    def fix_command(self, command: str, error_output: str, context: str = "") -> str:
        base_prompt = (
            f"The command `{command}` failed with the following error:\n"
            f"{error_output}\n"
            "Provide a corrected shell command to fix this error. "
            "Return ONLY the corrected command, no markdown, no explanations."
        )
        return self._generate(self._build_prompt(base_prompt, context))

    def explain_command(self, command: str, context: str = "") -> str:
        base_prompt = (
            f"Explain the following shell command concisely:\n"
            f"`{command}`\n"
            "Explain what it does and what the flags mean."
        )
        return self._generate(self._build_prompt(base_prompt, context))

def get_provider(provider_name: str) -> AIProvider:
    if provider_name.lower() == "ollama":
        return OllamaProvider()
    return GeminiProvider()
