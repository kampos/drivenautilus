import subprocess
import asyncio
import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

class CommandResult:
    def __init__(self, returncode: int, stdout: str, stderr: str):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.success = returncode == 0

class CommandRunner:
    @staticmethod
    def run_sync(cmd: List[str], timeout: Optional[int] = None) -> CommandResult:
        logger.info(f"Running sync command: {' '.join(cmd)}")
        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
            return CommandResult(process.returncode, process.stdout, process.stderr)
        except subprocess.TimeoutExpired as e:
            logger.error(f"Command timed out: {' '.join(cmd)}")
            return CommandResult(-1, e.stdout.decode() if e.stdout else "", "Timeout expired")
        except Exception as e:
            logger.error(f"Error running command {' '.join(cmd)}: {e}")
            return CommandResult(-1, "", str(e))

    @staticmethod
    async def run_async(cmd: List[str]) -> CommandResult:
        logger.info(f"Running async command: {' '.join(cmd)}")
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return CommandResult(
                process.returncode or 0,
                stdout.decode(),
                stderr.decode()
            )
        except Exception as e:
            logger.error(f"Error running async command {' '.join(cmd)}: {e}")
            return CommandResult(-1, "", str(e))
