import os
import logging
from .command_runner import CommandRunner

logger = logging.getLogger(__name__)

SERVICE_TEMPLATE = """[Unit]
Description=Mount Google Drive in Nautilus with rclone
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStartPre=/usr/bin/mkdir -p {mount_path}
ExecStart=/usr/bin/rclone mount {remote_name}: {mount_path} --vfs-cache-mode {cache_mode} --dir-cache-time {dir_cache_time} --poll-interval {poll_interval} --vfs-cache-max-size {cache_max_size} --volname "{volname}"
ExecStop=/usr/bin/fusermount3 -u {mount_path}
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
"""

class SystemdManager:
    def __init__(self, service_name: str = "drivenautilus-gdrive.service"):
        self.service_name = service_name
        self.service_path = os.path.expanduser(f"~/.config/systemd/user/{self.service_name}")

    def write_user_service(self, remote_name: str, mount_path: str, cache_mode: str, 
                         dir_cache_time: str, poll_interval: str, cache_max_size: str, volname: str):
        os.makedirs(os.path.dirname(self.service_path), exist_ok=True)
        
        # We need to make sure mount_path is absolute and handles %h for systemd if possible, 
        # but absolute path is safer for now as we know the user home.
        # Actually, %h is better for systemd units.
        
        # If mount_path starts with /home/username, replace with %h
        home = os.path.expanduser("~")
        if mount_path.startswith(home):
            mount_path_systemd = mount_path.replace(home, "%h")
        else:
            mount_path_systemd = mount_path

        content = SERVICE_TEMPLATE.format(
            remote_name=remote_name,
            mount_path=mount_path_systemd,
            cache_mode=cache_mode,
            dir_cache_time=dir_cache_time,
            poll_interval=poll_interval,
            cache_max_size=cache_max_size,
            volname=volname
        )
        
        with open(self.service_path, "w") as f:
            f.write(content)
        
        CommandRunner.run_sync(["systemctl", "--user", "daemon-reload"])

    def enable_service(self):
        return CommandRunner.run_sync(["systemctl", "--user", "enable", "--now", self.service_name]).success

    def disable_service(self):
        return CommandRunner.run_sync(["systemctl", "--user", "disable", "--now", self.service_name]).success

    def is_service_enabled(self) -> bool:
        result = CommandRunner.run_sync(["systemctl", "--user", "is-enabled", self.service_name])
        return result.stdout.strip() == "enabled"

    def is_service_active(self) -> bool:
        result = CommandRunner.run_sync(["systemctl", "--user", "is-active", self.service_name])
        return result.stdout.strip() == "active"
