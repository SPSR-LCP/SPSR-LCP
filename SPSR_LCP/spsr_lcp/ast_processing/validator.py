"""
Structure validation module.
"""


class StructureValidator:
    """Basic structure validator."""
    
    def __init__(self, config=None):
        """Initialize the validator."""
        self.config = config or {}
    
    def validate(self, data):
        """Validate structure."""
        return True 