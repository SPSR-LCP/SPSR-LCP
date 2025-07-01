"""Graph data types."""

class CodeNode:
    """Basic code node."""
    def __init__(self, name):
        self.name = name

class CodeEdge:
    """Basic code edge."""
    def __init__(self, source, target):
        self.source = source
        self.target = target

class SPSRGraph:
    """Basic SPSR Graph."""
    def __init__(self):
        self.nodes = []
        self.edges = []
