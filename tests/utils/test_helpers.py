"""
Test utility functions and helpers for the Cleanup Toolkit test suite.

This module provides reusable utilities for:
- File generation and manipulation
- Git repository setup and operations
- Code issue injection and detection
- Test data generation
- Assertion helpers
"""

import os
import random
import string
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import yaml

import git
from faker import Faker

fake = Faker()


# ==================== File Generation Utilities ====================

class CodeGenerator:
    """Generate code files with various issues for testing."""
    
    @staticmethod
    def generate_python_file(
        issues: List[str] = None,
        lines: int = 50,
        include_imports: bool = True,
        include_classes: bool = True,
        include_functions: bool = True
    ) -> str:
        """
        Generate Python code with specified issues.
        
        Args:
            issues: List of issues to include ('debug', 'todo', 'duplicate', 'unused', 'security')
            lines: Approximate number of lines to generate
            include_imports: Whether to include import statements
            include_classes: Whether to include class definitions
            include_functions: Whether to include function definitions
            
        Returns:
            Generated Python code as string
        """
        issues = issues or []
        code_lines = []
        
        # Add imports
        if include_imports:
            code_lines.extend([
                "#!/usr/bin/env python3",
                "import os",
                "import sys",
            ])
            
            if "unused" in issues:
                code_lines.extend([
                    "import pandas as pd  # unused",
                    "import numpy as np  # unused",
                ])
            
            code_lines.append("")
        
        # Add debug flag if needed
        if "debug" in issues:
            code_lines.extend([
                "DEBUG = True",
                ""
            ])
        
        # Add functions
        if include_functions:
            func_name = fake.word()
            code_lines.extend([
                f"def {func_name}(x, y):",
            ])
            
            if "debug" in issues:
                code_lines.append(f'    print(f"Debug: {func_name} called with {{x}}, {{y}}")')
            
            if "todo" in issues:
                code_lines.append("    # TODO: Add validation")
            
            if "security" in issues:
                code_lines.append('    password = "hardcoded123"  # Security issue!')
            
            code_lines.extend([
                "    result = x + y",
                "    return result",
                ""
            ])
            
            # Add duplicate function
            if "duplicate" in issues:
                code_lines.extend([
                    f"def {func_name}_v2(a, b):  # Duplicate function",
                    "    return a + b",
                    ""
                ])
        
        # Add class
        if include_classes:
            class_name = fake.word().capitalize()
            code_lines.extend([
                f"class {class_name}:",
                "    def __init__(self):",
            ])
            
            if "debug" in issues:
                code_lines.append(f'        print("Debug: {class_name} initialized")')
            
            code_lines.extend([
                "        self.data = {}",
                "",
                "    def process(self, item):",
            ])
            
            if "fixme" in issues:
                code_lines.append("        # FIXME: This is broken")
            
            code_lines.extend([
                "        self.data[item] = True",
                "        return self.data",
                ""
            ])
        
        # Add commented old code
        if "commented" in issues:
            code_lines.extend([
                "# Old implementation",
                "# def old_function():",
                "#     pass",
                ""
            ])
        
        # Pad to desired line count
        while len(code_lines) < lines:
            code_lines.append("")
        
        return "\n".join(code_lines)
    
    @staticmethod
    def generate_javascript_file(
        issues: List[str] = None,
        lines: int = 50
    ) -> str:
        """Generate JavaScript code with specified issues."""
        issues = issues or []
        code_lines = []
        
        # Add requires
        code_lines.extend([
            "const express = require('express');",
        ])
        
        if "unused" in issues:
            code_lines.append("const unused = require('unused-module');  // unused")
        
        code_lines.append("")
        
        # Add function
        func_name = fake.word()
        code_lines.extend([
            f"function {func_name}(x, y) {{",
        ])
        
        if "debug" in issues:
            code_lines.append(f'    console.log(`Debug: {func_name} called with ${{x}}, ${{y}}`);')
        
        if "todo" in issues:
            code_lines.append("    // TODO: Add validation")
        
        code_lines.extend([
            "    const result = x + y;",
            "    return result;",
            "}",
            ""
        ])
        
        # Add duplicate if requested
        if "duplicate" in issues:
            code_lines.extend([
                f"function {func_name}V2(a, b) {{  // Duplicate",
                "    return a + b;",
                "}",
                ""
            ])
        
        return "\n".join(code_lines)
    
    @staticmethod
    def inject_issues(code: str, issues: List[str]) -> str:
        """
        Inject specific issues into existing code.
        
        Args:
            code: Original code
            issues: List of issues to inject
            
        Returns:
            Modified code with issues
        """
        lines = code.split("\n")
        
        for issue in issues:
            if issue == "debug":
                # Add debug statements
                for i, line in enumerate(lines):
                    if "def " in line or "function " in line:
                        indent = len(line) - len(line.lstrip())
                        debug_line = " " * (indent + 4) + 'print("Debug: Entering function")'
                        lines.insert(i + 1, debug_line)
                        break
            
            elif issue == "todo":
                # Add TODO comments
                lines.insert(5, "# TODO: Refactor this code")
            
            elif issue == "fixme":
                # Add FIXME comments
                lines.insert(10, "# FIXME: This needs attention")
        
        return "\n".join(lines)


