from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class UIState:
    dependencies_installed: bool = False
    missing_deps: List[str] = field(default_factory=list)
    rclone_is_snap: bool = False
    gdrive_configured: bool = False
    is_mounted: bool = False
    auto_mount_active: bool = False
    last_error: str = ""
    logs: List[str] = field(default_factory=list)

    def add_log(self, message: str):
        self.logs.append(message)
        if len(self.logs) > 100:
            self.logs.pop(0)
