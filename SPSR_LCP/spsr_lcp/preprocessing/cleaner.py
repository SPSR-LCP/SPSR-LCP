"""
Code cleaning module for SPSR-LCP preprocessing.
"""


class CodeCleaner:
    """Basic code cleaner for preprocessing pipeline."""
    
    def __init__(self, config=None):
        """Initialize the code cleaner."""
        self.config = config or {}
    
    def clean_file(self, file_path: str) -> str:
        """
        Clean a source code file.
        
        Args:
            file_path (str): Path to file
            
        Returns:
            str: Cleaned file content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic cleaning - just return the content for now
            return content.strip()
            
        except Exception as e:
            print(f"Error cleaning file {file_path}: {e}")
            return "" 