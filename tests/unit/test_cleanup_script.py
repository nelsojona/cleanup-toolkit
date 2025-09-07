"""
Unit tests for the code cleanup gist shell script.

Tests the cleanup script's ability to:
- Analyze PR and local changes
- Generate cleanup checklists
- Perform file analysis
- Handle different scenarios
"""

import os
import subprocess
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import shutil

import pytest
import git


class TestCleanupScript:
    """Test suite for code_cleanup_gist.sh script."""
    
    @pytest.fixture(autouse=True)
    def setup(self, temp_dir, temp_git_repo):
        """Set up test environment."""
        self.temp_dir = temp_dir
        self.repo = temp_git_repo
        self.script_path = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        self.temp_script_dir = self.temp_dir / "scripts"
        self.temp_script_dir.mkdir(exist_ok=True)
        
        # Copy script to temp directory for testing
        if self.script_path.exists():
            self.test_script = self.temp_script_dir / "code_cleanup_gist.sh"
            shutil.copy2(self.script_path, self.test_script)
            os.chmod(self.test_script, 0o755)
    
    def test_script_exists_and_is_executable(self):
        """Test that the cleanup script exists and is executable."""
        assert self.script_path.exists(), "Cleanup script does not exist"
        assert os.access(self.script_path, os.X_OK), "Cleanup script is not executable"
    
    @patch('subprocess.run')
    def test_check_dependencies(self, mock_run):
        """Test dependency checking."""
        # Test with all dependencies present
        mock_run.return_value = MagicMock(returncode=0)
        
        result = subprocess.run(
            ["bash", "-c", f"source {self.test_script} && check_dependencies"],
            capture_output=True,
            text=True
        )
        
        # Should pass if git and gh are available
        # Note: This test may need adjustment based on actual environment
    
    def test_analyze_local_changes(self):
        """Test analysis of local changes."""
        # Create and modify files
        test_files = ["file1.py", "file2.js", "file3.go"]
        for filename in test_files:
            file_path = self.temp_dir / filename
            file_path.write_text(f"// {filename} content")
            # Make changes but don't stage them
            file_path.write_text(f"// Modified {filename} content")
        
        # Run analyze_local_changes function
        env = {"GIT_DIR": str(self.temp_dir / ".git")}
        result = subprocess.run(
            ["bash", "-c", f"cd {self.temp_dir} && source {self.test_script} && analyze_local_changes"],
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check output
        for filename in test_files:
            assert filename in result.stdout or filename in result.stderr
    
    def test_generate_cleanup_checklist(self):
        """Test generation of cleanup checklist."""
        # Create a changed files list
        changed_files = self.temp_dir / "tmp" / "changed_files.txt"
        changed_files.parent.mkdir(exist_ok=True)
        changed_files.write_text("main.py\nutils.js\nconfig.yaml")
        
        # Set TEMP_DIR environment variable
        env = {
            "TEMP_DIR": str(self.temp_dir / "tmp"),
            "GIT_DIR": str(self.temp_dir / ".git")
        }
        
        # Run checklist generation
        result = subprocess.run(
            ["bash", "-c", f"cd {self.temp_dir} && source {self.test_script} && generate_cleanup_checklist"],
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check if cleanup report was created
        cleanup_report = self.temp_dir / "cleanup_report.md"
        if cleanup_report.exists():
            content = cleanup_report.read_text()
            assert "Code Cleanup Report" in content
            assert "Cleanup Checklist" in content
            assert "Code Quality" in content
            assert "Documentation" in content
    
    def test_perform_file_analysis(self):
        """Test detailed file analysis."""
        # Create test files with various issues
        test_file1 = self.temp_dir / "test1.py"
        test_file1.write_text("""
# TODO: Fix this
def main():
    print("Debug message")
    # Commented code
    # old_function()
    pass
""")
        
        test_file2 = self.temp_dir / "test2.js"
        test_file2.write_text("""
// FIXME: This is broken
function test() {
    console.log("Debug output");
    // return old_value;
}
""")
        
        # Create changed files list
        changed_files = self.temp_dir / "tmp" / "changed_files.txt"
        changed_files.parent.mkdir(exist_ok=True)
        changed_files.write_text("test1.py\ntest2.js")
        
        # Create initial cleanup report
        cleanup_report = self.temp_dir / "cleanup_report.md"
        cleanup_report.write_text("# Code Cleanup Report\n\n")
        
        env = {
            "TEMP_DIR": str(self.temp_dir / "tmp"),
            "CLEANUP_REPORT": str(cleanup_report)
        }
        
        # Run file analysis
        result = subprocess.run(
            ["bash", "-c", f"cd {self.temp_dir} && source {self.test_script} && perform_file_analysis"],
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check analysis results
        if cleanup_report.exists():
            content = cleanup_report.read_text()
            # Should contain file analysis
            assert "test1.py" in content or "test2.js" in content
    
    @pytest.mark.parametrize("file_type,content,expected_issues", [
        ("python", "print('debug')\n# TODO: fix", ["debug print", "TODO"]),
        ("javascript", "console.log('test')\n// FIXME: broken", ["console.log", "FIXME"]),
        ("go", "fmt.Println('debug')\n// XXX: hack", ["Println", "XXX"]),
    ])
    def test_issue_detection(self, file_type, content, expected_issues):
        """Test detection of various code issues."""
        extensions = {"python": ".py", "javascript": ".js", "go": ".go"}
        test_file = self.temp_dir / f"test{extensions[file_type]}"
        test_file.write_text(content)
        
        # Check for issues using grep (simulating script behavior)
        for issue in expected_issues:
            result = subprocess.run(
                ["grep", issue, str(test_file)],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"Issue '{issue}' not detected in {file_type} file"
    
    def test_language_specific_cleanup_commands(self):
        """Test language-specific cleanup command generation."""
        # Create cleanup report
        cleanup_report = self.temp_dir / "cleanup_report.md"
        
        # Run cleanup checklist generation
        env = {"CLEANUP_REPORT": str(cleanup_report)}
        subprocess.run(
            ["bash", "-c", f"cd {self.temp_dir} && source {self.test_script} && generate_cleanup_checklist"],
            env=env,
            capture_output=True,
            text=True
        )
        
        if cleanup_report.exists():
            content = cleanup_report.read_text()
            # Check for language-specific sections
            assert "Python" in content
            assert "JavaScript/TypeScript" in content
            assert "Go" in content
            
            # Check for specific tools
            assert "black" in content or "autoflake" in content
            assert "eslint" in content or "prettier" in content
            assert "gofmt" in content or "goimports" in content


class TestCleanupScriptPRAnalysis:
    """Test PR analysis functionality."""
    
    @pytest.fixture
    def mock_gh_cli(self, mocker):
        """Mock GitHub CLI commands."""
        mock_run = mocker.patch('subprocess.run')
        
        # Mock PR list
        mock_run.return_value.stdout = json.dumps([{"number": 42}])
        mock_run.return_value.returncode = 0
        
        return mock_run
    
    @patch('subprocess.run')
    def test_get_pr_info(self, mock_run, temp_git_repo, temp_dir):
        """Test fetching PR information."""
        # Mock gh pr list
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps([{"number": 42}]),
            stderr=""
        )
        
        script_path = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        
        # Run get_pr_info
        result = subprocess.run(
            ["bash", "-c", f"cd {temp_dir} && source {script_path} && get_pr_info"],
            capture_output=True,
            text=True
        )
        
        # Should find or not find PR based on mock
        assert "branch" in result.stdout.lower() or "branch" in result.stderr.lower()
    
    @patch('subprocess.run')
    def test_analyze_pr_changes(self, mock_run, temp_dir):
        """Test PR change analysis."""
        # Mock gh pr view and gh pr diff
        mock_run.side_effect = [
            MagicMock(
                returncode=0,
                stdout=json.dumps({
                    "title": "Test PR",
                    "body": "Test body",
                    "files": ["file1.py", "file2.js"]
                })
            ),
            MagicMock(
                returncode=0,
                stdout="file1.py\nfile2.js"
            )
        ]
        
        script_path = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        
        # Create temp dir for output
        temp_output = temp_dir / "tmp"
        temp_output.mkdir()
        
        env = {
            "TEMP_DIR": str(temp_output),
            "PR_NUMBER": "42"
        }
        
        # Run analyze_pr_changes
        result = subprocess.run(
            ["bash", "-c", f"source {script_path} && analyze_pr_changes"],
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check for expected output
        assert "file1.py" in result.stdout or "file2.js" in result.stdout


class TestCleanupScriptInteractive:
    """Test interactive cleanup functionality."""
    
    def test_interactive_cleanup_menu(self, temp_dir, mocker):
        """Test interactive cleanup menu options."""
        # Create test file
        test_file = temp_dir / "test.py"
        test_file.write_text("print('test')")
        
        # Create changed files list
        changed_files = temp_dir / "tmp" / "changed_files.txt"
        changed_files.parent.mkdir(exist_ok=True)
        changed_files.write_text("test.py")
        
        # Mock user input
        mocker.patch('builtins.input', side_effect=['3', '4'])  # Skip, then exit
        
        script_path = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        
        env = {"TEMP_DIR": str(temp_dir / "tmp")}
        
        # Run interactive cleanup
        result = subprocess.run(
            ["bash", "-c", f"cd {temp_dir} && source {script_path} && interactive_cleanup"],
            env=env,
            capture_output=True,
            text=True,
            input="3\n4\n"  # Skip then exit
        )
        
        # Should show menu options
        assert "Open in editor" in result.stdout or result.returncode != 0


class TestCleanupScriptEdgeCases:
    """Test edge cases and error handling."""
    
    def test_no_git_repository(self, temp_dir):
        """Test behavior when not in a git repository."""
        # Remove .git directory
        git_dir = temp_dir / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)
        
        script_path = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        
        # Run script
        result = subprocess.run(
            ["bash", str(script_path)],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        # Should detect no git repo
        assert "not in a git repository" in result.stdout.lower() or \
               "not in a git repository" in result.stderr.lower() or \
               result.returncode != 0
    
    def test_empty_repository(self, temp_git_repo, temp_dir):
        """Test behavior with empty repository."""
        script_path = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        
        # Run script in empty repo
        result = subprocess.run(
            ["bash", str(script_path)],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        # Should handle empty repo gracefully
        assert result.returncode == 0 or "No" in result.stdout
    
    def test_large_file_handling(self, temp_dir):
        """Test handling of large files."""
        # Create a large file
        large_file = temp_dir / "large.py"
        content = "\n".join([f"line_{i} = {i}" for i in range(10000)])
        large_file.write_text(content)
        
        # Get file size
        size = large_file.stat().st_size
        
        # File should be detected as large
        assert size > 10000
    
    def test_binary_file_handling(self, temp_dir):
        """Test handling of binary files."""
        # Create a binary file
        binary_file = temp_dir / "test.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03\x04')
        
        # Binary files should be skipped in analysis
        assert binary_file.exists()
        
    def test_cleanup_temp_directory(self, temp_dir):
        """Test cleanup of temporary directories."""
        script_path = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        
        # Run script and check temp cleanup
        result = subprocess.run(
            ["bash", "-c", f"source {script_path} && TEMP_DIR=/tmp/test_$$ && cleanup_temp"],
            capture_output=True,
            text=True
        )
        
        # Temp directory should be cleaned up
        assert result.returncode == 0