import logging
from typing import List, Optional
from .command_runner import CommandRunner

logger = logging.getLogger(__name__)

class RcloneManager:
    def __init__(self, remote_name: str = "gdrive"):
        self.remote_name = remote_name

    def list_remotes(self) -> List[str]:
        result = CommandRunner.run_sync(["rclone", "listremotes"])
        if result.success:
            return [line.strip().rstrip(":") for line in result.stdout.splitlines()]
        return []

    def remote_exists(self) -> bool:
        remotes = self.list_remotes()
        return self.remote_name in remotes

    async def configure_google_drive(self):
        # rclone config create <name> drive
        # This will open a browser for OAuth
        cmd = ["rclone", "config", "create", self.remote_name, "drive"]
        return await CommandRunner.run_async(cmd)

    def test_remote(self) -> bool:
        # Check if we can list the root directory
        result = CommandRunner.run_sync(["rclone", "lsd", f"{self.remote_name}:"], timeout=10)
        return result.success

    def get_version(self) -> str:
        result = CommandRunner.run_sync(["rclone", "version"])
        if result.success:
            return result.stdout.splitlines()[0]
        return "Unknown"