# ==================== Git Repository Utilities ====================

class GitTestHelper:
    """Helper functions for git repository testing."""
    
    @staticmethod
    def create_test_repo(path: Path, initial_files: Dict[str, str] = None) -> git.Repo:
        """
        Create a test git repository with initial files.
        
        Args:
            path: Directory path for the repository
            initial_files: Dictionary of filename: content pairs
            
        Returns:
            Initialized git repository
        """
        repo = git.Repo.init(path)
        
        # Configure git user
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create initial files
        if initial_files:
            for filename, content in initial_files.items():
                file_path = path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content)
                repo.index.add([str(file_path)])
        else:
            # Create default README
            readme = path / "README.md"
            readme.write_text("# Test Repository\n")
            repo.index.add([str(readme)])
        
        # Make initial commit
        repo.index.commit("Initial commit")
        
        return repo
    
    @staticmethod
    def create_branch_with_changes(
        repo: git.Repo,
        branch_name: str,
        changes: Dict[str, str]
    ) -> git.Head:
        """
        Create a new branch with specified file changes.
        
        Args:
            repo: Git repository
            branch_name: Name of the new branch
            changes: Dictionary of filename: content pairs
            
        Returns:
            Created branch reference
        """
        branch = repo.create_head(branch_name)
        branch.checkout()
        
        for filename, content in changes.items():
            file_path = Path(repo.working_dir) / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            repo.index.add([str(file_path)])
        
        repo.index.commit(f"Changes in {branch_name}")
        
        return branch
    
    @staticmethod
    def simulate_merge_conflict(
        repo: git.Repo,
        file_path: str,
        branch1_content: str,
        branch2_content: str
    ) -> bool:
        """
        Simulate a merge conflict between two branches.
        
        Args:
            repo: Git repository
            file_path: Path to the conflicting file
            branch1_content: Content for branch 1
            branch2_content: Content for branch 2
            
        Returns:
            True if conflict was created successfully
        """
        main_branch = repo.heads.main or repo.heads.master
        
        # Create branch 1
        branch1 = repo.create_head("conflict-branch-1")
        branch1.checkout()
        
        conflict_file = Path(repo.working_dir) / file_path
        conflict_file.write_text(branch1_content)
        repo.index.add([file_path])
        repo.index.commit("Branch 1 changes")
        
        # Switch to main and create branch 2
        main_branch.checkout()
        branch2 = repo.create_head("conflict-branch-2")
        branch2.checkout()
        
        conflict_file.write_text(branch2_content)
        repo.index.add([file_path])
        repo.index.commit("Branch 2 changes")
        
        # Try to merge branch 1
        try:
            repo.git.merge("conflict-branch-1")
            return False  # No conflict
        except git.exc.GitCommandError:
            return True  # Conflict created


# ==================== Issue Detection Utilities ====================

class IssueDetector:
    """Detect various code issues in files."""
    
    @staticmethod
    def detect_debug_statements(file_path: Path) -> List[Tuple[int, str]]:
        """
        Detect debug statements in a file.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            List of (line_number, line_content) tuples
        """
        debug_patterns = [
            "print(",
            "console.log(",
            "System.out.println(",
            "fmt.Println(",
            "Debug:",
            "DEBUG"
        ]
        
        issues = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                for pattern in debug_patterns:
                    if pattern in line:
                        issues.append((i, line.strip()))
                        break
        
        return issues
    
    @staticmethod
    def detect_todos(file_path: Path) -> List[Tuple[int, str]]:
        """Detect TODO/FIXME comments."""
        todo_patterns = ["TODO", "FIXME", "XXX", "HACK"]
        
        issues = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                for pattern in todo_patterns:
                    if pattern in line:
                        issues.append((i, line.strip()))
                        break
        
        return issues
    
    @staticmethod
    def detect_duplicate_functions(file_path: Path) -> List[str]:
        """Detect potential duplicate functions."""
        # Simple detection based on function signatures
        if file_path.suffix == '.py':
            pattern = r'^def\s+(\w+)'
        elif file_path.suffix in ['.js', '.ts']:
            pattern = r'^function\s+(\w+)'
        else:
            return []
        
        import re
        functions = []
        duplicates = []
        seen = set()
        
        with open(file_path, 'r') as f:
            for line in f:
                match = re.match(pattern, line.strip())
                if match:
                    func_name = match.group(1)
                    # Check for similar names (potential duplicates)
                    base_name = func_name.rstrip('_v2').rstrip('V2').rstrip('2')
                    if base_name in seen:
                        duplicates.append(func_name)
                    seen.add(base_name)
                    functions.append(func_name)
        
        return duplicates


