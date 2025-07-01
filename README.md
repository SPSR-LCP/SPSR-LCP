# SPSR-LCP: Structure-Aware Corpus Construction and User-Perception-Aligned Metrics for LLM Code Completion

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the implementation of **SPSR-LCP** (Structure-Preserving and Semantically-Reordered Code Graph with Longest Common Prefix), a novel approach for repository-level code completion that addresses two key challenges:

1. **User-Perception-Aligned Evaluation**: We propose LCP and ROUGE-LCP metrics that better correlate with user adoption behavior in real-world code completion scenarios.

2. **Structure-Aware Corpus Construction**: We introduce SPSR-Graph, a method for constructing training corpora that preserves code structure and models cross-file dependencies.

## 📖 Paper

**Structure-Aware Corpus Construction and User-Perception-Aligned Metrics for Large-Language-Model Code Completion**

*Anonymous Authors - Under Review*

**Abstract**: Code completion technology based on large language model has significantly improved the development efficiency of programmers. However, in practical applications, there remains a gap between current commonly used code completion evaluation metrics and users' actual perception. To address this issue, we propose two evaluation metrics for code completion tasks—LCP and ROUGE-LCP, from the perspective of probabilistic modeling. Furthermore, to tackle the lack of effective structural semantic modeling and cross-module dependency information in LLMs for repository-level code completion scenarios, we propose a data processing method based on a Structure-Preserving and Semantically-Reordered Code Graph (SPSR-Graph).

## 🚀 Key Features

### Evaluation Metrics
- **LCP (Longest Common Prefix)**: Measures continuous prefix matching between model output and reference
- **ROUGE-LCP**: Normalized LCP metric for fair comparison across different sequence lengths
- **High User Correlation**: Metrics show >0.7 correlation with user adoption rates in production environments

### SPSR-Graph Construction
- **AST-based Semantic Segmentation**: Structure-aware code segmentation preserving semantic boundaries
- **Cross-file Dependency Modeling**: Graph-based representation of function calls and type dependencies
- **Repository-level Context**: Enhanced training corpus with global semantic consistency

## 📁 Repository Structure

```
SPSR_LCP/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── setup.py                          # Package installation
├── spsr_lcp/                         # Main package
│   ├── __init__.py                   # Package initialization
│   ├── metrics/                      # Evaluation metrics
│   │   ├── __init__.py
│   │   ├── lcp.py                    # LCP metric implementation
│   │   ├── rouge_lcp.py              # ROUGE-LCP metric implementation
│   │   └── base.py                   # Base metric classes
│   ├── preprocessing/                # Data preprocessing
│   │   ├── __init__.py
│   │   ├── filter.py                 # Data filtering
│   │   ├── cleaner.py                # Data cleaning
│   │   └── deduplicator.py           # Data deduplication
│   ├── ast_processing/               # AST-based processing
│   │   ├── __init__.py
│   │   ├── semantic_segmentation.py  # AST semantic segmentation
│   │   ├── parser.py                 # Code parsing utilities
│   │   └── validator.py              # Structure validation
│   ├── graph/                        # SPSR-Graph construction
│   │   ├── __init__.py
│   │   ├── builder.py                # Graph builder
│   │   ├── traversal.py              # Graph traversal algorithms
│   │   ├── chain_generator.py        # Call chain generation
│   │   └── types.py                  # Graph data structures
│   └── utils/                        # Utility functions
│       ├── __init__.py
│       ├── file_io.py                # File I/O operations
│       ├── logger.py                 # Logging utilities
│       └── constants.py              # Constants and configurations
├── examples/                         # Example usage and demos
│   ├── basic_usage.py                # Basic usage examples
│   └── evaluation_demo.py            # Evaluation metrics demo
├── tests/                           # Unit tests
│   └── test_metrics.py              # Test evaluation metrics
└── data/                            # Sample data
    └── sample_code/                 # Sample source code
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Install from Source

```bash
# Clone the repository
git clone https://github.com/SPSR-LCP/SPSR-LCP.git
cd SPSR-LCP

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Dependencies

Key dependencies include:
- `tree-sitter`: For AST parsing
- `tree-sitter-languages`: Language parsers
- `networkx`: Graph construction and algorithms
- `numpy`: Numerical computations
- `pandas`: Data manipulation
- `nltk`: Natural language processing (for BLEU/ROUGE)

## 📚 Quick Start

### 1. Evaluation Metrics

```python
from spsr_lcp.metrics import LCP, ROUGE_LCP

# Initialize metrics
lcp_metric = LCP()
rouge_lcp_metric = ROUGE_LCP()

# Evaluate predictions
prediction = "def add(a, b):\n    return a + b"
reference = "def add(a, b):\n    return a + b + c"

lcp_score = lcp_metric.compute(prediction, reference)
rouge_lcp_score = rouge_lcp_metric.compute(prediction, reference)

print(f"LCP Score: {lcp_score}")
print(f"ROUGE-LCP Score: {rouge_lcp_score}")
```

### 2. SPSR-Graph Construction

```python
from spsr_lcp.graph import SPSRGraphBuilder
from spsr_lcp.preprocessing import CodePreprocessor

# Initialize components
preprocessor = CodePreprocessor()
graph_builder = SPSRGraphBuilder()

# Process repository
repo_path = "/path/to/your/repository"
processed_files = preprocessor.process_repository(repo_path)
spsr_graph = graph_builder.build_graph(processed_files)

# Generate training samples
training_samples = graph_builder.generate_training_samples(spsr_graph, max_depth=3)
```

### 3. End-to-End Pipeline

```python
from spsr_lcp import SPSRLCPPipeline

# Initialize pipeline
pipeline = SPSRLCPPipeline()

# Process repository and generate training corpus
training_corpus = pipeline.process_repository(
    repo_path="/path/to/repository",
    output_path="/path/to/output",
    config={
        "max_depth": 3,
        "max_children": 5,
        "include_structs": True
    }
)

# Evaluate model outputs
results = pipeline.evaluate(
    predictions_file="/path/to/predictions.json",
    references_file="/path/to/references.json"
)
```


## 📖 Examples

See the `examples/` directory for comprehensive examples:

- [`basic_usage.py`](examples/basic_usage.py): Basic usage of LCP and ROUGE-LCP metrics
- [`evaluation_demo.py`](examples/evaluation_demo.py): Demonstration of user correlation analysis

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_metrics.py
python -m pytest tests/test_graph.py

# Run with coverage
python -m pytest tests/ --cov=spsr_lcp --cov-report=html
```

## 📄 Documentation

For detailed API reference and methodology, see the comprehensive examples and inline documentation in the source code.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- The open-source community for providing essential tools and libraries
- All contributors and users of this repository

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@article{anonymous2025spsr,
  title={Structure-Aware Corpus Construction and User-Perception-Aligned Metrics for Large-Language-Model Code Completion},
  author={Anonymous Authors},
  year={2025},
  note={Under Review}
}
``` 
