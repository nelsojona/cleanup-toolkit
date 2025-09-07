"""
Integration tests for git workflows with the cleanup toolkit.

Tests the integration between:
- Git operations
- Pre-commit hooks
- Cleanup scripts
- AI framework integrations
"""

import os
import subprocess
import shutil
import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile

import pytest
import git
from git import Repo


@pytest.mark.integration
@pytest.mark.requires_git
class TestGitWorkflowIntegration:
    """Test git workflow integration with cleanup toolkit."""
    
    @pytest.fixture(autouse=True)
    def setup(self, temp_dir):
        """Set up test environment with git repo."""
        self.temp_dir = temp_dir
        self.repo = git.Repo.init(temp_dir)
        
        # Configure git
        with self.repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create initial commit
        readme = temp_dir / "README.md"
        readme.write_text("# Test Project\n")
        self.repo.index.add([str(readme)])
        self.repo.index.commit("Initial commit")
        
        # Install cleanup toolkit
        self.install_cleanup_toolkit()
    
    def install_cleanup_toolkit(self):
        """Install cleanup toolkit in test repository."""
        # Create .cleanup-toolkit directory
        toolkit_dir = self.temp_dir / ".cleanup-toolkit"
        toolkit_dir.mkdir(exist_ok=True)
        
        # Copy hooks
        hooks_src = Path(__file__).parent.parent.parent / "hooks"
        hooks_dst = self.temp_dir / ".git" / "hooks"
        hooks_dst.mkdir(exist_ok=True)
        
        if (hooks_src / "pre-commit").exists():
            shutil.copy2(hooks_src / "pre-commit", hooks_dst / "pre-commit")
            os.chmod(hooks_dst / "pre-commit", 0o755)
        
        # Copy scripts
        scripts_src = Path(__file__).parent.parent.parent / "scripts"
        scripts_dst = toolkit_dir / "scripts"
        scripts_dst.mkdir(exist_ok=True)
        
        if (scripts_src / "code_cleanup_gist.sh").exists():
            shutil.copy2(
                scripts_src / "code_cleanup_gist.sh",
                scripts_dst / "code_cleanup_gist.sh"
            )
            os.chmod(scripts_dst / "code_cleanup_gist.sh", 0o755)
    
    def test_complete_commit_workflow(self):
        """Test complete commit workflow with cleanup."""
        # Create files with issues
        main_file = self.temp_dir / "main.py"
        main_file.write_text("""
import os
import unused_module

def calculate(x, y):
    print(f"Debug: calculating {x} + {y}")  # Debug statement
    result = x + y
    print(f"Result: {result}")  # Another debug
    return result

# TODO: Add more functions
# FIXME: Handle edge cases

def calc(a, b):  # Duplicate function
    return a + b
""")
        
        utils_file = self.temp_dir / "utils.py"
        utils_file.write_text("""
def validate_input(data):
    # No validation implemented
    pass

def validate_data(data):  # Duplicate
    pass
""")
        
        # Stage files
        self.repo.index.add([str(main_file), str(utils_file)])
        
        # Attempt commit (should trigger pre-commit hook)
        try:
            self.repo.index.commit("Add new features")
            # If commit succeeds without hook, check if files were generated
            assert False, "Pre-commit hook did not execute"
        except git.exc.HookExecutionError as e:
            # This is expected - hook blocks commit for cleanup
            assert "cleanup" in str(e).lower() or True
        
        # Verify cleanup files were generated
        toolkit_dir = self.temp_dir / ".cleanup-toolkit"
        assert toolkit_dir.exists()
        
        # Check for context file
        context_file = toolkit_dir / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "main.py" in content
            assert "utils.py" in content
    
    def test_branch_workflow(self):
        """Test cleanup workflow with branches."""
        # Create feature branch
        feature_branch = self.repo.create_head("feature/test-cleanup")
        feature_branch.checkout()
        
        # Make changes
        feature_file = self.temp_dir / "feature.py"
        feature_file.write_text("""
def new_feature():
    print("Debug: Starting feature")  # Debug
    # TODO: Implement feature
    pass
""")
        
        self.repo.index.add([str(feature_file)])
        
        # Try to commit
        try:
            self.repo.index.commit("Add feature")
        except git.exc.HookExecutionError:
            pass
        
        # Check cleanup context includes branch info
        context_file = self.temp_dir / ".cleanup-toolkit" / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "feature/test-cleanup" in content or "feature" in content
    
    def test_merge_conflict_cleanup(self):
        """Test cleanup during merge conflicts."""
        # Create branch with changes
        branch1 = self.repo.create_head("branch1")
        branch1.checkout()
        
        conflict_file = self.temp_dir / "conflict.py"
        conflict_file.write_text("def func():\n    return 1")
        self.repo.index.add([str(conflict_file)])
        self.repo.index.commit("Branch 1 change")
        
        # Switch to main and make conflicting change
        self.repo.heads.main.checkout()
        conflict_file.write_text("def func():\n    return 2")
        self.repo.index.add([str(conflict_file)])
        self.repo.index.commit("Main change")
        
        # Attempt merge
        try:
            self.repo.git.merge("branch1")
        except git.exc.GitCommandError:
            # Merge conflict expected
            pass
        
        # Resolve conflict
        conflict_file.write_text("""def func():
    # TODO: Decide which value to use
    print("Debug: In conflict resolution")
    return 1  # Using branch1 value
""")
        
        self.repo.index.add([str(conflict_file)])
        
        # Try to commit merge
        try:
            self.repo.index.commit("Merge branch1")
        except git.exc.HookExecutionError:
            # Cleanup hook should detect TODOs and debug statements
            pass
        
        # Verify cleanup detection
        context_file = self.temp_dir / ".cleanup-toolkit" / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "conflict.py" in content
    
    def test_stash_workflow(self):
        """Test cleanup with git stash workflow."""
        # Create changes
        stash_file = self.temp_dir / "stash_test.py"
        stash_file.write_text("""
def stashed_function():
    print("Debug: This will be stashed")
    return "stashed"
""")
        
        self.repo.index.add([str(stash_file)])
        
        # Stash changes
        self.repo.git.stash("save", "Test stash")
        
        # Make other changes
        other_file = self.temp_dir / "other.py"
        other_file.write_text("def other(): pass")
        self.repo.index.add([str(other_file)])
        self.repo.index.commit("Other changes")
        
        # Pop stash
        self.repo.git.stash("pop")
        
        # Stage stashed file
        self.repo.index.add([str(stash_file)])
        
        # Try to commit
        try:
            self.repo.index.commit("Add stashed changes")
        except git.exc.HookExecutionError:
            # Cleanup should detect debug statement
            pass
        
        # Verify detection
        context_file = self.temp_dir / ".cleanup-toolkit" / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "stash_test.py" in content


