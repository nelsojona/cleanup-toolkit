"""
Agentic Cleanup Toolkit - AI-powered code cleanup for development workflows.

This package provides utilities for automated code cleanup, including:
- Debug statement removal
- TODO/FIXME management
- Duplicate code detection
- Unused import cleanup
- Documentation improvement
"""

__version__ = "1.0.0"
__author__ = "Cleanup Toolkit Contributors"
__email__ = "contact@cleanup-toolkit.dev"

from cleanup_toolkit.core import CleanupEngine, CleanupConfig
from cleanup_toolkit.analyzers import CodeAnalyzer, PatternMatcher
from cleanup_toolkit.commands import CleanupCommand

__all__ = [
    "CleanupEngine",
    "CleanupConfig",
    "CodeAnalyzer",
    "PatternMatcher",
    "CleanupCommand",
    "__version__",
]