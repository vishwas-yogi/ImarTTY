import os
from pathlib import Path
from typing import List, Dict, Set

class ContextManager:
    """
    Manages context detection for the current shell session.
    Identifies project types and key files to provide context to the AI.
    """

    # Map of project type to characteristic files
    PROJECT_SIGNATURES = {
        "Python": {"pyproject.toml", "requirements.txt", "setup.py", "Pipfile", "manage.py"},
        "Node/JS/TS": {"package.json", "yarn.lock", "pnpm-lock.yaml", "tsconfig.json"},
        "Rust": {"Cargo.toml"},
        "Go": {"go.mod"},
        "Docker": {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"},
        "Makefile": {"Makefile"},
    }

    # Files that are useful to mention to the AI
    KEY_FILES = {
        "pyproject.toml", "requirements.txt", "setup.py", "Pipfile", "manage.py",
        "package.json", "tsconfig.json",
        "Cargo.toml",
        "go.mod",
        "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
        "Makefile",
        "README.md",
        ".env.example"
    }

    def get_project_context(self, cwd: str) -> str:
        """
        Scans the directory and returns a formatted context string.
        """
        project_types = self._detect_project_types(cwd)
        key_files = self._find_key_files(cwd)
        
        context_parts = [f"Path: {cwd}"]
        
        if project_types:
            context_parts.append(f"Type: {', '.join(project_types)}")
        
        if key_files:
            context_parts.append(f"Key Files: {', '.join(key_files)}")
            
        return "\n".join(context_parts)

    def _detect_project_types(self, cwd: str) -> List[str]:
        """
        Identifies project types based on file existence.
        """
        detected = []
        try:
            # Get all files in top level directory
            files = {f.name for f in Path(cwd).iterdir() if f.is_file()}
            
            for p_type, signatures in self.PROJECT_SIGNATURES.items():
                if files.intersection(signatures):
                    detected.append(p_type)
            
            # Special check for C#/.NET (wildcards)
            if any(f.endswith('.csproj') or f.endswith('.sln') for f in files):
                 detected.append("C#/.NET")
                 
        except Exception:
            # Gracefully handle permission errors or non-existent paths
            pass
            
        return sorted(detected)

    def _find_key_files(self, cwd: str) -> List[str]:
        """
        Returns a list of important files found in the directory.
        """
        found_files = []
        try:
            files = {f.name for f in Path(cwd).iterdir() if f.is_file()}
            
            # Add exact matches
            found_files.extend(sorted(list(files.intersection(self.KEY_FILES))))
            
            # Add C# project files
            found_files.extend(sorted([f for f in files if f.endswith('.csproj') or f.endswith('.sln')]))
            
        except Exception:
            pass
            
        return found_files
