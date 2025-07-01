"""
AST processing module for structure-aware semantic segmentation.

This module provides tools for:
- Parsing source code into Abstract Syntax Trees
- Semantic segmentation based on AST structure  
- Structure validation and completeness checking
- Multi-granularity semantic unit extraction
"""

from .parser import CodeParser
from .semantic_segmentation import ASTSemanticSegmentation
from .validator import StructureValidator

__all__ = [
    'CodeParser',
    'ASTSemanticSegmentation', 
    'StructureValidator'
] 