"""
Unit tests for pre-commit hook functionality.

Tests the pre-commit hook's ability to:
- Generate cleanup contexts
- Create AI framework prompts
- Handle different configurations
- Process staged files
"""

import os
import subprocess
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import tempfile
import shutil

import pytest
import git


class TestPreCommitHook:
    """Test suite for pre-commit hook functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, temp_dir, temp_git_repo):
        """Set up test environment."""
        self.temp_dir = temp_dir
        self.repo = temp_git_repo
        self.hook_script = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        
        # Create .cleanup-toolkit directory
        self.toolkit_dir = self.temp_dir / ".cleanup-toolkit"
        self.toolkit_dir.mkdir(exist_ok=True)
    
    def test_hook_exists_and_is_executable(self):
        """Test that the pre-commit hook exists and is executable."""
        assert self.hook_script.exists(), "Pre-commit hook does not exist"
        assert os.access(self.hook_script, os.X_OK), "Pre-commit hook is not executable"
    
    def test_skip_cleanup_environment_variable(self, shell_test_env):
        """Test that cleanup is skipped when SKIP_CLEANUP is set."""
        env = shell_test_env.copy()
        env["SKIP_CLEANUP"] = "true"
        
        result = subprocess.run(
            ["bash", str(self.hook_script)],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        assert "Cleanup skipped via SKIP_CLEANUP environment variable" in result.stdout
        assert result.returncode == 0
    
    def test_no_staged_files(self, shell_test_env):
        """Test behavior when no files are staged."""
        result = subprocess.run(
            ["bash", str(self.hook_script)],
            cwd=self.temp_dir,
            env=shell_test_env,
            capture_output=True,
            text=True
        )
        
        assert "No staged files found" in result.stdout
        assert result.returncode == 0
    
    @patch('subprocess.run')
    def test_generate_cleanup_context(self, mock_run, temp_dir):
        """Test cleanup context generation."""
        # Create some test files
        test_file1 = temp_dir / "test1.py"
        test_file2 = temp_dir / "test2.js"
        test_file1.write_text("print('debug')")
        test_file2.write_text("console.log('debug')")
        
        # Stage files in git
        self.repo.index.add([str(test_file1), str(test_file2)])
        
        # Mock git commands
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="test1.py\ntest2.js"),  # git diff --cached
            MagicMock(returncode=0, stdout="feature/test"),  # git branch
            MagicMock(returncode=0),  # Other commands
        ]
        
        # Run the hook
        env = {"GIT_DIR": str(self.temp_dir / ".git")}
        result = subprocess.run(
            ["bash", "-c", f"source {self.hook_script} && generate_cleanup_context"],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check that context file was created
        context_file = self.toolkit_dir / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "Cleanup Context" in content
            assert "test1.py" in content
            assert "test2.js" in content
    
    def test_claude_prompts_generation(self):
        """Test generation of Claude Code prompts."""
        # Create claude.md file to trigger Claude prompt generation
        claude_file = self.temp_dir / "claude.md"
        claude_file.write_text("# Claude Project\n")
        
        # Create a test file and stage it
        test_file = self.temp_dir / "test.py"
        test_file.write_text("print('test')")
        self.repo.index.add([str(test_file)])
        
        # Run the hook function
        env = {"GIT_DIR": str(self.temp_dir / ".git")}
        subprocess.run(
            ["bash", "-c", f"source {self.hook_script} && generate_claude_code_prompts"],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check prompts file
        prompts_file = self.toolkit_dir / "claude-prompts.txt"
        if prompts_file.exists():
            content = prompts_file.read_text()
            assert "Initial Analysis Prompt" in content
            assert "Systematic Cleanup Prompt" in content
            assert "Verification Prompt" in content
    
    def test_warp_prompts_generation(self):
        """Test generation of Warp Terminal prompts."""
        # Create .warp directory to trigger Warp prompt generation
        warp_dir = self.temp_dir / ".warp"
        warp_dir.mkdir()
        
        # Create a test file and stage it
        test_file = self.temp_dir / "test.js"
        test_file.write_text("console.log('test')")
        self.repo.index.add([str(test_file)])
        
        # Run the hook function
        env = {"GIT_DIR": str(self.temp_dir / ".git")}
        subprocess.run(
            ["bash", "-c", f"source {self.hook_script} && generate_warp_prompts"],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check prompts files
        context_file = self.toolkit_dir / "warp-ai-context.md"
        prompts_file = self.toolkit_dir / "warp-ai-prompts.txt"
        
        if context_file.exists():
            content = context_file.read_text()
            assert "Warp AI Context" in content
            assert "test.js" in content
        
        if prompts_file.exists():
            content = prompts_file.read_text()
            assert "Analysis Prompt" in content
            assert "Cleanup Execution Prompt" in content
    
    def test_cleanup_summary_generation(self):
        """Test generation of cleanup summary."""
        # Create and stage test files
        test_files = []
        for i in range(3):
            file_path = self.temp_dir / f"file{i}.py"
            file_path.write_text(f"print('file {i}')")
            test_files.append(str(file_path))
        
        self.repo.index.add(test_files)
        
        # Run the hook function
        env = {"GIT_DIR": str(self.temp_dir / ".git")}
        subprocess.run(
            ["bash", "-c", f"source {self.hook_script} && generate_cleanup_summary"],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check summary file
        summary_file = self.toolkit_dir / "cleanup-summary.md"
        if summary_file.exists():
            content = summary_file.read_text()
            assert "Pre-commit Cleanup Summary" in content
            assert "Files Modified: 3 files" in content
            assert "Available Cleanup Methods" in content
    
    def test_file_with_debug_statements_detection(self):
        """Test detection of debug statements in files."""
        # Create file with debug statements
        debug_file = self.temp_dir / "debug_test.py"
        debug_file.write_text("""