# ==================== Test Data Generation ====================

class TestDataGenerator:
    """Generate test data for various scenarios."""
    
    @staticmethod
    def generate_commit_history(repo: git.Repo, count: int = 10) -> List[str]:
        """
        Generate a series of commits with various changes.
        
        Args:
            repo: Git repository
            count: Number of commits to generate
            
        Returns:
            List of commit SHAs
        """
        commits = []
        
        for i in range(count):
            # Create or modify a file
            file_name = f"file_{i % 3}.txt"
            file_path = Path(repo.working_dir) / file_name
            
            content = f"Content for commit {i}\n"
            content += f"Timestamp: {datetime.now()}\n"
            content += f"Random: {fake.text()}\n"
            
            file_path.write_text(content)
            repo.index.add([file_name])
            
            commit = repo.index.commit(f"Commit {i}: {fake.sentence()}")
            commits.append(commit.hexsha)
        
        return commits
    
    @staticmethod
    def generate_pr_data() -> Dict[str, Any]:
        """Generate realistic PR data for testing."""
        return {
            "number": random.randint(1, 1000),
            "title": f"Feature: {fake.sentence()}",
            "body": fake.paragraph(),
            "state": random.choice(["open", "closed", "merged"]),
            "created_at": fake.date_time().isoformat(),
            "updated_at": fake.date_time().isoformat(),
            "head": {
                "ref": f"feature/{fake.word()}",
                "sha": fake.sha1()
            },
            "base": {
                "ref": "main",
                "sha": fake.sha1()
            },
            "files_changed": random.randint(1, 20),
            "additions": random.randint(10, 500),
            "deletions": random.randint(5, 200),
            "commits": random.randint(1, 15)
        }
    
    @staticmethod
    def generate_cleanup_report() -> str:
        """Generate a sample cleanup report."""
        return f"""# Cleanup Report
Generated: {datetime.now().isoformat()}

## Files Analyzed
- src/main.py
- src/utils.py
- tests/test_main.py

## Issues Found
### Debug Statements
- main.py:15 - print("Debug: Processing")
- utils.py:23 - console.log("Debug output")

### TODO Comments
- main.py:45 - # TODO: Add error handling
- test_main.py:10 - # FIXME: Mock this properly

### Duplicate Functions
- utils.py: validate_input() and validate_data() appear to be duplicates

### Security Issues
- main.py:67 - Hardcoded password detected

## Recommendations
1. Remove all debug statements before committing
2. Address TODO/FIXME comments or create issues
3. Consolidate duplicate functions
4. Move credentials to environment variables
"""


# ==================== Assertion Helpers ====================

class AssertionHelpers:
    """Custom assertion helpers for cleanup toolkit tests."""
    
    @staticmethod
    def assert_file_contains(file_path: Path, expected_content: List[str]):
        """
        Assert that a file contains all expected content.
        
        Args:
            file_path: Path to the file
            expected_content: List of strings that should be in the file
        """
        assert file_path.exists(), f"File {file_path} does not exist"
        
        content = file_path.read_text()
        for expected in expected_content:
            assert expected in content, f"Expected '{expected}' not found in {file_path}"
    
    @staticmethod
    def assert_cleanup_context_valid(context_file: Path):
        """Assert that a cleanup context file is valid."""
        assert context_file.exists(), "Cleanup context file does not exist"
        
        content = context_file.read_text()
        
        # Check required sections
        required_sections = [
            "# Cleanup Context",
            "## Project Information",
            "## Files Modified",
            "## Cleanup Request"
        ]
        
        for section in required_sections:
            assert section in content, f"Missing section: {section}"
    
    @staticmethod
    def assert_hook_executed(repo_path: Path):
        """Assert that the pre-commit hook was executed."""
        toolkit_dir = repo_path / ".cleanup-toolkit"
        assert toolkit_dir.exists(), "Toolkit directory not created"
        
        # Check for at least one generated file
        generated_files = list(toolkit_dir.glob("*.md")) + list(toolkit_dir.glob("*.txt"))
        assert len(generated_files) > 0, "No cleanup files generated"


