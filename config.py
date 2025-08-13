#!/usr/bin/env python3
"""
Configuration and customization for the custom shell
"""

import os
import json
from typing import Dict, Any


class ShellConfig:
    """Shell configuration management"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or os.path.expanduser("~/.custom_shell_config.json")
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "prompt": {
                "format": "{user}@{hostname}:{cwd}$ ",
                "colors": {
                    "user": "green",
                    "hostname": "blue",
                    "cwd": "yellow",
                    "prompt": "white"
                }
            },
            "aliases": {
                "ll": "ls -la",
                "la": "ls -la",
                "l": "ls -l",
                "..": "cd ..",
                "...": "cd ../..",
                "grep": "grep --color=auto",
                "fgrep": "fgrep --color=auto",
                "egrep": "egrep --color=auto"
            },
            "history": {
                "size": 1000,
                "ignore_duplicates": True,
                "ignore_space": True
            },
            "completion": {
                "case_sensitive": False,
                "show_all_if_ambiguous": True,
                "colored_stats": True
            },
            "features": {
                "auto_cd": True,
                "correct_typos": True,
                "glob_expansion": True,
                "brace_expansion": True
            }
        }
        
        try:
            with open(self.config_file, 'r') as f:
                user_config = json.load(f)
                self._merge_config(default_config, user_config)
                return default_config
        except FileNotFoundError:
            return default_config
            
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def _merge_config(self, default: Dict, user: Dict):
        """Recursively merge user config with defaults"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_config(default[key], value)
            else:
                default[key] = value
                
    def get(self, key: str, default=None):
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value


class ColorScheme:
    """ANSI color codes for terminal output"""
    
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'underline': '\033[4m'
    }
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Apply color to text"""
        if color in cls.COLORS:
            return f"{cls.COLORS[color]}{text}{cls.COLORS['reset']}"
        return text
        
    @classmethod
    def get_colored_prompt(cls, prompt_format: str, colors: Dict[str, str], **kwargs) -> str:
        """Generate a colored prompt"""
        colored_parts = {}
        for key, value in kwargs.items():
            color = colors.get(key, 'white')
            colored_parts[key] = cls.colorize(str(value), color)
            
        return prompt_format.format(**colored_parts)


class PluginManager:
    """Simple plugin system for extending shell functionality"""
    
    def __init__(self):
        self.plugins = {}
        self.hooks = {
            'pre_command': [],
            'post_command': [],
            'prompt_update': [],
            'completion': []
        }
        
    def load_plugin(self, plugin_name: str, plugin_module):
        """Load a plugin"""
        self.plugins[plugin_name] = plugin_module
        
        for hook_name in self.hooks:
            if hasattr(plugin_module, f'on_{hook_name}'):
                self.hooks[hook_name].append(getattr(plugin_module, f'on_{hook_name}'))
                
    def execute_hook(self, hook_name: str, *args, **kwargs):
        """Execute all functions registered for a hook"""
        results = []
        for hook_func in self.hooks.get(hook_name, []):
            try:
                result = hook_func(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Plugin hook error: {e}")
        return results
        
    def list_plugins(self):
        """List all loaded plugins"""
        return list(self.plugins.keys())