import asyncio
import os
from utils.commander import execute_command

async def test_commander():
    print("Testing 'echo hello'...")
    output = []
    async def callback(text):
        output.append(text)
        print(f"Callback received: {repr(text)}")

    await execute_command("echo hello", callback)
    assert "hello\n" in output or "hello" in output
    print("PASS: echo hello")

    print("\nTesting 'cd'...")
    original_cwd = os.getcwd()
    target_dir = "/tmp"
    await execute_command(f"cd {target_dir}", callback)
    new_cwd = os.getcwd()
    print(f"Original: {original_cwd}, New: {new_cwd}")
    assert new_cwd == target_dir
    print("PASS: cd /tmp")

    print("\nTesting 'cd ..'...")
    await execute_command("cd ..", callback)
    final_cwd = os.getcwd()
    print(f"Final: {final_cwd}")
    assert final_cwd == "/"
    print("PASS: cd ..")

    print("\nTesting 'ls' (streaming)...")
    output.clear()
    await execute_command("ls -1 /bin | head -n 3", callback)
    assert len(output) > 0
    print("PASS: ls streaming")

if __name__ == "__main__":
    asyncio.run(test_commander())
