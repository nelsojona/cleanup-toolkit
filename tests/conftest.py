"""
Minimal pytest configuration for Cleanup Toolkit tests.

This module provides essential fixtures without external dependencies.
"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Generator
from unittest.mock import Mock, MagicMock

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "fixtures" / "data"
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)


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


# ==================== Basic Fixtures ====================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp(prefix="cleanup_toolkit_test_"))
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


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
    content = '''
const fs = require('fs');
const path = require('path');
const unused = require('lodash');  // unused

function calculateSum(a, b) {
    console.log(`Debug: calculating ${a} + ${b}`);  // debug statement
    const result = a + b;
    console.log(`Debug: result is ${result}`);  // debug statement
    return result;
}

function calcSum(x, y) {  // duplicate function
    return x + y;
}

// TODO: Fix this later
// FIXME: This is broken
function brokenFunction() {
    
}

if (require.main === module) {
    console.log("Running main");  // debug
    const result = calculateSum(1, 2);
}
'''
    file_path.write_text(content)
    return file_path


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing."""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = ""
    mock_result.stderr = ""
    return mock_result


@pytest.fixture
def mock_git_repo(temp_dir: Path):
    """Mock git repository without requiring GitPython."""
    # Create basic git structure
    git_dir = temp_dir / ".git"
    git_dir.mkdir()
    
    # Create hooks directory
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir()
    
    # Create config file
    config_file = git_dir / "config"
    config_content = """[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
[user]
    name = Test User
    email = test@example.com
"""
    config_file.write_text(config_content)
    
    return {
        "path": temp_dir,
        "git_dir": git_dir,
        "hooks_dir": hooks_dir
    }


@pytest.fixture
def project_root():
    """Get the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def cleanup_toolkit_files():
    """Get paths to cleanup toolkit files."""
    return {
        "pre_commit_hook": PROJECT_ROOT / "hooks" / "pre-commit",
        "install_script": PROJECT_ROOT / "install.sh",
        "cleanup_script": PROJECT_ROOT / "scripts" / "code_cleanup_gist.sh",
        "test_runner": PROJECT_ROOT / "run_tests.py"
    }


# ==================== Test Utilities ====================

def create_test_files(directory: Path, file_specs: dict) -> dict:
    """
    Create test files in the specified directory.
    
    Args:
        directory: Directory to create files in
        file_specs: Dict of {filename: content}
    
    Returns:
        Dict of {filename: Path}
    """
    created_files = {}
    for filename, content in file_specs.items():
        file_path = directory / filename
        file_path.write_text(content)
        created_files[filename] = file_path
    return created_files


def count_patterns(text: str, patterns: list) -> int:
    """Count occurrences of patterns in text."""
    count = 0
    for pattern in patterns:
        count += text.count(pattern)
    return count


def simulate_git_add(repo_path: Path, files: list) -> bool:
    """Simulate git add operation."""
    try:
        for file in files:
            file_path = repo_path / file if isinstance(file, str) else file
            if not file_path.exists():
                return False
        return True
    except Exception:
        return False


def simulate_git_commit(repo_path: Path, message: str) -> bool:
    """Simulate git commit operation."""
    try:
        git_dir = repo_path / ".git"
        return git_dir.exists()
    except Exception:
        return False