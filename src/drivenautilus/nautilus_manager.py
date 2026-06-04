import os
import logging
from .command_runner import CommandRunner

logger = logging.getLogger(__name__)

class NautilusManager:
    @staticmethod
    def open_in_nautilus(path: str):
        path = os.path.expanduser(path)
        CommandRunner.run_sync(["nautilus", path])

    @staticmethod
    def try_add_bookmark(path: str, label: str = "Google Drive"):
        path = os.path.abspath(os.path.expanduser(path))
        bookmark_path = os.path.expanduser("~/.config/gtk-3.0/bookmarks")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(bookmark_path), exist_ok=True)
        
        entry = f"file://{path} {label}"
        
        lines = []
        if os.path.exists(bookmark_path):
            with open(bookmark_path, "r") as f:
                lines = f.readlines()
        
        # Check if already exists (even with different label for same path)
        path_uri = f"file://{path}"
        new_lines = []
        exists = False
        for line in lines:
            if line.strip().startswith(path_uri):
                if line.strip() == entry:
                    exists = True
                    new_lines.append(line)
                else:
                    # Replace old label for same path
                    new_lines.append(f"{entry}\n")
                    exists = True
            else:
                new_lines.append(line)
        
        if not exists:
            new_lines.append(f"{entry}\n")
            
        with open(bookmark_path, "w") as f:
            f.writelines(new_lines)
        
        return True

    @staticmethod
    def remove_bookmark(path: str):
        path = os.path.abspath(os.path.expanduser(path))
        bookmark_path = os.path.expanduser("~/.config/gtk-3.0/bookmarks")
        
        if not os.path.exists(bookmark_path):
            return True
            
        path_uri = f"file://{path}"
        with open(bookmark_path, "r") as f:
            lines = f.readlines()
            
        new_lines = [line for line in lines if not line.strip().startswith(path_uri)]
        
        with open(bookmark_path, "w") as f:
            f.writelines(new_lines)
            
        return True
