import pytest
import os
from utils.commander import execute_command

@pytest.mark.asyncio
async def test_echo():
    output = []
    async def callback(text):
        output.append(text)

    exit_code, full_output = await execute_command("echo hello", callback)
    assert exit_code == 0
    assert "hello" in full_output

@pytest.mark.asyncio
async def test_cd():
    original_cwd = os.getcwd()
    target_dir = "/tmp"
    
    async def callback(text):
        pass

    exit_code, _ = await execute_command(f"cd {target_dir}", callback)
    assert exit_code == 0
    assert os.getcwd() == target_dir
    
    # Cleanup
    os.chdir(original_cwd)

@pytest.mark.asyncio
async def test_cd_fail():
    async def callback(text):
        pass
        
    exit_code, output = await execute_command("cd /nonexistent", callback)
    assert exit_code == 1
    assert "no such file" in output.lower()

@pytest.mark.asyncio
async def test_exit():
    async def callback(text):
        pass
        
    exit_code, output = await execute_command("exit", callback)
    assert exit_code == 0
    assert "Exit command received" in output
