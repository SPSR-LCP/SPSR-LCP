"""
Code deduplication module for SPSR-LCP preprocessing.
"""

from typing import List, Dict


class CodeDeduplicator:
    """Basic code deduplicator for preprocessing pipeline."""
    
    def __init__(self, config=None):
        """Initialize the deduplicator."""
        self.config = config or {}
    
    def deduplicate(self, files: List[Dict]) -> List[Dict]:
        """
        Deduplicate a list of files.
        
        Args:
            files (List[Dict]): List of file dictionaries
            
        Returns:
            List[Dict]: Deduplicated files
        """
        # Simple deduplication based on content hash
        seen_contents = set()
        deduplicated = []
        
        for file_data in files:
            content = file_data.get('content', '')
            content_hash = hash(content)
            
            if content_hash not in seen_contents:
                seen_contents.add(content_hash)
                deduplicated.append(file_data)
        
        return deduplicated 