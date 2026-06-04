import os
import logging
from .command_runner import CommandRunner

logger = logging.getLogger(__name__)

class MountManager:
    def __init__(self, remote_name: str, mount_path: str):
        self.remote_name = remote_name
        self.mount_path = os.path.expanduser(mount_path)

    def ensure_mount_folder(self):
        if not os.path.exists(self.mount_path):
            os.makedirs(self.mount_path, exist_ok=True)

    def is_mounted(self) -> bool:
        # Using findmnt is more reliable
        result = CommandRunner.run_sync(["findmnt", "-r", self.mount_path])
        return result.success

    async def mount(self, cache_mode: str = "writes", dir_cache_time: str = "30m", 
                  poll_interval: str = "1m", cache_max_size: str = "1G", volname: Optional[str] = None):
        self.ensure_mount_folder()
        
        cmd = [
            "rclone", "mount", f"{self.remote_name}:", self.mount_path,
            "--vfs-cache-mode", cache_mode,
            "--dir-cache-time", dir_cache_time,
            "--poll-interval", poll_interval,
            "--vfs-cache-max-size", cache_max_size,
            "--daemon"
        ]
        
        if volname:
            cmd.extend(["--volname", volname])
            
        return await CommandRunner.run_async(cmd)

    async def unmount(self):
        cmd = ["fusermount3", "-u", self.mount_path]
        return await CommandRunner.run_async(cmd)

    def open_mount_folder(self):
        CommandRunner.run_sync(["xdg-open", self.mount_path])
        # Or specifically with nautilus
        # CommandRunner.run_sync(["nautilus", self.mount_path])
