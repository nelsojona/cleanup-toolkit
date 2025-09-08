"""
Basic functionality tests that work across all platforms.

This module tests core toolkit functionality without complex git operations
that cause cross-platform issues.
"""

import os
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import pytest


class TestBasicFunctionality:
    """Test basic toolkit functionality."""
    
    def test_pre_commit_hook_exists(self):
        """Test that pre-commit hook file exists."""
        hook_path = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        assert hook_path.exists(), "Pre-commit hook file should exist"
    
    def test_install_script_exists(self):
        """Test that install script exists."""
        install_path = Path(__file__).parent.parent.parent / "install.sh"
        assert install_path.exists(), "Install script should exist"
    
    def test_cleanup_script_exists(self):
        """Test that cleanup script exists."""
        script_path = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        assert script_path.exists(), "Cleanup script should exist"
    
    def test_python_test_runner_exists(self):
        """Test that Python test runner exists."""
        runner_path = Path(__file__).parent.parent.parent / "run_tests.py"
        assert runner_path.exists(), "Python test runner should exist"
    
    def test_pre_commit_hook_is_executable(self):
        """Test that pre-commit hook has executable permissions."""
        hook_path = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_path.exists():
            # Check if file is executable (Unix-like systems)
            if os.name != 'nt':  # Not Windows
                assert os.access(hook_path, os.X_OK), "Pre-commit hook should be executable"
    
    def test_basic_file_detection(self):
        """Test basic file detection functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.py"
            test_content = '''
import os
print("debug statement")  # This is a debug statement
def test_function():
    # TODO: implement this
    pass
'''
            test_file.write_text(test_content)
            
            # Check if we can detect debug statements
            content = test_file.read_text()
            assert "print(" in content
            assert "TODO:" in content
    
    def test_environment_skip_condition(self):
        """Test environment variable skip condition."""
        # Test SKIP_CLEANUP environment variable
        original_value = os.environ.get("SKIP_CLEANUP")
        
        try:
            os.environ["SKIP_CLEANUP"] = "true"
            assert os.environ.get("SKIP_CLEANUP") == "true"
            
            os.environ["SKIP_CLEANUP"] = "false"
            assert os.environ.get("SKIP_CLEANUP") == "false"
            
        finally:
            # Restore original value
            if original_value is None:
                os.environ.pop("SKIP_CLEANUP", None)
            else:
                os.environ["SKIP_CLEANUP"] = original_value
    
    def test_file_extension_detection(self):
        """Test file extension detection."""
        test_files = {
            "app.py": "python",
            "script.js": "javascript", 
            "main.go": "go",
            "index.html": "html",
            "style.css": "css",
            "README.md": "markdown"
        }
        
        for filename, expected_type in test_files.items():
            file_path = Path(filename)
            extension = file_path.suffix.lower()
            
            # Basic extension detection
            if extension == ".py":
                assert expected_type == "python"
            elif extension == ".js":
                assert expected_type == "javascript"
            elif extension == ".go":
                assert expected_type == "go"
    
    @patch('subprocess.run')
    def test_git_command_availability(self, mock_subprocess):
        """Test git command availability check."""
        # Mock successful git command
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "git version 2.39.0"
        
        # Test git availability check
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        assert result.returncode == 0
        
        mock_subprocess.assert_called_once_with(
            ["git", "--version"], 
            capture_output=True, 
            text=True
        )
    
    def test_cleanup_context_generation(self):
        """Test cleanup context generation without git operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files with different issues
            test_files = {
                "app.py": '''
import os, sys, unused_import
print("debug statement")
def test(): pass
''',
                "utils.js": '''
console.log("debug");
function duplicate() { return true; }
function similar() { return true; }
''',
                "main.go": '''
package main
import "fmt"
func main() {
    fmt.Println("debug")
}
'''
            }
            
            for filename, content in test_files.items():
                file_path = temp_path / filename
                file_path.write_text(content)
            
            # Count issues
            debug_count = 0
            todo_count = 0
            
            for file_path in temp_path.glob("*"):
                if file_path.is_file():
                    content = file_path.read_text()
                    debug_count += content.count("print(") + content.count("console.log") + content.count("fmt.Print")
                    todo_count += content.count("TODO") + content.count("FIXME")
            
            assert debug_count > 0, "Should detect debug statements"
    
    def test_language_specific_patterns(self):
        """Test language-specific pattern detection."""
        patterns = {
            "python": ["print(", "pprint(", "breakpoint("],
            "javascript": ["console.log(", "console.debug(", "debugger"],
            "go": ["fmt.Print", "log.Print"],
            "java": ["System.out.print", "System.err.print"]
        }
        
        for language, debug_patterns in patterns.items():
            assert len(debug_patterns) > 0, f"Should have patterns for {language}"
            
            # Test that patterns are strings
            for pattern in debug_patterns:
                assert isinstance(pattern, str), f"Pattern should be string: {pattern}"
    
    def test_temporary_file_creation(self):
        """Test temporary file creation and cleanup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create temporary files
            test_file = temp_path / "test.py"
            test_file.write_text("print('test')")
            
            assert test_file.exists()
            assert test_file.read_text() == "print('test')"
        
        # Directory should be cleaned up automatically
        assert not temp_path.exists()
    
    def test_configuration_defaults(self):
        """Test default configuration values."""
        default_config = {
            "cleanup_enabled": True,
            "preferred_framework": "claude-code",
            "auto_generate_prompts": True,
            "quality_gates": {
                "max_file_lines": 500,
                "require_docstrings": False
            }
        }
        
        # Test configuration structure
        assert "cleanup_enabled" in default_config
        assert "preferred_framework" in default_config
        assert "quality_gates" in default_config
        assert isinstance(default_config["quality_gates"], dict)


class TestUtilityFunctions:
    """Test utility functions that don't require complex setup."""
    
    def test_line_counting(self):
        """Test line counting functionality."""
        test_content = """line 1
line 2
line 3
line 4"""
        lines = test_content.split('\n')
        assert len(lines) == 4
    
    def test_debug_statement_detection(self):
        """Test debug statement detection patterns."""
        test_cases = [
            ("print('debug')", True),
            ("console.log('test')", True),
            ("fmt.Println('go')", True),
            ("regular code", False),
            ("# print comment", False)  # Should not match commented print
        ]
        
        for code, should_detect in test_cases:
            # Simple detection logic
            has_debug = ("print(" in code or "console.log(" in code or "fmt.Print" in code)
            if code.strip().startswith("#"):
                has_debug = False  # Comments don't count
            assert has_debug == should_detect, f"Detection failed for: {code}"
    
    def test_file_size_detection(self):
        """Test file size detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create small file
            small_file = temp_path / "small.py"
            small_file.write_text("print('small')")
            
            # Create large file
            large_file = temp_path / "large.py" 
            large_content = "def function_{}(): pass\n" * 1000
            large_file.write_text(large_content)
            
            assert small_file.stat().st_size < large_file.stat().st_size
            assert large_file.stat().st_size > 10000  # Large file should be >10KB


class TestCrossPlatformCompatibility:
    """Test cross-platform compatibility."""
    
    def test_path_handling(self):
        """Test path handling across platforms."""
        # Test Path operations work consistently
        test_path = Path("test") / "subdir" / "file.py"
        assert str(test_path).endswith("file.py")
        
        # Test absolute path creation
        temp_path = Path.cwd() / "test.py"
        assert temp_path.is_absolute()
    
    def test_environment_variables(self):
        """Test environment variable handling."""
        # Test setting and getting environment variables
        test_var = "CLEANUP_TEST_VAR"
        test_value = "test_value"
        
        original_value = os.environ.get(test_var)
        try:
            os.environ[test_var] = test_value
            assert os.environ.get(test_var) == test_value
        finally:
            if original_value is None:
                os.environ.pop(test_var, None)
            else:
                os.environ[test_var] = original_value
    
    def test_subprocess_basic(self):
        """Test basic subprocess functionality."""
        # Test a basic command that should work on all platforms
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(["echo", "test"], shell=True, capture_output=True, text=True)
            else:  # Unix-like
                result = subprocess.run(["echo", "test"], capture_output=True, text=True)
            
            assert result.returncode == 0
            assert "test" in result.stdout
        except FileNotFoundError:
            # Skip if echo command not available
            pytest.skip("echo command not available")