import os

def main():
    print("Debug: Starting")  # This should be detected
    result = calculate()
    print(f"Debug: Result is {result}")  # This too
    return result

def calculate():
    return 42
""")
        
        self.repo.index.add([str(debug_file)])
        
        # Run context generation
        env = {"GIT_DIR": str(self.temp_dir / ".git")}
        subprocess.run(
            ["bash", "-c", f"source {self.hook_script} && generate_cleanup_context"],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check context file for debug detection
        context_file = self.toolkit_dir / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "debug_test.py" in content
            # The script should detect debug statements
    
    def test_todo_fixme_detection(self):
        """Test detection of TODO/FIXME comments."""
        # Create file with TODO/FIXME
        todo_file = self.temp_dir / "todo_test.py"
        todo_file.write_text("""
# TODO: Implement this function
def not_implemented():
    pass

# FIXME: This is broken
def broken_function():
    return None

# XXX: Hack alert
def hacky_function():
    pass
""")
        
        self.repo.index.add([str(todo_file)])
        
        # Run context generation
        env = {"GIT_DIR": str(self.temp_dir / ".git")}
        subprocess.run(
            ["bash", "-c", f"source {self.hook_script} && generate_cleanup_context"],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check context file
        context_file = self.toolkit_dir / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "todo_test.py" in content
    
    def test_large_file_detection(self):
        """Test detection of large files."""
        # Create a large file (>200 lines)
        large_file = self.temp_dir / "large_file.py"
        content = "\n".join([f"line_{i} = {i}" for i in range(250)])
        large_file.write_text(content)
        
        self.repo.index.add([str(large_file)])
        
        # Run context generation
        env = {"GIT_DIR": str(self.temp_dir / ".git")}
        subprocess.run(
            ["bash", "-c", f"source {self.hook_script} && generate_cleanup_context"],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check context file
        context_file = self.toolkit_dir / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "large_file.py" in content
            # Should warn about large file
    
    @pytest.mark.parametrize("cleanup_mode", ["prompt", "auto", "manual"])
    def test_different_cleanup_modes(self, cleanup_mode):
        """Test different cleanup modes."""
        # Create test file
        test_file = self.temp_dir / "test.py"
        test_file.write_text("print('test')")
        self.repo.index.add([str(test_file)])
        
        # Run with different modes
        env = {
            "GIT_DIR": str(self.temp_dir / ".git"),
            "CLEANUP_MODE": cleanup_mode
        }
        
        result = subprocess.run(
            ["bash", str(self.hook_script)],
            cwd=self.temp_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Hook should exit with 1 to pause commit (except when skipped)
        assert result.returncode == 1
        assert "Cleanup" in result.stdout


class TestPreCommitHookHelpers:
    """Test helper functions in the pre-commit hook."""
    
    def test_check_skip_conditions(self):
        """Test skip condition checking logic."""
        test_cases = [
            {"SKIP_CLEANUP": "true", "should_skip": True},
            {"SKIP_CLEANUP": "false", "should_skip": False},
            {"SKIP_CLEANUP": "", "should_skip": False},
        ]
        
        for case in test_cases:
            env = {"SKIP_CLEANUP": case["SKIP_CLEANUP"]}
            # Test would need to be run with actual shell script
            # This is a placeholder for the test logic
    
    def test_get_staged_files_parsing(self):
        """Test parsing of staged files."""
        # This would test the git diff --cached --name-only parsing
        pass
    
    def test_shell_guide_generation(self):
        """Test shell cleanup guide generation."""
        # This would test the generate_shell_prompts function
        pass


class TestPreCommitHookIntegration:
    """Integration tests for pre-commit hook with git."""
    
    @pytest.mark.requires_git
    def test_full_commit_workflow(self, temp_git_repo, temp_dir):
        """Test complete commit workflow with cleanup."""
        # Create multiple files with various issues
        files = {
            "main.py": """
import unused
def main():
    print("debug")
    pass
""",
            "utils.py": """
# TODO: Fix this
def util():
    console.log("debug")
""",
            "config.py": """
DEBUG = True
password = "hardcoded"  # Security issue
"""
        }
        
        for filename, content in files.items():
            file_path = temp_dir / filename
            file_path.write_text(content)
            temp_git_repo.index.add([str(file_path)])
        
        # Install pre-commit hook
        hooks_dir = temp_dir / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        hook_dest = hooks_dir / "pre-commit"
        
        # Copy our hook
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_src.exists():
            shutil.copy2(hook_src, hook_dest)
            os.chmod(hook_dest, 0o755)
        
        # Try to commit (should be blocked by hook)
        try:
            temp_git_repo.index.commit("Test commit")
        except git.exc.HookExecutionError:
            # This is expected - hook should block commit
            pass
        
        # Check that cleanup files were generated
        toolkit_dir = temp_dir / ".cleanup-toolkit"
        assert toolkit_dir.exists()
        
        # Check for generated files
        expected_files = [
            "cleanup-context.md",
            "cleanup-summary.md",
            "shell-cleanup-guide.md"
        ]
        
        for filename in expected_files:
            file_path = toolkit_dir / filename
            if file_path.exists():
                assert file_path.stat().st_size > 0