import asyncio
import os
import shlex
from typing import Callable, Awaitable

async def execute_command(command: str, output_callback: Callable[[str], Awaitable[None]]) -> None:
    """
    Executes a shell command and streams the output to the callback.
    Handles built-in commands like 'cd' and 'exit'.
    """
    command = command.strip()
    if not command:
        return

    # Handle built-in commands
    parts = shlex.split(command)
    cmd_name = parts[0]

    if cmd_name == "cd":
        try:
            target_dir = parts[1] if len(parts) > 1 else os.path.expanduser("~")
            os.chdir(target_dir)
            # No output needed for successful cd, but maybe we want to show the new path?
            # For now, let's just silently succeed like a real shell, or maybe print the new path.
            # Let's print nothing on success to mimic standard behavior, 
            # but if it fails we catch it below.
        except FileNotFoundError:
            await output_callback(f"cd: no such file or directory: {parts[1]}\n")
        except Exception as e:
            await output_callback(f"cd: {str(e)}\n")
        return

    if cmd_name == "exit":
        # In a real app we might want to close the app here.
        # For now, let's just print a message. The UI can handle the actual exit if needed.
        await output_callback("Exit command received. Press Ctrl+C to quit the app for now.\n")
        return

    # Run external commands
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Helper to read stream
        async def read_stream(stream, callback):
            while True:
                line = await stream.readline()
                if not line:
                    break
                await callback(line.decode('utf-8', errors='replace'))

        # Run both readers concurrently
        await asyncio.gather(
            read_stream(process.stdout, output_callback),
            read_stream(process.stderr, output_callback)
        )

        await process.wait()

    except Exception as e:
        await output_callback(f"Error executing command: {str(e)}\n")
