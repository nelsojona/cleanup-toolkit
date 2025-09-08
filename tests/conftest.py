"""
Pytest configuration and fixtures for Cleanup Toolkit tests.

This module provides shared fixtures, configuration, and test utilities
for all test levels (unit, integration, e2e).
"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Generator, Dict, Any, List
from unittest.mock import Mock, MagicMock
import json
import yaml

import pytest
import git
from faker import Faker
from freezegun import freeze_time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "fixtures" / "data"
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Initialize faker
fake = Faker()


# ==================== Pytest Configuration ====================

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "unit: Mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: Mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: Mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "performance: Mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "security: Mark test as a security test"
    )
    config.addinivalue_line(
        "markers", "slow: Mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_git: Test requires git repository"
    )
    config.addinivalue_line(
        "markers", "requires_network: Test requires network access"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "security" in str(item.fspath):
            item.add_marker(pytest.mark.security)


# ==================== Directory and File Fixtures ====================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp(prefix="cleanup_toolkit_test_"))
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def temp_git_repo(temp_dir: Path) -> Generator[git.Repo, None, None]:
    """Create a temporary git repository for testing."""
    # Change to temp directory to avoid path resolution issues
    original_cwd = Path.cwd()
    os.chdir(temp_dir)
    
    try:
        repo = git.Repo.init(temp_dir)
        
        # Configure git user for commits
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create initial commit using relative paths
        readme_path = temp_dir / "README.md"
        readme_path.write_text("# Test Repository\n")
        
        # Use subprocess for git operations to avoid GitPython path issues
        subprocess.run(["git", "add", "README.md"], cwd=temp_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_dir, check=True)
        
        yield repo
    finally:
        # Always return to original directory
        os.chdir(original_cwd)


@pytest.fixture
def sample_python_file(temp_dir: Path) -> Path:
    """Create a sample messy Python file for testing."""
    file_path = temp_dir / "messy_code.py"
    content = '''#!/usr/bin/env python3
import os
import sys
import json  # unused
import pandas as pd  # unused

DEBUG = True

def calculate_sum(a, b):
    print(f"Debug: calculating {a} + {b}")  # debug statement
    result = a + b
    print(f"Debug: result is {result}")  # debug statement
    return result

def calc_sum(x, y):  # duplicate function
    """Calculate sum of two numbers."""
    return x + y

# TODO: Fix this later
# FIXME: This is broken
def broken_function():
    pass

# Old code
# def old_function():
#     pass

if __name__ == "__main__":
    print("Running main")  # debug
    result = calculate_sum(1, 2)
'''
    file_path.write_text(content)
    return file_path


@pytest.fixture
def sample_javascript_file(temp_dir: Path) -> Path:
    """Create a sample messy JavaScript file for testing."""
    file_path = temp_dir / "messy_code.js"
    content = '''// Messy JavaScript file
const unused = require('unused-module');

const DEBUG = true;

function calculateSum(a, b) {
    console.log(`Debug: calculating ${a} + ${b}`); // debug statement
    const result = a + b;
    console.log(`Debug: result is ${result}`); // debug statement
    return result;
}

function calcSum(x, y) { // duplicate function
    return x + y;
}

// TODO: Fix this later
// FIXME: This is broken
function brokenFunction() {
    // Not implemented
}

// Old code
// function oldFunction() {
//     return;
// }

console.log("Script loaded"); // debug
'''
    file_path.write_text(content)
    return file_path


# ==================== Configuration Fixtures ====================

@pytest.fixture
def cleanup_config() -> Dict[str, Any]:
    """Provide default cleanup toolkit configuration."""
    return {
        "cleanup_mode": "prompt",
        "skip_cleanup": False,
        "ai_frameworks": {
            "claude": {
                "enabled": True,
                "project_files": ["claude.md", "handover.md"]
            },
            "warp": {
                "enabled": True,
                "config_dir": ".warp"
            },
            "cursor": {
                "enabled": False
            }
        },
        "cleanup_rules": {
            "remove_debug": True,
            "remove_todos": True,
            "consolidate_duplicates": True,
            "add_documentation": True,
            "check_security": True
        },
        "file_patterns": {
            "python": ["*.py"],
            "javascript": ["*.js", "*.jsx", "*.ts", "*.tsx"],
            "go": ["*.go"],
            "java": ["*.java"]
        }
    }


@pytest.fixture
def config_file(temp_dir: Path, cleanup_config: Dict[str, Any]) -> Path:
    """Create a temporary config file."""
    config_path = temp_dir / ".cleanup-toolkit" / "config.yml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(cleanup_config, f)
    
    return config_path


# ==================== Mock Fixtures ====================

@pytest.fixture
def mock_git_operations():
    """Mock git operations for testing."""
    mock = MagicMock()
    mock.get_staged_files.return_value = [
        "src/main.py",
        "src/utils.py",
        "tests/test_main.py"
    ]
    mock.get_current_branch.return_value = "feature/test-branch"
    mock.get_commit_message.return_value = "Add new feature"
    mock.get_project_root.return_value = "/project/root"
    return mock


@pytest.fixture
def mock_ai_framework():
    """Mock AI framework interactions."""
    mock = MagicMock()
    mock.generate_prompts.return_value = {
        "analysis": "Analyze the following files for cleanup...",
        "execution": "Execute cleanup on the following issues...",
        "verification": "Verify cleanup is complete..."
    }
    mock.process_cleanup.return_value = {
        "status": "success",
        "files_processed": 3,
        "issues_found": 5,
        "issues_fixed": 4
    }
    return mock


@pytest.fixture
def mock_subprocess(mocker):
    """Mock subprocess calls for shell script testing."""
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="Success",
        stderr=""
    )
    return mock_run


# ==================== Shell Script Testing Fixtures ====================

@pytest.fixture
def pre_commit_hook_path() -> Path:
    """Get the path to the pre-commit hook."""
    return PROJECT_ROOT / "hooks" / "pre-commit"


@pytest.fixture
def cleanup_script_path() -> Path:
    """Get the path to the cleanup script."""
    return PROJECT_ROOT / "scripts" / "code_cleanup_gist.sh"


@pytest.fixture
def shell_test_env(temp_dir: Path) -> Dict[str, str]:
    """Create environment variables for shell script testing."""
    return {
        "HOME": str(temp_dir),
        "GIT_DIR": str(temp_dir / ".git"),
        "GIT_WORK_TREE": str(temp_dir),
        "CLEANUP_MODE": "test",
        "SKIP_CLEANUP": "false",
        "PATH": os.environ.get("PATH", "")
    }


# ==================== Test Data Fixtures ====================

@pytest.fixture
def sample_commit_data() -> Dict[str, Any]:
    """Provide sample commit data for testing."""
    return {
        "message": "Fix: Remove debug statements and add documentation",
        "author": "Test User <test@example.com>",
        "files": [
            {"path": "src/main.py", "additions": 10, "deletions": 5},
            {"path": "src/utils.py", "additions": 20, "deletions": 15},
            {"path": "tests/test_main.py", "additions": 50, "deletions": 0}
        ],
        "stats": {
            "total": 3,
            "additions": 80,
            "deletions": 20
        }
    }


@pytest.fixture
def sample_pr_data() -> Dict[str, Any]:
    """Provide sample pull request data for testing."""
    return {
        "number": 42,
        "title": "Feature: Add cleanup toolkit integration",
        "body": "This PR adds cleanup toolkit integration...",
        "head": "feature/cleanup-integration",
        "base": "main",
        "state": "open",
        "files_changed": 5,
        "additions": 150,
        "deletions": 30
    }


@pytest.fixture
def cleanup_issues() -> List[Dict[str, Any]]:
    """Provide sample cleanup issues for testing."""
    return [
        {
            "file": "src/main.py",
            "line": 10,
            "type": "debug_statement",
            "severity": "medium",
            "message": "Remove debug print statement"
        },
        {
            "file": "src/utils.py",
            "line": 25,
            "type": "duplicate_function",
            "severity": "high",
            "message": "Duplicate function 'calculate_sum' found"
        },
        {
            "file": "src/config.py",
            "line": 5,
            "type": "unused_import",
            "severity": "low",
            "message": "Unused import 'pandas'"
        },
        {
            "file": "src/main.py",
            "line": 45,
            "type": "todo_comment",
            "severity": "low",
            "message": "TODO comment found"
        },
        {
            "file": "src/auth.py",
            "line": 15,
            "type": "hardcoded_credential",
            "severity": "critical",
            "message": "Hardcoded password detected"
        }
    ]


# ==================== Performance Testing Fixtures ====================

@pytest.fixture
def large_codebase(temp_dir: Path) -> Path:
    """Create a large codebase for performance testing."""
    # Create 100 Python files with various issues
    for i in range(100):
        file_path = temp_dir / f"module_{i}.py"
        content = f'''# Module {i}
import os
import sys
import unused_module_{i}

def function_{i}(x, y):
    print(f"Debug: function_{i} called")  # debug
    return x + y

def duplicate_function_{i}(x, y):  # duplicate
    return x + y

# TODO: Implement feature_{i}
# FIXME: Bug in module_{i}
'''
        file_path.write_text(content)
    
    return temp_dir


# ==================== Utility Fixtures ====================

@pytest.fixture
def capture_output(mocker):
    """Capture stdout and stderr for testing."""
    stdout = mocker.patch('sys.stdout', new_callable=Mock)
    stderr = mocker.patch('sys.stderr', new_callable=Mock)
    return {"stdout": stdout, "stderr": stderr}


@pytest.fixture
def frozen_time():
    """Freeze time for consistent testing."""
    with freeze_time("2024-01-15 10:30:00"):
        yield


@pytest.fixture
def mock_network_requests(mocker):
    """Mock network requests for testing."""
    import requests
    mock_get = mocker.patch.object(requests, 'get')
    mock_post = mocker.patch.object(requests, 'post')
    
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"status": "success"}
    
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id": 123}
    
    return {"get": mock_get, "post": mock_post}


# ==================== Cleanup Context Fixtures ====================

@pytest.fixture
def cleanup_context(temp_dir: Path, sample_commit_data: Dict[str, Any]) -> Path:
    """Create a cleanup context file for testing."""
    context_dir = temp_dir / ".cleanup-toolkit"
    context_dir.mkdir(parents=True, exist_ok=True)
    
    context_file = context_dir / "cleanup-context.md"
    content = f'''# Cleanup Context

## Project Information
- Project: test-project
- Branch: feature/test
- Commit: {sample_commit_data["message"]}

## Files Modified
{chr(10).join(f"- {f['path']}" for f in sample_commit_data["files"])}

## Cleanup Tasks
- Remove debug statements
- Consolidate duplicate functions
- Add documentation
'''
    context_file.write_text(content)
    return context_file


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables after each test."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)