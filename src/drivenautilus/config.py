import os
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "remote_name": "gdrive",
    "connection_label": "Google Drive",
    "mount_path": "~/GoogleDrive",
    "vfs_cache_mode": "writes",
    "dir_cache_time": "30m",
    "poll_interval": "1m",
    "vfs_cache_max_size": "1G",
    "auto_mount": False
}

class Config:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/drivenautilus")
        self.config_path = os.path.join(self.config_dir, "config.json")
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    user_data = json.load(f)
                    self.data.update(user_data)
            except Exception as e:
                logger.error(f"Error loading config: {e}")

    def save(self):
        os.makedirs(self.config_dir, exist_ok=True)
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self.save()
        
    @property
    def mount_path_absolute(self) -> str:
        return os.path.expanduser(self.data["mount_path"])