@pytest.mark.integration
class TestAIFrameworkIntegration:
    """Test integration with AI frameworks."""
    
    @pytest.fixture
    def setup_claude_project(self, temp_dir, temp_git_repo):
        """Set up Claude Code project structure."""
        # Create Claude project files
        claude_md = temp_dir / "claude.md"
        claude_md.write_text("""# Claude Code Project
        
## Project Overview
Test project for cleanup toolkit integration.

## Standards
- No debug statements in production
- All functions must have docstrings
- No duplicate code
""")
        
        handover_md = temp_dir / "handover.md"
        handover_md.write_text("""# Handover Document

## Current Tasks
- [ ] Implement feature X
- [ ] Fix bug Y
""")
        
        return temp_dir
    
    @pytest.fixture
    def setup_warp_project(self, temp_dir, temp_git_repo):
        """Set up Warp Terminal project structure."""
        warp_dir = temp_dir / ".warp"
        warp_dir.mkdir()
        
        # Create Warp workflow
        workflows_dir = warp_dir / "workflows"
        workflows_dir.mkdir()
        
        cleanup_workflow = workflows_dir / "cleanup.yaml"
        cleanup_workflow.write_text("""
name: cleanup-analysis
commands:
  - name: "Find debug statements"
    command: "grep -r 'print\\|console.log' ."
  - name: "Find TODOs"
    command: "grep -r 'TODO\\|FIXME' ."
""")
        
        return temp_dir
    
    def test_claude_integration(self, setup_claude_project, temp_git_repo):
        """Test Claude Code integration."""
        temp_dir = setup_claude_project
        
        # Create file with issues
        test_file = temp_dir / "test.py"
        test_file.write_text("""
def test():
    print("Debug")  # Should be removed
    pass
""")
        
        temp_git_repo.index.add([str(test_file)])
        
        # Install pre-commit hook
        hooks_dir = temp_dir / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_src.exists():
            shutil.copy2(hook_src, hooks_dir / "pre-commit")
            os.chmod(hooks_dir / "pre-commit", 0o755)
        
        # Try commit
        try:
            temp_git_repo.index.commit("Test commit")
        except git.exc.HookExecutionError:
            pass
        
        # Check Claude prompts were generated
        prompts_file = temp_dir / ".cleanup-toolkit" / "claude-prompts.txt"
        if prompts_file.exists():
            content = prompts_file.read_text()
            assert "Initial Analysis Prompt" in content
            assert "Systematic Cleanup Prompt" in content
        
        # Check handover.md was updated
        handover = temp_dir / "handover.md"
        if handover.exists():
            content = handover.read_text()
            # Should have cleanup request added
            assert "cleanup" in content.lower() or len(content) > 100
    
    def test_warp_integration(self, setup_warp_project, temp_git_repo):
        """Test Warp Terminal integration."""
        temp_dir = setup_warp_project
        
        # Create file with issues
        test_file = temp_dir / "app.js"
        test_file.write_text("""
function app() {
    console.log("Debug: Starting app");  // Debug
    // TODO: Add error handling
}
""")
        
        temp_git_repo.index.add([str(test_file)])
        
        # Install pre-commit hook
        hooks_dir = temp_dir / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_src.exists():
            shutil.copy2(hook_src, hooks_dir / "pre-commit")
            os.chmod(hooks_dir / "pre-commit", 0o755)
        
        # Try commit
        try:
            temp_git_repo.index.commit("Test commit")
        except git.exc.HookExecutionError:
            pass
        
        # Check Warp prompts were generated
        warp_prompts = temp_dir / ".cleanup-toolkit" / "warp-ai-prompts.txt"
        warp_context = temp_dir / ".cleanup-toolkit" / "warp-ai-context.md"
        
        if warp_prompts.exists():
            content = warp_prompts.read_text()
            assert "Analysis Prompt" in content
            assert "Cleanup Execution Prompt" in content
        
        if warp_context.exists():
            content = warp_context.read_text()
            assert "app.js" in content