# ==================== Environment Setup Utilities ====================

class EnvironmentSetup:
    """Set up test environments for different scenarios."""
    
    @staticmethod
    def setup_claude_environment(project_dir: Path) -> None:
        """Set up Claude Code environment."""
        # Create Claude project files
        claude_md = project_dir / "claude.md"
        claude_md.write_text("""# Claude Code Project

## Standards
- No debug statements
- Comprehensive documentation
- Type hints required
""")
        
        handover_md = project_dir / "handover.md"
        handover_md.write_text("""# Handover

## Tasks
- [ ] Implement feature
- [ ] Clean up code
""")
    
    @staticmethod
    def setup_warp_environment(project_dir: Path) -> None:
        """Set up Warp Terminal environment."""
        warp_dir = project_dir / ".warp"
        warp_dir.mkdir()
        
        workflows_dir = warp_dir / "workflows"
        workflows_dir.mkdir()
        
        cleanup_workflow = workflows_dir / "cleanup.yaml"
        cleanup_workflow.write_text("""
name: cleanup
commands:
  - grep -r "console.log" .
  - grep -r "TODO" .
""")
    
    @staticmethod
    def setup_team_environment(project_dir: Path, team_size: int = 3) -> None:
        """Set up team collaboration environment."""
        # Create team configuration
        team_config = project_dir / ".cleanup-toolkit" / "team.yml"
        team_config.parent.mkdir(exist_ok=True)
        
        team_data = {
            "team": {
                "name": "Test Team",
                "members": [f"dev{i}@example.com" for i in range(team_size)]
            },
            "standards": {
                "require_cleanup": True,
                "auto_assign": True,
                "review_required": True
            }
        }
        
        with open(team_config, 'w') as f:
            yaml.dump(team_data, f)


# ==================== Mock Helpers ====================

class MockHelpers:
    """Helpers for creating mock objects."""
    
    @staticmethod
    def mock_github_api_response(endpoint: str) -> Dict[str, Any]:
        """Create mock GitHub API responses."""
        if "pulls" in endpoint:
            return {
                "number": 42,
                "title": "Test PR",
                "state": "open",
                "files": ["file1.py", "file2.js"]
            }
        elif "commits" in endpoint:
            return {
                "sha": fake.sha1(),
                "message": "Test commit",
                "author": {"name": "Test User", "email": "test@example.com"}
            }
        else:
            return {"status": "success"}
    
    @staticmethod
    def mock_shell_command(command: str) -> Tuple[int, str, str]:
        """
        Mock shell command execution.
        
        Args:
            command: Shell command to mock
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        if "git status" in command:
            return (0, "On branch main\nnothing to commit", "")
        elif "git diff" in command:
            return (0, "diff --git a/file.py b/file.py", "")
        elif "gh pr" in command:
            return (0, json.dumps([{"number": 1}]), "")
        else:
            return (0, "Success", "")


# ==================== Performance Testing Utilities ====================

class PerformanceTestHelper:
    """Utilities for performance testing."""
    
    @staticmethod
    def generate_large_codebase(
        base_dir: Path,
        num_files: int = 1000,
        lines_per_file: int = 100
    ) -> Path:
        """
        Generate a large codebase for performance testing.
        
        Args:
            base_dir: Base directory for the codebase
            num_files: Number of files to generate
            lines_per_file: Lines per file
            
        Returns:
            Path to the generated codebase
        """
        codebase_dir = base_dir / "large_codebase"
        codebase_dir.mkdir(exist_ok=True)
        
        code_gen = CodeGenerator()
        
        for i in range(num_files):
            # Create directory structure
            module_dir = codebase_dir / f"module_{i % 10}"
            module_dir.mkdir(exist_ok=True)
            
            # Generate file with random issues
            issues = random.sample(
                ['debug', 'todo', 'duplicate', 'unused'],
                k=random.randint(0, 3)
            )
            
            code = code_gen.generate_python_file(
                issues=issues,
                lines=lines_per_file
            )
            
            file_path = module_dir / f"file_{i}.py"
            file_path.write_text(code)
        
        return codebase_dir
    
    @staticmethod
    def measure_execution_time(func, *args, **kwargs) -> float:
        """
        Measure execution time of a function.
        
        Args:
            func: Function to measure
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Execution time in seconds
        """
        import time
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        return end - start