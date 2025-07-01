"""
Constants and default configurations for the SPSR-LCP package.
"""

# Supported programming languages for AST parsing
SUPPORTED_LANGUAGES = {
    'c': {
        'extensions': ['.c', '.h'],
        'tree_sitter_language': 'c',
        'comment_styles': ['//','/**/']
    },
    'cpp': {
        'extensions': ['.cpp', '.cxx', '.cc', '.hpp', '.hxx', '.hh'],
        'tree_sitter_language': 'cpp',
        'comment_styles': ['//','/**/']
    },
    'python': {
        'extensions': ['.py'],
        'tree_sitter_language': 'python',
        'comment_styles': ['#']
    },
    'java': {
        'extensions': ['.java'],
        'tree_sitter_language': 'java',
        'comment_styles': ['//','/**/']
    },
    'javascript': {
        'extensions': ['.js', '.jsx'],
        'tree_sitter_language': 'javascript',
        'comment_styles': ['//','/**/']
    },
    'typescript': {
        'extensions': ['.ts', '.tsx'],
        'tree_sitter_language': 'typescript',
        'comment_styles': ['//','/**/']
    }
}

# Default configuration for the pipeline
DEFAULT_CONFIG = {
    'preprocessing': {
        'min_line_length': 5,
        'max_line_length': 200,
        'min_file_size': 100,
        'max_file_size': 50000,
        'char_validity_ratio': 0.8,
        'exclude_patterns': [
            '*.pyc', '*.so', '*.dll', '*.exe',
            '.git/*', '__pycache__/*', 'node_modules/*'
        ]
    },
    'ast_processing': {
        'max_depth': 50,
        'granularity_theta_min': 10,
        'granularity_theta_max': 100,
        'check_completeness': True,
        'preserve_structure': True
    },
    'graph': {
        'max_depth': 3,
        'max_children': 5,
        'include_structs': True,
        'include_functions': True,
        'edge_types': [
            'direct_call',
            'member_reference', 
            'type_usage',
            'include_dependency'
        ]
    },
    'evaluation': {
        'metrics': ['lcp', 'rouge_lcp', 'em', 'bleu'],
        'normalize_whitespace': True,
        'case_sensitive': True
    }
}

# AST node types for different semantic units
AST_NODE_TYPES = {
    'function_nodes': [
        'function_definition',
        'function_declarator',
        'method_definition'
    ],
    'struct_nodes': [
        'struct_specifier',
        'union_specifier',
        'class_definition',
        'class_specifier'
    ],
    'control_flow_nodes': [
        'if_statement',
        'while_statement',
        'for_statement',
        'switch_statement',
        'compound_statement'
    ],
    'expression_nodes': [
        'call_expression',
        'assignment_expression',
        'binary_expression',
        'unary_expression'
    ],
    'declaration_nodes': [
        'declaration',
        'variable_declaration',
        'parameter_declaration'
    ]
}

# Metric score ranges for evaluation
METRIC_RANGES = {
    'lcp': {
        'perfect': (1.0, 1.0),
        'excellent': (0.9, 0.99),
        'good': (0.7, 0.89),
        'fair': (0.5, 0.69),
        'poor': (0.0, 0.49)
    },
    'rouge_lcp': {
        'perfect': (1.0, 1.0),
        'excellent': (0.8, 0.99),
        'good': (0.6, 0.79),
        'fair': (0.4, 0.59),
        'poor': (0.0, 0.39)
    },
    'bleu': {
        'excellent': (80, 100),
        'good': (60, 79),
        'fair': (40, 59),
        'poor': (0, 39)
    }
}

# File patterns for filtering
EXCLUDE_PATTERNS = [
    # Version control
    '.git/*', '.svn/*', '.hg/*',
    # Build artifacts
    'build/*', 'dist/*', '*.pyc', '*.pyo', '*.so', '*.dll', '*.exe',
    # Dependencies
    'node_modules/*', '__pycache__/*', '.venv/*', 'venv/*',
    # IDE files
    '.vscode/*', '.idea/*', '*.swp', '*.swo',
    # Temporary files
    '*.tmp', '*.temp', '*~'
]

# Maximum values for processing
MAX_PROCESSING_LIMITS = {
    'max_file_size_bytes': 1024 * 1024,  # 1MB
    'max_ast_depth': 100,
    'max_graph_nodes': 10000,
    'max_path_length': 10,
    'max_children_per_node': 20
}

# Error messages
ERROR_MESSAGES = {
    'file_not_found': "File not found: {filepath}",
    'invalid_language': "Unsupported language: {language}",
    'ast_parse_error': "Failed to parse AST for file: {filepath}",
    'graph_build_error': "Failed to build graph: {error}",
    'metric_compute_error': "Failed to compute metric {metric}: {error}"
} 