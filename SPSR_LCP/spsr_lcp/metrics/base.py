"""
Base classes and data structures for evaluation metrics.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
import numpy as np


@dataclass
class MetricResults:
    """
    Data class to store metric evaluation results.
    
    Attributes:
        scores (List[float]): Individual scores for each sample
        aggregate_score (float): Aggregated score (e.g., mean, median)
        metadata (Dict[str, Any]): Additional metadata about the evaluation
    """
    scores: List[float] = field(default_factory=list)
    aggregate_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculate aggregate score if not provided."""
        if self.scores and self.aggregate_score == 0.0:
            self.aggregate_score = float(np.mean(self.scores))
    
    def add_score(self, score: float):
        """Add a single score to the results."""
        self.scores.append(score)
        self.aggregate_score = float(np.mean(self.scores))
    
    def add_metadata(self, key: str, value: Any):
        """Add metadata to the results."""
        self.metadata[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to dictionary format."""
        return {
            'scores': self.scores,
            'aggregate_score': self.aggregate_score,
            'num_samples': len(self.scores),
            'std_dev': float(np.std(self.scores)) if self.scores else 0.0,
            'min_score': float(np.min(self.scores)) if self.scores else 0.0,
            'max_score': float(np.max(self.scores)) if self.scores else 0.0,
            'metadata': self.metadata
        }


class BaseMetric(ABC):
    """
    Abstract base class for all evaluation metrics.
    
    This class defines the interface that all metrics should implement.
    """
    
    def __init__(self, name: str):
        """
        Initialize the metric.
        
        Args:
            name (str): Name of the metric
        """
        self.name = name
    
    @abstractmethod
    def compute(self, prediction: str, reference: str) -> float:
        """
        Compute the metric score for a single prediction-reference pair.
        
        Args:
            prediction (str): The model's prediction
            reference (str): The ground truth reference
            
        Returns:
            float: The metric score
        """
        pass
    
    def compute_batch(self, predictions: List[str], references: List[str]) -> MetricResults:
        """
        Compute the metric scores for a batch of prediction-reference pairs.
        
        Args:
            predictions (List[str]): List of model predictions
            references (List[str]): List of ground truth references
            
        Returns:
            MetricResults: Results containing scores and metadata
        """
        if len(predictions) != len(references):
            raise ValueError(f"Number of predictions ({len(predictions)}) must match "
                           f"number of references ({len(references)})")
        
        scores = []
        for pred, ref in zip(predictions, references):
            try:
                score = self.compute(pred, ref)
                scores.append(score)
            except Exception as e:
                print(f"Warning: Error computing {self.name} for pair: {e}")
                scores.append(0.0)
        
        results = MetricResults(scores=scores)
        results.add_metadata('metric_name', self.name)
        results.add_metadata('num_valid_scores', len([s for s in scores if s is not None]))
        
        return results
    
    def __str__(self) -> str:
        """String representation of the metric."""
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        """Detailed string representation of the metric."""
        return self.__str__()


class StringMetric(BaseMetric):
    """
    Base class for string-based metrics (most code completion metrics).
    
    Provides common string preprocessing functionality.
    """
    
    def __init__(self, name: str, normalize: bool = True, case_sensitive: bool = True):
        """
        Initialize the string metric.
        
        Args:
            name (str): Name of the metric
            normalize (bool): Whether to normalize whitespace
            case_sensitive (bool): Whether comparison is case-sensitive
        """
        super().__init__(name)
        self.normalize = normalize
        self.case_sensitive = case_sensitive
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text according to metric settings.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Preprocessed text
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Remove carriage returns and leading newlines
        text = text.replace('\r', '').lstrip('\n')
        
        # Take only the first line for on-the-fly completion
        text = text.split('\n')[0]
        
        if self.normalize:
            text = text.strip()
        
        if not self.case_sensitive:
            text = text.lower()
        
        return text


class SequenceMetric(StringMetric):
    """
    Base class for sequence-based metrics that work with tokenized sequences.
    """
    
    def __init__(self, name: str, tokenizer=None, **kwargs):
        """
        Initialize the sequence metric.
        
        Args:
            name (str): Name of the metric
            tokenizer: Optional tokenizer for sequence processing
            **kwargs: Additional arguments for StringMetric
        """
        super().__init__(name, **kwargs)
        self.tokenizer = tokenizer or self._default_tokenizer
    
    def _default_tokenizer(self, text: str) -> List[str]:
        """Default character-level tokenizer."""
        return list(text)
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into sequence elements.
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: Tokenized sequence
        """
        processed_text = self.preprocess_text(text)
        return self.tokenizer(processed_text) 