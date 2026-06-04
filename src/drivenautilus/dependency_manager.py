import shutil
from typing import Dict, List
from .command_runner import CommandRunner

class DependencyManager:
    REQUIRED_COMMANDS = [
        "rclone",
        "fusermount3",
        "systemctl",
        "nautilus",
        "xdg-open"
    ]

    @staticmethod
    def command_exists(command: str) -> bool:
        return shutil.which(command) is not None

    @classmethod
    def check_dependencies(cls) -> Dict[str, bool]:
        return {cmd: cls.command_exists(cmd) for cmd in cls.REQUIRED_COMMANDS}

    @staticmethod
    def is_rclone_snap() -> bool:
        rclone_path = shutil.which("rclone")
        if rclone_path:
            return "/snap/" in rclone_path
        return False

    @staticmethod
    def get_missing_dependencies() -> List[str]:
        missing = []
        for cmd in DependencyManager.REQUIRED_COMMANDS:
            if not DependencyManager.command_exists(cmd):
                missing.append(cmd)
        return missing

    @staticmethod
    def install_dependencies_deb() -> bool:
        # Note: This usually requires sudo. The UI should handle pkexec or similar.
        # For now, we return the command that should be run.
        cmd = ["pkexec", "apt", "install", "-y", "rclone", "fuse3", "nautilus"]
        result = CommandRunner.run_sync(cmd)
        return result.success
