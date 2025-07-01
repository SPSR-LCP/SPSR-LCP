"""
Utility functions and constants for the SPSR-LCP package.

This module provides common utilities including:
- File I/O operations
- Logging configuration
- Constants and configuration loading
- Helper functions for data processing
"""

from .file_io import (
    read_source_code,
    write_json_file,
    load_json_file,
    ensure_directory,
    find_source_files
)
from .logger import setup_logging, get_logger
from .constants import (
    SUPPORTED_LANGUAGES,
    DEFAULT_CONFIG,
    AST_NODE_TYPES,
    METRIC_RANGES
)

try:
    from .config import load_config, save_config, merge_configs
except ImportError:
    # Provide fallback if yaml not available
    def load_config(config_path):
        """Fallback config loader."""
        import json
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def save_config(config, config_path):
        """Fallback config saver."""
        import json
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def merge_configs(base_config, override_config):
        """Fallback config merger."""
        merged = base_config.copy()
        merged.update(override_config)
        return merged

__all__ = [
    'read_source_code',
    'write_json_file', 
    'load_json_file',
    'ensure_directory',
    'find_source_files',
    'setup_logging',
    'get_logger',
    'load_config',
    'save_config',
    'merge_configs',
    'SUPPORTED_LANGUAGES',
    'DEFAULT_CONFIG',
    'AST_NODE_TYPES',
    'METRIC_RANGES'
] 