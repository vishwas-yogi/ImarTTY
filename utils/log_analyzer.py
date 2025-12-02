import os
from typing import Optional, List, Tuple

class LogAnalyzer:
    """
    Analyzes log files to extract errors and generate agent-ready prompts.
    """
    
    # Keywords that suggest an error
    ERROR_KEYWORDS = [
        "Error", "Exception", "Traceback", "Panic", "Fatal", 
        "CRITICAL", "FAIL", "Caused by"
    ]
    
    # Max file size to process (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Lines of context to capture around an error
    CONTEXT_LINES = 20

    def analyze_file(self, file_path: str, query: Optional[str] = None) -> Tuple[str, str]:
        """
        Reads the file and returns a tuple (analysis_summary, handoff_prompt).
        """
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}", ""
            
        if os.path.getsize(file_path) > self.MAX_FILE_SIZE:
            # For large files, read only the last 1MB
            try:
                with open(file_path, 'rb') as f:
                    f.seek(-1024 * 1024, 2) # Seek to 1MB before end
                    content = f.read().decode('utf-8', errors='replace')
                    # Discard first partial line
                    lines = content.splitlines(keepends=True)[1:]
                    # Discard first partial line
                    lines = content.splitlines(keepends=True)[1:]
            except Exception as e:
                return f"Error reading large file: {str(e)}", ""
        else:
            try:
                with open(file_path, 'r', errors='replace') as f:
                    lines = f.readlines()
            except Exception as e:
                return f"Error reading file: {str(e)}", ""

        return self._analyze_lines(lines, file_path, query)

    def analyze_string(self, content: str, source_name: str = "Output", query: Optional[str] = None) -> Tuple[str, str]:
        """
        Analyzes a raw string (e.g. command output).
        """
        lines = content.splitlines(keepends=True)
        return self._analyze_lines(lines, source_name, query)

    def _analyze_lines(self, lines: List[str], source_name: str, query: Optional[str]) -> Tuple[str, str]:
        """
        Internal method to analyze a list of lines.
        """
        relevant_chunk = self._extract_relevant_chunk(lines, query)
        
        if not relevant_chunk:
            return "No obvious errors or matching lines found.", ""

        # Construct the handoff prompt
        handoff_prompt = self._generate_handoff_prompt(source_name, relevant_chunk, query)
        
        return "Analysis complete. Found potential issues.", handoff_prompt

    def _extract_relevant_chunk(self, lines: List[str], query: Optional[str]) -> str:
        """
        Finds the most relevant section of the log.
        Prioritizes the query if present, otherwise looks for error keywords.
        """
        target_line_index = -1
        
        # 1. Search for query if provided
        if query:
            for i, line in enumerate(lines):
                if query.lower() in line.lower():
                    target_line_index = i
                    break
        
        # 2. If no query or not found, search for error keywords (reverse order to find most recent)
        if target_line_index == -1:
            for i in range(len(lines) - 1, -1, -1):
                line = lines[i].lower()
                if any(keyword.lower() in line for keyword in self.ERROR_KEYWORDS):
                    target_line_index = i
                    break
        
        if target_line_index == -1:
            return ""

        # Extract context
        start = max(0, target_line_index - self.CONTEXT_LINES)
        end = min(len(lines), target_line_index + self.CONTEXT_LINES)
        
        return "".join(lines[start:end])

    def _generate_handoff_prompt(self, file_path: str, chunk: str, query: Optional[str]) -> str:
        """
        Creates the formatted prompt for the agent.
        """
        filename = os.path.basename(file_path)
        
        prompt = f"""I am analyzing a log file `{filename}` and found an issue.

[Context]
File: {filename}
Query: {query if query else "Auto-detected error"}

[Log Excerpt]
```text
{chunk}
```

Please analyze this log excerpt, identify the root cause of the error, and suggest a fix.
"""
        return prompt
