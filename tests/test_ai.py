from utils.ai import get_command_suggestion
import os

def test_ai():
    print("Testing AI integration...")
    if not os.getenv("GEMINI_API_KEY"):
        print("SKIP: GEMINI_API_KEY not found.")
        return

    query = "list all python files in the current directory"
    print(f"Query: {query}")
    suggestion = get_command_suggestion(query)
    print(f"Suggestion: {suggestion}")
    
    assert suggestion is not None
    assert len(suggestion) > 0
    assert "ls" in suggestion or "find" in suggestion
    print("PASS: AI suggestion received.")

if __name__ == "__main__":
    test_ai()
