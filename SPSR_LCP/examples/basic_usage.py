#!/usr/bin/env python3
"""
Basic usage example for SPSR-LCP.

This example demonstrates:
1. Computing LCP and ROUGE-LCP metrics
2. Basic preprocessing operations  
3. Simple evaluation workflow
"""

import sys
import os

# Add the package to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from spsr_lcp.metrics import LCP, ROUGE_LCP, evaluate_single, evaluate_batch


def demo_basic_metrics():
    """Demonstrate basic LCP and ROUGE-LCP metric computation."""
    print("=== Basic Metrics Demo ===")
    
    # Initialize metrics
    lcp_metric = LCP()
    rouge_lcp_metric = ROUGE_LCP()
    
    # Example predictions and references
    examples = [
        {
            'prediction': 'def add(a, b):\n    return a + b',
            'reference': 'def add(a, b):\n    return a + b + c',
            'description': 'Function definition with missing variable'
        },
        {
            'prediction': 'if (condition) {',
            'reference': 'if (condition) {',
            'description': 'Perfect match case'
        },
        {
            'prediction': 'for i in range(',
            'reference': 'for j in range(10):',
            'description': 'Variable name mismatch'
        },
        {
            'prediction': 'import numpy as np',
            'reference': 'import pandas as pd',
            'description': 'Different import statement'
        }
    ]
    
    print(f"{'Description':<30} {'LCP':<5} {'ROUGE-LCP':<10} {'Prediction':<20} {'Reference'}")
    print("-" * 90)
    
    for example in examples:
        pred = example['prediction']
        ref = example['reference']
        desc = example['description']
        
        lcp_score = lcp_metric.compute(pred, ref)
        rouge_lcp_score = rouge_lcp_metric.compute(pred, ref)
        
        print(f"{desc:<30} {lcp_score:<5} {rouge_lcp_score:<10.3f} {pred[:20]:<20} {ref[:20]}")


def demo_batch_evaluation():
    """Demonstrate batch evaluation with multiple metrics."""
    print("\n=== Batch Evaluation Demo ===")
    
    # Sample data
    predictions = [
        "def function_name():",
        "if condition:",
        "for i in range(10):",
        "import os",
        "class MyClass:",
        "try:",
        "with open('file.txt') as f:",
        "return result"
    ]
    
    references = [
        "def function_name(param):",
        "if condition and other:",
        "for i in range(10):",
        "import os, sys",
        "class MyClass(BaseClass):",
        "try:",
        "with open('file.txt', 'r') as f:",
        "return result + 1"
    ]
    
    # Evaluate using all available metrics
    results = evaluate_batch(
        predictions=predictions,
        references=references,
        metrics=['lcp', 'rouge_lcp', 'em', 'bleu']
    )
    
    print("Evaluation Results:")
    print("-" * 50)
    
    for metric_name, metric_results in results.items():
        avg_score = metric_results['aggregate_score']
        num_samples = metric_results['num_samples']
        print(f"{metric_name.upper():<12}: {avg_score:.3f} (avg over {num_samples} samples)")
    
    # Show detailed LCP results
    lcp_results = results.get('lcp', {})
    if 'scores' in lcp_results:
        print(f"\nDetailed LCP scores: {lcp_results['scores']}")


def demo_single_evaluation():
    """Demonstrate single prediction evaluation."""
    print("\n=== Single Evaluation Demo ===")
    
    prediction = "def calculate_sum(a, b):\n    return a + b"
    reference = "def calculate_sum(a, b):\n    return a + b + c"
    
    # Evaluate with all metrics
    results = evaluate_single(prediction, reference)
    
    print(f"Prediction: {prediction[:50]}...")
    print(f"Reference:  {reference[:50]}...")
    print("\nMetric Scores:")
    print("-" * 30)
    
    for metric, score in results.items():
        print(f"{metric.upper():<12}: {score}")


def demo_metric_analysis():
    """Demonstrate metric-specific analysis features."""
    print("\n=== Metric Analysis Demo ===")
    
    # Create some test data with varying lengths
    test_data = [
        ("a", "abc"),           # Short sequences
        ("hello", "hello"),     # Perfect match
        ("function(", "function(param)"),  # Partial match
        ("if x > 0:", "if y > 0:"),       # Similar structure, different variable
        ("", "something"),       # Empty prediction
        ("longer_prediction", "short")     # Prediction longer than reference
    ]
    
    rouge_lcp_metric = ROUGE_LCP()
    
    print("Length Analysis:")
    print(f"{'Prediction':<15} {'Reference':<15} {'LCP':<5} {'ROUGE-LCP':<10} {'Notes'}")
    print("-" * 70)
    
    for pred, ref in test_data:
        try:
            lcp_score = LCP().compute(pred, ref)
            rouge_lcp_score = rouge_lcp_metric.compute(pred, ref)
            
            # Determine notes
            notes = []
            if pred == ref:
                notes.append("Perfect match")
            elif rouge_lcp_score >= 1.0:
                notes.append("Extension")
            elif rouge_lcp_score == 0.0:
                notes.append("No prefix match")
            
            notes_str = ", ".join(notes) if notes else ""
            
            print(f"'{pred}'{'.'*(15-len(pred)-2)} '{ref}'{'.'*(15-len(ref)-2)} {lcp_score:<5} {rouge_lcp_score:<10.3f} {notes_str}")
            
        except Exception as e:
            print(f"'{pred}'{'.'*(15-len(pred)-2)} '{ref}'{'.'*(15-len(ref)-2)} Error: {e}")


if __name__ == "__main__":
    print("SPSR-LCP Basic Usage Examples")
    print("=" * 50)
    
    try:
        demo_basic_metrics()
        demo_batch_evaluation()
        demo_single_evaluation()
        demo_metric_analysis()
        
        print("\n=== Demo completed successfully! ===")
        
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback
        traceback.print_exc() 