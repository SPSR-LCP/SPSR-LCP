"""
Data preprocessing module for SPSR-LCP.

This module provides tools for cleaning and preparing code data including:
- File filtering based on size, content, and patterns
- Data cleaning and normalization
- Deduplication using hash-based and fuzzy matching
"""

from .filter import CodeFilter
from .cleaner import CodeCleaner
from .deduplicator import CodeDeduplicator

class CodePreprocessor:
    """
    Main preprocessing pipeline that combines filtering, cleaning, and deduplication.
    """
    
    def __init__(self, config=None):
        """
        Initialize the preprocessor with configuration.
        
        Args:
            config (dict, optional): Configuration dictionary
        """
        if config is None:
            config = {}
        
        self.filter = CodeFilter(config.get('filter', {}))
        self.cleaner = CodeCleaner(config.get('cleaner', {}))
        self.deduplicator = CodeDeduplicator(config.get('deduplicator', {}))
    
    def process_repository(self, repo_path, output_path=None):
        """
        Process an entire repository.
        
        Args:
            repo_path (str): Path to the repository
            output_path (str, optional): Path to save processed files
            
        Returns:
            dict: Processing results and statistics
        """
        # Step 1: Find and filter files
        filtered_files = self.filter.filter_repository(repo_path)
        
        # Step 2: Clean the code content
        cleaned_files = []
        for file_path in filtered_files:
            try:
                cleaned_content = self.cleaner.clean_file(file_path)
                cleaned_files.append({
                    'file_path': file_path,
                    'content': cleaned_content
                })
            except Exception as e:
                print(f"Warning: Failed to clean {file_path}: {e}")
        
        # Step 3: Deduplicate
        deduplicated_files = self.deduplicator.deduplicate(cleaned_files)
        
        # Save results if output path provided
        if output_path:
            self._save_processed_files(deduplicated_files, output_path)
        
        return {
            'original_files': len(filtered_files),
            'cleaned_files': len(cleaned_files),
            'deduplicated_files': len(deduplicated_files),
            'files': deduplicated_files
        }
    
    def _save_processed_files(self, files, output_path):
        """Save processed files to output directory."""
        import os
        import json
        
        os.makedirs(output_path, exist_ok=True)
        
        # Save file index
        index_path = os.path.join(output_path, 'file_index.json')
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(files, f, indent=2, ensure_ascii=False)

__all__ = [
    'CodePreprocessor',
    'CodeFilter',
    'CodeCleaner', 
    'CodeDeduplicator'
] 