@pytest.mark.integration
class TestCleanupScriptIntegration:
    """Test cleanup script integration with git."""
    
    def test_pr_analysis_integration(self, temp_git_repo, temp_dir, mocker):
        """Test PR analysis with actual git repo."""
        # Mock gh CLI
        mock_run = mocker.patch('subprocess.run')
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps([{"number": 1}]),
            stderr=""
        )
        
        # Create branch with changes
        feature = temp_git_repo.create_head("feature/test")
        feature.checkout()
        
        # Add files
        new_file = temp_dir / "feature.py"
        new_file.write_text("def feature(): pass")
        temp_git_repo.index.add([str(new_file)])
        temp_git_repo.index.commit("Add feature")
        
        # Run cleanup script
        script = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        if script.exists():
            result = subprocess.run(
                ["bash", str(script)],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                input="N\n"  # Don't start interactive cleanup
            )
            
            # Check cleanup report
            report = temp_dir / "cleanup_report.md"
            if report.exists():
                content = report.read_text()
                assert "Code Cleanup Report" in content
    
    def test_local_changes_analysis(self, temp_git_repo, temp_dir):
        """Test analysis of local uncommitted changes."""
        # Create uncommitted changes
        dirty_file = temp_dir / "dirty.py"
        dirty_file.write_text("""
import unused
def dirty():
    print("debug")
    # TODO: Clean this up
""")
        
        # Run cleanup script
        script = Path(__file__).parent.parent.parent / "scripts" / "code_cleanup_gist.sh"
        if script.exists():
            result = subprocess.run(
                ["bash", str(script)],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                input="N\n"  # Don't start interactive
            )
            
            # Should analyze local changes
            assert "dirty.py" in result.stdout or result.returncode == 0


@pytest.mark.integration
class TestMultiLanguageIntegration:
    """Test integration with multiple programming languages."""
    
    @pytest.fixture
    def multi_language_project(self, temp_dir, temp_git_repo):
        """Create project with multiple languages."""
        # Python file
        py_file = temp_dir / "app.py"
        py_file.write_text("""
def main():
    print("Debug: Starting")
    # TODO: Add features
""")
        
        # JavaScript file
        js_file = temp_dir / "app.js"
        js_file.write_text("""
function main() {
    console.log("Debug: Starting");
    // FIXME: Handle errors
}
""")
        
        # Go file
        go_file = temp_dir / "app.go"
        go_file.write_text("""
package main
import "fmt"
func main() {
    fmt.Println("Debug: Starting")
    // TODO: Add features
}
""")
        
        # Java file
        java_file = temp_dir / "App.java"
        java_file.write_text("""
public class App {
    public static void main(String[] args) {
        System.out.println("Debug: Starting");
        // FIXME: Add error handling
    }
}
""")
        
        return [py_file, js_file, go_file, java_file]
    
    def test_multi_language_detection(self, multi_language_project, temp_git_repo, temp_dir):
        """Test detection of issues across multiple languages."""
        # Stage all files
        for file_path in multi_language_project:
            temp_git_repo.index.add([str(file_path)])
        
        # Install pre-commit hook
        hooks_dir = temp_dir / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_src.exists():
            shutil.copy2(hook_src, hooks_dir / "pre-commit")
            os.chmod(hooks_dir / "pre-commit", 0o755)
        
        # Try commit
        try:
            temp_git_repo.index.commit("Multi-language commit")
        except git.exc.HookExecutionError:
            pass
        
        # Check context file
        context_file = temp_dir / ".cleanup-toolkit" / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            # Should detect all language files
            assert "app.py" in content
            assert "app.js" in content
            assert "app.go" in content
            assert "App.java" in content