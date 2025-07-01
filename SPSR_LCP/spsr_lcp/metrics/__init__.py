"""
Evaluation metrics for code completion tasks.

This module provides user-perception-aligned metrics including:
- LCP (Longest Common Prefix): Measures continuous prefix matching
- ROUGE-LCP: Normalized LCP metric for fair comparison across sequence lengths
- Integration with traditional metrics (EM, BLEU, ROUGE-L)
"""

from .lcp import LCP
from .rouge_lcp import ROUGE_LCP
from .base import BaseMetric, MetricResults
from .evaluator import evaluate_batch, evaluate_single, calculate_all_metrics

__all__ = [
    'LCP',
    'ROUGE_LCP', 
    'BaseMetric',
    'MetricResults',
    'evaluate_batch',
    'evaluate_single',
    'calculate_all_metrics'
] 