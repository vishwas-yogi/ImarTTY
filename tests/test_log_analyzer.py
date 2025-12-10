import pytest
import os
from utils.log_analyzer import LogAnalyzer

@pytest.fixture
def analyzer():
    return LogAnalyzer()

def test_analyze_file_not_found(analyzer):
    summary, prompt = analyzer.analyze_file("nonexistent.log")
    assert "Error: File not found" in summary
    assert prompt == ""

def test_analyze_file_too_large(analyzer, tmp_path):
    # Create a dummy large file
    large_file = tmp_path / "large.log"
    with open(large_file, "wb") as f:
        f.seek(11 * 1024 * 1024) # 11MB
        f.write(b"\0")
    
    summary, prompt = analyzer.analyze_file(str(large_file))
    assert "Error: File too large" in summary

def test_extract_error_chunk(analyzer, tmp_path):
    log_file = tmp_path / "error.log"
    content = """
    INFO: Starting app
    INFO: Loading config
    ERROR: Connection failed
    Traceback (most recent call last):
      File "app.py", line 10, in <module>
    INFO: Shutting down
    """
    log_file.write_text(content)
    
    summary, prompt = analyzer.analyze_file(str(log_file))
    assert "Found potential issues" in summary
    assert "ERROR: Connection failed" in prompt
    assert "Traceback" in prompt

def test_extract_query_chunk(analyzer, tmp_path):
    log_file = tmp_path / "query.log"
    content = """
    Line 1
    Line 2
    SpecialEvent: Something happened
    Line 4
    """
    log_file.write_text(content)
    
    summary, prompt = analyzer.analyze_file(str(log_file), query="SpecialEvent")
    assert "Found potential issues" in summary
    assert "SpecialEvent" in prompt

def test_clean_log(analyzer, tmp_path):
    log_file = tmp_path / "clean.log"
    content = """
    INFO: All good
    INFO: Still good
    """
    log_file.write_text(content)
    
    summary, prompt = analyzer.analyze_file(str(log_file))
    assert "No obvious errors" in summary
    assert prompt == ""
