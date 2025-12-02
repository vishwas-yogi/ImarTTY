import asyncio
import os
import shlex
from typing import Callable, Awaitable

async def execute_command(command: str, output_callback: Callable[[str], Awaitable[None]], max_buffer_size: int = 1024 * 1024) -> tuple[int, str]:
    """
    Executes a shell command and streams the output to the callback.
    Handles built-in commands like 'cd' and 'exit'.
    Returns (exit_code, full_output).
    full_output is truncated to the last max_buffer_size bytes if it exceeds the limit.
    """
    command = command.strip()
    if not command:
        return 0, ""

    full_output = []
    current_size = 0

    async def wrapped_callback(text: str):
        nonlocal current_size
        full_output.append(text)
        current_size += len(text)
        
        # Simple truncation strategy: if we exceed 2x buffer, slice to 1x buffer
        # This avoids slicing on every append
        if current_size > max_buffer_size * 2:
            # Reconstruct string to slice correctly
            temp_str = "".join(full_output)
            temp_str = temp_str[-max_buffer_size:]
            full_output.clear()
            full_output.append(temp_str)
            current_size = len(temp_str)
            
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
        
        # Final truncation check
        final_str = "".join(full_output)
        if len(final_str) > max_buffer_size:
            final_str = final_str[-max_buffer_size:]
            
        return process.returncode, final_str

    except Exception as e:
        msg = f"Error executing command: {str(e)}\n"
        await wrapped_callback(msg)
        return 1, msg
