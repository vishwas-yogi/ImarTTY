import os
import pytest
from utils.context import ContextManager

@pytest.fixture
def context_manager():
    return ContextManager()

def test_detect_python_project(context_manager, tmp_path):
    (tmp_path / "pyproject.toml").touch()
    (tmp_path / "main.py").touch()
    
    context = context_manager.get_project_context(str(tmp_path))
    assert "Type: Python" in context
    assert "Key Files: pyproject.toml" in context

def test_detect_node_project(context_manager, tmp_path):
    (tmp_path / "package.json").touch()
    (tmp_path / "index.js").touch()
    
    context = context_manager.get_project_context(str(tmp_path))
    assert "Type: Node/JS/TS" in context
    assert "Key Files: package.json" in context

def test_detect_csharp_project(context_manager, tmp_path):
    (tmp_path / "MyProject.csproj").touch()
    (tmp_path / "Program.cs").touch()
    
    context = context_manager.get_project_context(str(tmp_path))
    assert "Type: C#/.NET" in context
    assert "Key Files: MyProject.csproj" in context

def test_detect_mixed_project(context_manager, tmp_path):
    (tmp_path / "pyproject.toml").touch()
    (tmp_path / "Dockerfile").touch()
    
    context = context_manager.get_project_context(str(tmp_path))
    assert "Python" in context
    assert "Docker" in context
    assert "Key Files: Dockerfile, pyproject.toml" in context

def test_empty_directory(context_manager, tmp_path):
    context = context_manager.get_project_context(str(tmp_path))
    assert f"Path: {str(tmp_path)}" in context
    assert "Type:" not in context
    assert "Key Files:" not in context
