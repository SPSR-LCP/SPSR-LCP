"""
Evaluation utilities for batch processing and comprehensive metric computation.

This module provides high-level functions for evaluating code completion models
using multiple metrics including LCP, ROUGE-LCP, and traditional metrics.
"""

import json
import os
from typing import Dict, List, Optional, Union, Any
from .lcp import LCP
from .rouge_lcp import ROUGE_LCP
from .base import MetricResults


def exact_match_score(prediction: str, reference: str) -> float:
    """
    Calculate exact match score between prediction and reference.
    
    Args:
        prediction (str): Model prediction
        reference (str): Ground truth reference
        
    Returns:
        float: 1.0 if exact match, 0.0 otherwise
    """
    # Preprocess strings similar to LCP preprocessing
    pred = str(prediction).replace('\r', '').lstrip('\n').split('\n')[0].strip()
    ref = str(reference).replace('\r', '').lstrip('\n').split('\n')[0].strip()
    
    return 1.0 if pred == ref else 0.0


def calculate_bleu_score(prediction: str, reference: str) -> float:
    """
    Calculate BLEU score using NLTK.
    
    Args:
        prediction (str): Model prediction
        reference (str): Ground truth reference
        
    Returns:
        float: BLEU score (0-100)
    """
    try:
        from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
        
        if not prediction or not reference:
            return 0.0
        
        # Preprocess strings
        pred = str(prediction).replace('\r', '').lstrip('\n').split('\n')[0].strip()
        ref = str(reference).replace('\r', '').lstrip('\n').split('\n')[0].strip()
        
        if not pred or not ref:
            return 0.0
        
        # Tokenize at character level for code
        reference_tokens = [list(ref)]
        candidate_tokens = list(pred)
        
        # Use smoothing to handle edge cases
        smoothing = SmoothingFunction().method1
        score = sentence_bleu(reference_tokens, candidate_tokens, smoothing_function=smoothing)
        
        return score * 100  # Convert to percentage
        
    except ImportError:
        print("Warning: NLTK not available for BLEU computation")
        return 0.0
    except Exception as e:
        print(f"Warning: Error computing BLEU score: {e}")
        return 0.0


