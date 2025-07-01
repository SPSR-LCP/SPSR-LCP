"""
LCP (Longest Common Prefix) metric implementation.

The LCP metric measures the length of the longest common prefix between 
the model's prediction and the reference text. This metric aligns well 
with user perception in code completion tasks.
"""

from typing import List
from .base import StringMetric, MetricResults
import numpy as np


class LCP(StringMetric):
    """
    Longest Common Prefix (LCP) metric.
    
    This metric computes the length of the longest common prefix between
    prediction and reference strings. It shows strong correlation (r > 0.7) 
    with user adoption rates in real-world code completion scenarios.
    """
    
    def __init__(self, normalize: bool = True, case_sensitive: bool = True):
        """
        Initialize the LCP metric.
        
        Args:
            normalize (bool): Whether to normalize whitespace in inputs
            case_sensitive (bool): Whether comparison should be case-sensitive
        """
        super().__init__(name="LCP", normalize=normalize, case_sensitive=case_sensitive)
    
    def compute(self, prediction: str, reference: str) -> int:
        """
        Compute the LCP score between prediction and reference.
        
        Args:
            prediction (str): The model's prediction
            reference (str): The ground truth reference
            
        Returns:
            int: Length of the longest common prefix
        """
        # Preprocess both strings
        pred_processed = self.preprocess_text(prediction)
        ref_processed = self.preprocess_text(reference)
        
        return self._compute_character_lcp(pred_processed, ref_processed)
    
    def _compute_character_lcp(self, prediction: str, reference: str) -> int:
        """
        Compute character-level LCP.
        
        Args:
            prediction (str): Preprocessed prediction string
            reference (str): Preprocessed reference string
            
        Returns:
            int: Length of character-level LCP
        """
        min_length = min(len(prediction), len(reference))
        lcp_length = 0
        
        for i in range(min_length):
            if prediction[i] == reference[i]:
                lcp_length += 1
            else:
                break
        
        return lcp_length
    
    def compute_batch(self, predictions: List[str], references: List[str]) -> MetricResults:
        """
        Compute LCP scores for a batch of predictions.
        
        Args:
            predictions (List[str]): List of model predictions
            references (List[str]): List of ground truth references
            
        Returns:
            MetricResults: Results with LCP scores and statistics
        """
        results = super().compute_batch(predictions, references)
        
        # Add LCP-specific metadata
        scores = results.scores
        total_chars_ref = sum(len(self.preprocess_text(r)) for r in references)
        
        results.add_metadata('total_reference_chars', total_chars_ref)
        results.add_metadata('total_lcp_chars', sum(scores))
        results.add_metadata('lcp_coverage_rate', 
                           sum(scores) / total_chars_ref if total_chars_ref > 0 else 0.0)
        
        return results


class NormalizedLCP(LCP):
    """
    Normalized LCP metric that returns LCP as a fraction of reference length.
    
    This variant normalizes the LCP score by the reference length, making it
    easier to compare across samples with different reference lengths.
    """
    
    def __init__(self, **kwargs):
        """Initialize normalized LCP metric."""
        super().__init__(**kwargs)
        self.name = "Normalized_LCP"
    
    def compute(self, prediction: str, reference: str) -> float:
        """
        Compute normalized LCP score.
        
        Args:
            prediction (str): The model's prediction
            reference (str): The ground truth reference
            
        Returns:
            float: LCP length divided by reference length (0.0 to 1.0)
        """
        ref_processed = self.preprocess_text(reference)
        if not ref_processed:
            return 0.0
        
        lcp_length = super().compute(prediction, reference)
        return lcp_length / len(ref_processed) 