#!/usr/bin/env python3
"""
Evaluation metrics demonstration for SPSR-LCP.

This example shows how the LCP and ROUGE-LCP metrics correlate better with
user perception compared to traditional metrics like EM and BLEU.
"""

import sys
import os

# Add the package to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from spsr_lcp.metrics import LCP, ROUGE_LCP, evaluate_batch


def demo_user_correlation():
    """Demonstrate how LCP correlates with user adoption behavior."""
    
    print("=== User Correlation Demo ===")
    print("Showing how LCP/ROUGE-LCP better predict user adoption\n")
    
    # Sample scenarios based on real user behavior patterns
    test_cases = [
        {
            'prediction': 'def function_name(',
            'reference': 'def function_name(param):',
            'user_adopts': True,  # Good prefix, user likely to adopt
            'description': 'Good prefix match'
        },
        {
            'prediction': 'for j in range(10):',
            'reference': 'for i in range(10):',
            'user_adopts': False,  # Variable name mismatch, unlikely adoption
            'description': 'Variable name mismatch'
        },
        {
            'prediction': 'if condition:',
            'reference': 'if condition:',
            'user_adopts': True,  # Perfect match
            'description': 'Perfect match'
        },
        {
            'prediction': 'import numpy',
            'reference': 'import pandas as pd',
            'user_adopts': False,  # Different library
            'description': 'Different import'
        }
    ]
    
    lcp_metric = LCP()
    rouge_lcp_metric = ROUGE_LCP()
    
    print(f"{'Description':<20} {'LCP':<5} {'R-LCP':<7} {'User':<6} {'LCP>3':<6} {'Match'}")
    print("-" * 60)
    
    correct_predictions = 0
    
    for case in test_cases:
        lcp_score = lcp_metric.compute(case['prediction'], case['reference'])
        rouge_lcp_score = rouge_lcp_metric.compute(case['prediction'], case['reference'])
        
        # Simple heuristic: LCP > 3 suggests user adoption
        lcp_predicts = lcp_score > 3
        matches = lcp_predicts == case['user_adopts']
        
        if matches:
            correct_predictions += 1
        
        print(f"{case['description']:<20} {lcp_score:<5} {rouge_lcp_score:<7.2f} "
              f"{'Yes' if case['user_adopts'] else 'No':<6} "
              f"{'Yes' if lcp_predicts else 'No':<6} "
              f"{'✓' if matches else '✗'}")
    
    accuracy = correct_predictions / len(test_cases) * 100
    print(f"\nLCP prediction accuracy: {accuracy:.1f}%")


def demo_length_analysis():
    """Demonstrate ROUGE-LCP for different sequence lengths."""
    
    print("\n=== Length Analysis Demo ===")
    print("Comparing LCP and ROUGE-LCP across different sequence lengths\n")
    
    base_ref = "def calculate_fibonacci_number(n):"
    
    test_cases = [
        ("def", "Short prefix"),
        ("def calc", "Medium prefix"),  
        ("def calculate_fib", "Long prefix"),
        ("def calculate_fibonacci_number", "Almost complete"),
        ("def calculate_fibonacci_number(n):", "Perfect match"),
        ("def calculate_fibonacci_number(n): return", "Extension")
    ]
    
    lcp_metric = LCP()
    rouge_lcp_metric = ROUGE_LCP()
    
    print(f"{'Prediction':<35} {'LCP':<5} {'ROUGE-LCP':<10} {'Description'}")
    print("-" * 70)
    
    for pred, desc in test_cases:
        lcp_score = lcp_metric.compute(pred, base_ref)
        rouge_lcp_score = rouge_lcp_metric.compute(pred, base_ref)
        
        print(f"'{pred}'{'.' * (33 - len(pred))} {lcp_score:<5} {rouge_lcp_score:<10.3f} {desc}")


if __name__ == "__main__":
    print("SPSR-LCP Evaluation Demo")
    print("=" * 30)
    
    try:
        demo_user_correlation()
        demo_length_analysis()
        
        print("\n=== Demo completed! ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc() 