def calculate_rouge_l_score(prediction: str, reference: str) -> float:
    """
    Calculate ROUGE-L score.
    
    Args:
        prediction (str): Model prediction
        reference (str): Ground truth reference
        
    Returns:
        float: ROUGE-L F1 score (0-100)
    """
    try:
        # Preprocess strings
        pred = str(prediction).replace('\r', '').lstrip('\n').split('\n')[0].strip()
        ref = str(reference).replace('\r', '').lstrip('\n').split('\n')[0].strip()
        
        if not pred or not ref:
            return 0.0
        
        # Calculate LCS (Longest Common Subsequence)
        def lcs_length(s1, s2):
            m, n = len(s1), len(s2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if s1[i-1] == s2[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            
            return dp[m][n]
        
        lcs_len = lcs_length(pred, ref)
        
        if lcs_len == 0:
            return 0.0
        
        # Calculate precision, recall, and F1
        precision = lcs_len / len(pred) if len(pred) > 0 else 0.0
        recall = lcs_len / len(ref) if len(ref) > 0 else 0.0
        
        if precision + recall == 0:
            return 0.0
        
        f1 = 2 * (precision * recall) / (precision + recall)
        return f1 * 100  # Convert to percentage
        
    except Exception as e:
        print(f"Warning: Error computing ROUGE-L score: {e}")
        return 0.0


def evaluate_single(prediction: str, 
                   reference: str, 
                   metrics: Optional[List[str]] = None) -> Dict[str, float]:
    """
    Evaluate a single prediction-reference pair using multiple metrics.
    
    Args:
        prediction (str): Model prediction
        reference (str): Ground truth reference
        metrics (List[str], optional): List of metrics to compute.
                                     Defaults to ['lcp', 'rouge_lcp', 'em', 'bleu', 'rouge_l']
    
    Returns:
        Dict[str, float]: Dictionary mapping metric names to scores
    """
    if metrics is None:
        metrics = ['lcp', 'rouge_lcp', 'em', 'bleu', 'rouge_l']
    
    results = {}
    
    # Initialize metric objects
    if 'lcp' in metrics:
        lcp_metric = LCP()
        results['lcp'] = lcp_metric.compute(prediction, reference)
    
    if 'rouge_lcp' in metrics:
        rouge_lcp_metric = ROUGE_LCP()
        results['rouge_lcp'] = rouge_lcp_metric.compute(prediction, reference)
    
    if 'em' in metrics:
        results['em'] = exact_match_score(prediction, reference)
    
    if 'bleu' in metrics:
        results['bleu'] = calculate_bleu_score(prediction, reference)
    
    if 'rouge_l' in metrics:
        results['rouge_l'] = calculate_rouge_l_score(prediction, reference)
    
    return results


def evaluate_batch(predictions: List[str], 
                  references: List[str], 
                  metrics: Optional[List[str]] = None) -> Dict[str, Dict]:
    """
    Evaluate a batch of predictions using multiple metrics.
    
    Args:
        predictions (List[str]): List of model predictions
        references (List[str]): List of ground truth references
        metrics (List[str], optional): List of metrics to compute
    
    Returns:
        Dict[str, Dict]: Results for each metric with scores and statistics
    """
    if len(predictions) != len(references):
        raise ValueError(f"Number of predictions ({len(predictions)}) must match "
                        f"number of references ({len(references)})")
    
    if metrics is None:
        metrics = ['lcp', 'rouge_lcp', 'em', 'bleu', 'rouge_l']
    
    all_results = {}
    
    # Compute each metric
    for metric_name in metrics:
        scores = []
        
        for pred, ref in zip(predictions, references):
            single_result = evaluate_single(pred, ref, [metric_name])
            scores.append(single_result[metric_name])
        
        # Create MetricResults object
        metric_results = MetricResults(scores=scores)
        metric_results.add_metadata('metric_name', metric_name)
        
        all_results[metric_name] = metric_results.to_dict()
    
    return all_results


def load_evaluation_data(predictions_file: str, 
                        references_file: str) -> tuple[List[str], List[str]]:
    """
    Load predictions and references from JSON files.
    
    Args:
        predictions_file (str): Path to JSON file containing predictions
        references_file (str): Path to JSON file containing references
    
    Returns:
        tuple: (predictions, references) lists
    """
    # Load predictions
    with open(predictions_file, 'r', encoding='utf-8') as f:
        pred_data = json.load(f)
    
    # Load references  
    with open(references_file, 'r', encoding='utf-8') as f:
        ref_data = json.load(f)
    
    # Extract predictions and references based on data format
    if isinstance(pred_data, list):
        predictions = [item.get('prediction', '') if isinstance(item, dict) else str(item) 
                      for item in pred_data]
    else:
        predictions = list(pred_data.values()) if isinstance(pred_data, dict) else [str(pred_data)]
    
    if isinstance(ref_data, list):
        references = [item.get('reference', '') if isinstance(item, dict) else str(item) 
                     for item in ref_data]
    else:
        references = list(ref_data.values()) if isinstance(ref_data, dict) else [str(ref_data)]
    
    return predictions, references


def calculate_all_metrics(predictions_file: Optional[str] = None,
                         references_file: Optional[str] = None,
                         predictions: Optional[List[str]] = None,
                         references: Optional[List[str]] = None,
                         metrics: Optional[List[str]] = None,
                         output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Calculate all metrics for a dataset.
    
    Args:
        predictions_file (str, optional): Path to predictions JSON file
        references_file (str, optional): Path to references JSON file  
        predictions (List[str], optional): List of predictions
        references (List[str], optional): List of references
        metrics (List[str], optional): List of metrics to compute
        output_file (str, optional): Path to save results
    
    Returns:
        Dict[str, Any]: Complete evaluation results
    """
    # Load data
    if predictions_file and references_file:
        predictions, references = load_evaluation_data(predictions_file, references_file)
    elif predictions is not None and references is not None:
        pass  # Use provided lists
    else:
        raise ValueError("Must provide either file paths or prediction/reference lists")
    
    # Evaluate
    results = evaluate_batch(predictions, references, metrics)
    
    # Add summary statistics
    summary = {
        'total_samples': len(predictions),
        'metrics_computed': list(results.keys()),
        'summary_scores': {
            metric: results[metric]['aggregate_score'] 
            for metric in results
        }
    }
    
    final_results = {
        'summary': summary,
        'detailed_results': results
    }
    
    # Save if output file specified
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    return final_results 