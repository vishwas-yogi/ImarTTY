import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_command_suggestion(query: str) -> str:
    """
    Uses Gemini to translate a natural language query into a shell command.
    """
    if not api_key:
        return "Error: GEMINI_API_KEY not found in .env file."

    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        prompt = (
            "You are a shell command expert. Translate the user's request into a single, "
            "executable shell command for Linux. Return ONLY the command, no markdown, "
            "no explanations, no code blocks. "
            f"Request: {query}"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"
