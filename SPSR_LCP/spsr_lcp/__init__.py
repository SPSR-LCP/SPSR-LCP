"""
SPSR-LCP: Structure-Aware Corpus Construction and User-Perception-Aligned Metrics for LLM Code Completion

This package provides tools for:
1. Evaluating code completion models with user-perception-aligned metrics (LCP, ROUGE-LCP)
2. Constructing structure-aware training corpora using SPSR-Graph
3. Processing code repositories with AST-based semantic segmentation

Main components:
- metrics: LCP and ROUGE-LCP evaluation metrics
- preprocessing: Data filtering, cleaning, and deduplication
- ast_processing: AST-based semantic segmentation and parsing
- graph: SPSR-Graph construction and traversal
- utils: Utility functions and constants
"""

__version__ = "1.0.0"
__author__ = "Research Team"
__email__ = "contact@spsr-lcp-research.org"

# Import main classes and functions for easy access
from .metrics import LCP, ROUGE_LCP, evaluate_batch
from .preprocessing import CodePreprocessor
from .ast_processing import ASTSemanticSegmentation, CodeParser
from .graph import SPSRGraphBuilder, CallChainGenerator
from .utils import setup_logging, load_config

# Main pipeline class
class SPSRLCPPipeline:
    """
    Main pipeline for SPSR-LCP processing and evaluation.
    
    This class provides a high-level interface for:
    1. Processing repositories to create structure-aware training corpora
    2. Evaluating model outputs with LCP/ROUGE-LCP metrics
    3. End-to-end corpus construction and evaluation workflow
    """
    
    def __init__(self, config=None):
        """
        Initialize the SPSR-LCP pipeline.
        
        Args:
            config (dict, optional): Configuration dictionary. If None, uses default settings.
        """
        if config is None:
            config = {}
        
        self.config = config
        self.preprocessor = CodePreprocessor(config.get('preprocessing', {}))
        self.ast_processor = ASTSemanticSegmentation(config.get('ast_processing', {}))
        self.graph_builder = SPSRGraphBuilder(config.get('graph', {}))
        
        # Initialize metrics
        self.lcp_metric = LCP()
        self.rouge_lcp_metric = ROUGE_LCP()
    
    def process_repository(self, repo_path, output_path, config=None):
        """
        Process a repository to create structure-aware training corpus.
        
        Args:
            repo_path (str): Path to the source repository
            output_path (str): Path to save the processed corpus
            config (dict, optional): Processing configuration
            
        Returns:
            dict: Processing statistics and results
        """
        if config is None:
            config = self.config
        
        # Step 1: Preprocess repository
        processed_files = self.preprocessor.process_repository(repo_path)
        
        # Step 2: AST-based semantic segmentation
        segmented_data = self.ast_processor.segment_files(processed_files)
        
        # Step 3: Build SPSR-Graph
        spsr_graph = self.graph_builder.build_graph(segmented_data)
        
        # Step 4: Generate training samples
        training_samples = self.graph_builder.generate_training_samples(
            spsr_graph, 
            max_depth=config.get('max_depth', 3),
            max_children=config.get('max_children', 5)
        )
        
        # Step 5: Save results
        self._save_training_corpus(training_samples, output_path)
        
        return {
            'num_files_processed': len(processed_files),
            'num_training_samples': len(training_samples),
            'graph_nodes': len(spsr_graph.nodes),
            'graph_edges': len(spsr_graph.edges),
            'output_path': output_path
        }
    
    def evaluate(self, predictions_file, references_file, output_file=None):
        """
        Evaluate model predictions using LCP and ROUGE-LCP metrics.
        
        Args:
            predictions_file (str): Path to predictions JSON file
            references_file (str): Path to references JSON file
            output_file (str, optional): Path to save evaluation results
            
        Returns:
            dict: Evaluation results
        """
        results = evaluate_batch(
            predictions_file=predictions_file,
            references_file=references_file,
            metrics=['lcp', 'rouge_lcp', 'em', 'bleu']
        )
        
        if output_file:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        
        return results
    
    def _save_training_corpus(self, training_samples, output_path):
        """Save training corpus to file."""
        import json
        import os
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_samples, f, indent=2, ensure_ascii=False)

# Export main classes and functions
__all__ = [
    'SPSRLCPPipeline',
    'LCP',
    'ROUGE_LCP',
    'CodePreprocessor', 
    'ASTSemanticSegmentation',
    'CodeParser',
    'SPSRGraphBuilder',
    'CallChainGenerator',
    'evaluate_batch',
    'setup_logging',
    'load_config'
] 