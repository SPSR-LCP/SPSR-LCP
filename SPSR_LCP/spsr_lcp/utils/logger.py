"""Logging utilities."""

import logging

def setup_logging(level=logging.INFO):
    """Setup basic logging."""
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def get_logger(name):
    """Get a logger instance."""
    return logging.getLogger(name)
