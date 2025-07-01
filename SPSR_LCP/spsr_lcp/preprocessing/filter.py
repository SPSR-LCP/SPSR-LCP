"""
Code filtering module for SPSR-LCP preprocessing.
"""

import os
from typing import List


class CodeFilter:
    """Basic code filter for preprocessing pipeline."""
    
    def __init__(self, config=None):
        """Initialize the code filter."""
        self.config = config or {}
    
    def filter_repository(self, repo_path: str) -> List[str]:
        """
        Filter files in a repository.
        
        Args:
            repo_path (str): Path to repository
            
        Returns:
            List[str]: List of filtered file paths
        """
        # Simple implementation - just find C/C++ files
        filtered_files = []
        
        if not os.path.exists(repo_path):
            return filtered_files
        
        valid_extensions = ['.c', '.cpp', '.h', '.hpp']
        
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if any(file.endswith(ext) for ext in valid_extensions):
                    file_path = os.path.join(root, file)
                    filtered_files.append(file_path)
        
        return filtered_files 