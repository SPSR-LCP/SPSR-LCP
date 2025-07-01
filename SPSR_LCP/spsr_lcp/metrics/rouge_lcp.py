"""
ROUGE-LCP metric implementation.

ROUGE-LCP is a normalized variant of the LCP metric that divides the LCP score
by the reference length, enabling fair comparison across samples of different lengths.

Formula: ROUGE-LCP(S, R) = LCP(S, R) / |R|

Where S is the prediction, R is the reference, and |R| is the reference length.
"""

from typing import List
from .base import StringMetric, MetricResults
from .lcp import LCP


class ROUGE_LCP(StringMetric):
    """
    ROUGE-LCP (Normalized Longest Common Prefix) metric.
    
    This metric normalizes the LCP score by the reference length, making it
    suitable for comparing code completion performance across samples with
    different reference lengths. The score ranges from 0.0 to 1.0 (or higher
    if the prediction is longer than the reference).
    """
    
    def __init__(self, normalize: bool = True, case_sensitive: bool = True):
        """
        Initialize the ROUGE-LCP metric.
        
        Args:
            normalize (bool): Whether to normalize whitespace in inputs
            case_sensitive (bool): Whether comparison should be case-sensitive
        """
        super().__init__(name="ROUGE_LCP", normalize=normalize, case_sensitive=case_sensitive)
        self.lcp_metric = LCP(normalize=normalize, case_sensitive=case_sensitive)
    
    def compute(self, prediction: str, reference: str) -> float:
        """
        Compute the ROUGE-LCP score between prediction and reference.
        
        Args:
            prediction (str): The model's prediction
            reference (str): The ground truth reference
            
        Returns:
            float: ROUGE-LCP score (LCP length / reference length)
        """
        ref_processed = self.preprocess_text(reference)
        
        # Handle empty reference
        if not ref_processed:
            return 0.0
        
        # Get LCP score
        lcp_score = self.lcp_metric.compute(prediction, reference)
        
        # Normalize by reference length
        rouge_lcp_score = lcp_score / len(ref_processed)
        
        return rouge_lcp_score
    
    def compute_batch(self, predictions: List[str], references: List[str]) -> MetricResults:
        """
        Compute ROUGE-LCP scores for a batch of predictions.
        
        Args:
            predictions (List[str]): List of model predictions
            references (List[str]): List of ground truth references
            
        Returns:
            MetricResults: Results with ROUGE-LCP scores and statistics
        """
        results = super().compute_batch(predictions, references)
        
        # Add ROUGE-LCP specific metadata
        scores = results.scores
        
        # Calculate component statistics
        lcp_scores = []
        ref_lengths = []
        
        for pred, ref in zip(predictions, references):
            lcp_score = self.lcp_metric.compute(pred, ref)
            ref_len = len(self.preprocess_text(ref))
            lcp_scores.append(lcp_score)
            ref_lengths.append(ref_len)
        
        results.add_metadata('lcp_scores', lcp_scores)
        results.add_metadata('reference_lengths', ref_lengths)
        results.add_metadata('mean_reference_length', sum(ref_lengths) / len(ref_lengths) if ref_lengths else 0)
        
        # Calculate exact match and extension statistics
        exact_matches = sum(1 for score in scores if score >= 1.0)
        extensions = sum(1 for score in scores if score > 1.0)
        
        results.add_metadata('exact_matches', exact_matches)
        results.add_metadata('exact_match_rate', exact_matches / len(scores) if scores else 0.0)
        results.add_metadata('extensions', extensions)
        results.add_metadata('extension_rate', extensions / len(scores) if scores else 0.0)
        
        return results
    
    def analyze_score_distribution(self, predictions: List[str], references: List[str]) -> dict:
        """
        Analyze the distribution of ROUGE-LCP scores across different ranges.
        
        Args:
            predictions (List[str]): List of model predictions
            references (List[str]): List of ground truth references
            
        Returns:
            dict: Analysis of score distribution in different ranges
        """
        scores = []
        for pred, ref in zip(predictions, references):
            score = self.compute(pred, ref)
            scores.append(score)
        
        # Define score ranges
        ranges = {
            'perfect_match': (1.0, 1.0),     # Exactly equal
            'high_quality': (0.8, 0.99),    # Very good prefix match
            'good_quality': (0.6, 0.79),    # Good prefix match  
            'medium_quality': (0.4, 0.59),  # Medium prefix match
            'low_quality': (0.2, 0.39),     # Low prefix match
            'poor_quality': (0.0, 0.19),    # Very poor prefix match
            'extensions': (1.01, float('inf'))  # Prediction longer than reference
        }
        
        distribution = {}
        total_samples = len(scores)
        
        for range_name, (min_val, max_val) in ranges.items():
            if range_name == 'perfect_match':
                count = sum(1 for s in scores if s == 1.0)
            elif range_name == 'extensions':
                count = sum(1 for s in scores if s > 1.0)
            else:
                count = sum(1 for s in scores if min_val <= s <= max_val)
            
            distribution[range_name] = {
                'count': count,
                'percentage': (count / total_samples * 100) if total_samples > 0 else 0.0
            }
        
        return {
            'score_distribution': distribution,
            'total_samples': total_samples,
            'mean_score': sum(scores) / len(scores) if scores else 0.0,
            'median_score': sorted(scores)[len(scores)//2] if scores else 0.0
        } 