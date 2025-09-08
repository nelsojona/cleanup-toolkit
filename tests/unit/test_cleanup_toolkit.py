"""
Tests for the cleanup_toolkit Python package.
"""

import pytest
from pathlib import Path
import tempfile

# Import the package modules
from cleanup_toolkit import __version__, CleanupEngine, CleanupConfig, CodeAnalyzer, PatternMatcher, CleanupCommand
from cleanup_toolkit.core import CleanupConfig, CleanupEngine
from cleanup_toolkit.analyzers import CodeAnalyzer, PatternMatcher
from cleanup_toolkit.commands import CleanupCommand


class TestCleanupConfig:
    """Test the CleanupConfig class."""
    
    def test_config_initialization(self):
        """Test config initialization with defaults."""
        config = CleanupConfig()
        assert config.enabled is True
        assert config.auto_fix is False
        assert config.config_path == ".cleanup-toolkit/config.yml"
    
    def test_config_load(self):
        """Test loading configuration."""
        config = CleanupConfig()
        loaded = config.load()
        assert loaded["enabled"] is True
        assert loaded["auto_fix"] is False
        assert "exclude_patterns" in loaded
        assert "debug_patterns" in loaded
    
    def test_is_excluded(self):
        """Test file exclusion logic."""
        config = CleanupConfig()
        assert config.is_excluded("node_modules/test.js") is True
        assert config.is_excluded("vendor/package.py") is True
        assert config.is_excluded("src/main.py") is False
        assert config.is_excluded(".git/config") is True


class TestCleanupEngine:
    """Test the CleanupEngine class."""
    
    def test_engine_initialization(self):
        """Test engine initialization."""
        engine = CleanupEngine()
        assert engine.config is not None
        assert engine.stats["files_processed"] == 0
        assert engine.stats["issues_found"] == 0
    
    def test_analyze_file_with_debug(self, tmp_path):
        """Test analyzing a file with debug statements."""
        # Create a test Python file with debug statements
        test_file = tmp_path / "test.py"
        test_file.write_text("""
def main():
    print("Debug message")
    x = 10
    # TODO: Fix this later
    return x
""")
        
        engine = CleanupEngine()
        result = engine.analyze_file(str(test_file))
        
        assert result["file"] == str(test_file)
        assert len(result["issues"]) > 0
        assert engine.stats["files_processed"] == 1
    
    def test_analyze_excluded_file(self):
        """Test analyzing an excluded file."""
        engine = CleanupEngine()
        result = engine.analyze_file("node_modules/test.js")
        assert result["skipped"] is True
        assert result["reason"] == "excluded"
    
    def test_analyze_directory(self, tmp_path):
        """Test analyzing a directory."""
        # Create test files
        (tmp_path / "test1.py").write_text("print('test')")
        (tmp_path / "test2.py").write_text("# TODO: implement")
        
        engine = CleanupEngine()
        results = engine.analyze_directory(str(tmp_path))
        assert len(results) == 2
    
    def test_cleanup_file(self, tmp_path):
        """Test cleanup file method."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('debug')")
        
        engine = CleanupEngine()
        result = engine.cleanup_file(str(test_file), fix=False)
        assert "issues" in result
    
    def test_get_summary(self):
        """Test getting engine summary."""
        engine = CleanupEngine()
        summary = engine.get_summary()
        assert "files_processed" in summary
        assert "issues_found" in summary
        assert "debug_statements" in summary


class TestPatternMatcher:
    """Test the PatternMatcher class."""
    
    def test_pattern_matcher_initialization(self):
        """Test pattern matcher initialization."""
        matcher = PatternMatcher()
        assert "debug" in matcher.patterns
        assert "todo" in matcher.patterns
    
    def test_find_debug_patterns(self):
        """Test finding debug patterns."""
        matcher = PatternMatcher()
        content = """
import sys
print("Debug output")
console.log("Test")
"""
        matches = matcher.find_patterns(content, "debug", "python")
        assert len(matches) > 0
        assert any(m["type"] == "debug" for m in matches)
    
    def test_find_todo_patterns(self):
        """Test finding TODO patterns."""
        matcher = PatternMatcher()
        content = """
# TODO: Implement this function
// FIXME: This is broken
"""
        matches = matcher.find_patterns(content, "todo")
        assert len(matches) == 2
    
    def test_add_custom_pattern(self):
        """Test adding custom patterns."""
        matcher = PatternMatcher()
        matcher.add_custom_pattern("custom", r"CUSTOM:", "python")
        assert "custom" in matcher.patterns


class TestCodeAnalyzer:
    """Test the CodeAnalyzer class."""
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        analyzer = CodeAnalyzer()
        assert analyzer.pattern_matcher is not None
        assert ".py" in analyzer.supported_languages
    
    def test_analyze_python_file(self, tmp_path):
        """Test analyzing a Python file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
def hello():
    print("Hello")
    # TODO: Add more features
    return True
""")
        
        analyzer = CodeAnalyzer()
        result = analyzer.analyze(str(test_file))
        
        assert result["file"] == str(test_file)
        assert result["language"] == "python"
        assert "metrics" in result
        assert result["metrics"]["total_lines"] == 5
    
    def test_find_unused_imports(self, tmp_path):
        """Test finding unused imports."""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
import os
import sys
import json

def main():
    print(sys.version)
""")
        
        analyzer = CodeAnalyzer()
        unused = analyzer.find_unused_imports(str(test_file))
        assert "os" in unused
        assert "json" in unused
        assert "sys" not in unused


class TestCleanupCommand:
    """Test the CleanupCommand class."""
    
    def test_command_initialization(self):
        """Test command initialization."""
        command = CleanupCommand()
        assert command.config is not None
        assert command.engine is not None
        assert command.analyzer is not None
    
    def test_format_output(self):
        """Test formatting command output."""
        command = CleanupCommand()
        results = {
            "files_analyzed": 10,
            "issues_found": 5,
            "issues_fixed": 0,
            "summary": {
                "debug_statements": 3,
                "todos": 2,
            }
        }
        
        output = command.format_output(results)
        assert "Code Cleanup Analysis" in output
        assert "Files analyzed: 10" in output
        assert "Issues found: 5" in output


class TestPackageImports:
    """Test package-level imports."""
    
    def test_version(self):
        """Test package version."""
        assert __version__ == "1.0.0"
    
    def test_imports(self):
        """Test that all expected classes are importable."""
        assert CleanupEngine is not None
        assert CleanupConfig is not None
        assert CodeAnalyzer is not None
        assert PatternMatcher is not None
        assert CleanupCommand is not None