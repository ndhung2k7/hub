"""
Application settings management
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


class Settings:
    """Application settings manager"""
    
    def __init__(self, config_file="settings.json"):
        self.config_file = Path(config_file)
        self.settings = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load settings from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save(self):
        """Save settings to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except:
            pass
    
    def get(self, key: str, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set setting value"""
        self.settings[key] = value
        self.save()
    
    def get_last_output_dir(self) -> str:
        """Get last output directory"""
        return self.get('last_output_dir', '')
    
    def set_last_output_dir(self, path: str):
        """Set last output directory"""
        self.set('last_output_dir', path)
    
    def get_last_video_dir(self) -> str:
        """Get last video directory"""
        return self.get('last_video_dir', '')
    
    def set_last_video_dir(self, path: str):
        """Set last video directory"""
        self.set('last_video_dir', path)
