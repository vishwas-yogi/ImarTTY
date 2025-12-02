import pytest
import asyncio
import os
from utils.commander import execute_command
from utils.log_analyzer import LogAnalyzer

@pytest.mark.asyncio
async def test_execute_command_truncation():
    # Create a command that outputs more than the buffer size
    # Buffer size 10 bytes, output 20 bytes
    cmd = "echo '12345678901234567890'"
    
    async def noop(text):
        pass
        
    exit_code, output = await execute_command(cmd, noop, max_buffer_size=10)
    
    # Output should be truncated to last 10 chars
    assert len(output) <= 10
    # We expect the end of the string to be preserved
    assert output.strip().endswith("67890")

def test_analyze_large_file(tmp_path):
    analyzer = LogAnalyzer()
    large_file = tmp_path / "large.log"
    
def test_analyze_large_file(tmp_path):
    analyzer = LogAnalyzer()
    large_file = tmp_path / "large.log"
    
    # Create a large file with valid text and newlines
    # Write 1MB of padding lines, then the error
    # 1024 lines of 1024 chars = 1MB
    padding_line = "x" * 1023 + "\n"
    with open(large_file, "w") as f:
        for _ in range(10 * 1024): # 10MB
            f.write(padding_line)
        f.write("ERROR: End of file error\n")
        
    summary, prompt = analyzer.analyze_file(str(large_file))
    
    # Should not error
    assert "Error: File too large" not in summary
    # Should find the error at the end
    assert "ERROR: End of file error" in prompt
