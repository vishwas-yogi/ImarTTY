import asyncio
import os
import shlex
from typing import Callable, Awaitable

async def execute_command(command: str, output_callback: Callable[[str], Awaitable[None]]) -> tuple[int, str]:
    """
    Executes a shell command and streams the output to the callback.
    Handles built-in commands like 'cd' and 'exit'.
    Returns (exit_code, full_output).
    """
    command = command.strip()
    if not command:
        return 0, ""

    full_output = []

    async def wrapped_callback(text: str):
        full_output.append(text)
        await output_callback(text)

    # Handle built-in commands
    parts = shlex.split(command)
    cmd_name = parts[0]

    if cmd_name == "cd":
        try:
            target_dir = parts[1] if len(parts) > 1 else os.path.expanduser("~")
            os.chdir(target_dir)
            return 0, ""
        except FileNotFoundError:
            msg = f"cd: no such file or directory: {parts[1]}\n"
            await wrapped_callback(msg)
            return 1, msg
        except Exception as e:
            msg = f"cd: {str(e)}\n"
            await wrapped_callback(msg)
            return 1, msg

    if cmd_name == "exit":
        msg = "Exit command received. Press Ctrl+C to quit the app for now.\n"
        await wrapped_callback(msg)
        return 0, msg

    # Run external commands
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Helper to read stream
        async def read_stream(stream):
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded_line = line.decode('utf-8', errors='replace')
                await wrapped_callback(decoded_line)

        # Run both readers concurrently
        await asyncio.gather(
            read_stream(process.stdout),
            read_stream(process.stderr)
        )

        await process.wait()
        return process.returncode, "".join(full_output)

    except Exception as e:
        msg = f"Error executing command: {str(e)}\n"
        await wrapped_callback(msg)
        return 1, msg
