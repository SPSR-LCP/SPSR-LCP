#!/usr/bin/env python3
"""
Test cases for SPSR-LCP metrics.

Run with: python -m pytest tests/test_metrics.py
"""

import unittest
import sys
import os

# Add the package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from spsr_lcp.metrics import LCP, ROUGE_LCP


class TestLCPMetric(unittest.TestCase):
    """Test cases for LCP metric."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lcp_metric = LCP()
    
    def test_perfect_match(self):
        """Test LCP with perfect match."""
        prediction = "def function(param):"
        reference = "def function(param):"
        
        score = self.lcp_metric.compute(prediction, reference)
        self.assertEqual(score, len(reference))
    
    def test_prefix_match(self):
        """Test LCP with partial prefix match."""
        prediction = "def function("
        reference = "def function(param):"
        
        score = self.lcp_metric.compute(prediction, reference)
        self.assertEqual(score, len(prediction))
    
    def test_no_match(self):
        """Test LCP with no match."""
        prediction = "import pandas"
        reference = "def function():"
        
        score = self.lcp_metric.compute(prediction, reference)
        self.assertEqual(score, 0)
    
    def test_empty_prediction(self):
        """Test LCP with empty prediction."""
        prediction = ""
        reference = "def function():"
        
        score = self.lcp_metric.compute(prediction, reference)
        self.assertEqual(score, 0)
    
    def test_empty_reference(self):
        """Test LCP with empty reference."""
        prediction = "def function():"
        reference = ""
        
        score = self.lcp_metric.compute(prediction, reference)
        self.assertEqual(score, 0)


class TestROUGELCPMetric(unittest.TestCase):
    """Test cases for ROUGE-LCP metric."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rouge_lcp_metric = ROUGE_LCP()
    
    def test_perfect_match(self):
        """Test ROUGE-LCP with perfect match."""
        prediction = "def function(param):"
        reference = "def function(param):"
        
        score = self.rouge_lcp_metric.compute(prediction, reference)
        self.assertEqual(score, 1.0)
    
    def test_half_match(self):
        """Test ROUGE-LCP with half match."""
        prediction = "def func"
        reference = "def function"  # 8 chars total, 8 chars match
        
        score = self.rouge_lcp_metric.compute(prediction, reference)
        self.assertAlmostEqual(score, 8/12, places=3)  # 8 matching chars out of 12 total
    
    def test_extension(self):
        """Test ROUGE-LCP when prediction is longer than reference."""
        prediction = "def function(param, extra):"
        reference = "def function(param):"
        
        score = self.rouge_lcp_metric.compute(prediction, reference)
        # Should be LCP / reference_length
        expected_lcp = len("def function(param")  # 18 chars match
        expected_score = expected_lcp / len(reference)
        self.assertAlmostEqual(score, expected_score, places=3)
    
    def test_no_match(self):
        """Test ROUGE-LCP with no match."""
        prediction = "import pandas"
        reference = "def function():"
        
        score = self.rouge_lcp_metric.compute(prediction, reference)
        self.assertEqual(score, 0.0)
    
    def test_empty_reference(self):
        """Test ROUGE-LCP with empty reference."""
        prediction = "def function():"
        reference = ""
        
        score = self.rouge_lcp_metric.compute(prediction, reference)
        self.assertEqual(score, 0.0)


class TestMetricComparison(unittest.TestCase):
    """Test cases comparing different scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lcp_metric = LCP()
        self.rouge_lcp_metric = ROUGE_LCP()
    
    def test_user_adoption_scenarios(self):
        """Test scenarios based on expected user adoption behavior."""
        
        # Scenario 1: Good prefix, likely adoption
        pred1 = "if condition"
        ref1 = "if condition and other:"
        lcp1 = self.lcp_metric.compute(pred1, ref1)
        rouge_lcp1 = self.rouge_lcp_metric.compute(pred1, ref1)
        
        # Scenario 2: Poor prefix, unlikely adoption  
        pred2 = "for j in"
        ref2 = "for i in range(10):"
        lcp2 = self.lcp_metric.compute(pred2, ref2)
        rouge_lcp2 = self.rouge_lcp_metric.compute(pred2, ref2)
        
        # Good prefix should have higher LCP
        self.assertGreater(lcp1, lcp2)
        
        # ROUGE-LCP should also differentiate
        self.assertGreater(rouge_lcp1, rouge_lcp2)
    
    def test_length_normalization(self):
        """Test that ROUGE-LCP properly normalizes for length."""
        
        # Same prefix length, different reference lengths
        pred = "def func"
        ref_short = "def function"
        ref_long = "def function_with_very_long_name"
        
        rouge_lcp_short = self.rouge_lcp_metric.compute(pred, ref_short)
        rouge_lcp_long = self.rouge_lcp_metric.compute(pred, ref_long)
        
        # ROUGE-LCP should be higher for shorter reference (better proportion)
        self.assertGreater(rouge_lcp_short, rouge_lcp_long)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2) 