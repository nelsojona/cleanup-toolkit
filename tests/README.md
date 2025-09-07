# Cleanup Toolkit Test Suite

Comprehensive testing suite for the Cleanup Toolkit following the testing pyramid structure with 80% unit tests, 15% integration tests, and 5% end-to-end tests.

## 📁 Test Structure

```
tests/
├── unit/                    # Unit tests (80% of tests)
│   ├── test_pre_commit_hook.py
│   └── test_cleanup_script.py
├── integration/             # Integration tests (15% of tests)
│   └── test_git_workflows.py
├── e2e/                    # End-to-end tests (5% of tests)
│   └── test_complete_workflows.py
├── performance/            # Performance tests
│   └── test_performance.py
├── security/              # Security tests
│   └── test_security.py
├── fixtures/              # Test fixtures and data
├── utils/                 # Test utilities
│   └── test_helpers.py
├── conftest.py           # Pytest configuration
└── README.md            # This file
```

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
# Using pytest directly
pytest tests/ -v

# Using Make
make test

# With coverage
pytest tests/ --cov=. --cov-report=html
```

## 🧪 Test Categories

### Unit Tests
Fast, isolated tests for individual functions and components.

```bash
# Run unit tests only
pytest tests/unit/ -v
# or
make test-unit
```

**Coverage Areas:**
- Pre-commit hook functions
- Cleanup script utilities
- Configuration parsing
- File operations
- Issue detection

### Integration Tests
Tests for component interactions and git workflows.

```bash
# Run integration tests only
pytest tests/integration/ -v
# or
make test-integration
```

**Coverage Areas:**
- Git repository operations
- AI framework integrations (Claude, Warp)
- Multi-language support
- Branch workflows
- PR analysis

### End-to-End Tests
Complete workflow tests from installation to cleanup.

```bash
# Run E2E tests only
pytest tests/e2e/ -v
# or
make test-e2e
```

**Coverage Areas:**
- Complete installation process
- Full development workflow
- Team collaboration scenarios
- AI framework workflows

### Performance Tests
Tests for performance characteristics and benchmarks.

```bash
# Run performance tests
pytest tests/performance/ -v --benchmark-only
# or
make test-performance
```

**Coverage Areas:**
- Large file processing
- Repository scanning
- Memory usage
- Parallel processing
- Cleanup operations

### Security Tests
Tests for security vulnerabilities and safe practices.

```bash
# Run security tests
pytest tests/security/ -v
# or
make test-security
```

**Coverage Areas:**
- Path traversal prevention
- Command injection prevention
- Sensitive data detection
- Input validation
- Secure file operations

## 📊 Coverage Reports

### Generate Coverage Report

```bash
# Terminal report
pytest tests/ --cov=. --cov-report=term-missing

# HTML report
pytest tests/ --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# XML report (for CI)
pytest tests/ --cov=. --cov-report=xml
```

### Coverage Thresholds

- Overall coverage target: **80%**
- Critical paths coverage: **90%**
- Per-file minimum: **70%**

## 🏃 Running Specific Tests

### By Marker

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Slow tests
pytest -m slow

# Tests requiring git
pytest -m requires_git

# Tests requiring network
pytest -m requires_network
```

### By Pattern

```bash
# Test specific file
pytest tests/unit/test_pre_commit_hook.py

# Test specific function
pytest tests/unit/test_pre_commit_hook.py::TestPreCommitHook::test_hook_exists_and_is_executable

# Tests matching pattern
pytest -k "test_cleanup"
```

### Parallel Execution

```bash
# Run tests in parallel
pytest tests/ -n auto

# Specify number of workers
pytest tests/ -n 4
```

## 🔧 Test Utilities

The `tests/utils/test_helpers.py` module provides reusable utilities:

### Code Generation
```python
from tests.utils.test_helpers import CodeGenerator

# Generate Python file with issues
code = CodeGenerator.generate_python_file(
    issues=['debug', 'todo', 'duplicate'],
    lines=100
)
```

### Git Operations
```python
from tests.utils.test_helpers import GitTestHelper

# Create test repository
repo = GitTestHelper.create_test_repo(path, initial_files={
    'main.py': 'print("hello")'
})
```

### Issue Detection
```python
from tests.utils.test_helpers import IssueDetector

# Detect debug statements
issues = IssueDetector.detect_debug_statements(file_path)
```

## 🔍 Debugging Tests

### Verbose Output
```bash
# Show all output
pytest tests/ -vv

# Show print statements
pytest tests/ -s

# Both verbose and print
pytest tests/ -vvs
```

### Debug Failed Tests
```bash
# Drop to debugger on failure
pytest tests/ --pdb

# Drop to debugger on first failure
pytest tests/ --pdb --maxfail=1
```

### Test Logging
```bash
# Show log output
pytest tests/ --log-cli-level=DEBUG
```

## 📝 Writing New Tests

### Test Structure Template

```python
"""Test module description."""

import pytest
from pathlib import Path

@pytest.mark.unit  # or integration, e2e, etc.
class TestFeature:
    """Test suite for specific feature."""
    
    @pytest.fixture(autouse=True)
    def setup(self, temp_dir):
        """Set up test environment."""
        self.temp_dir = temp_dir
        # Additional setup
    
    def test_specific_functionality(self):
        """Test specific functionality."""
        # Arrange
        test_file = self.temp_dir / "test.py"
        test_file.write_text("content")
        
        # Act
        result = function_under_test(test_file)
        
        # Assert
        assert result == expected_value
```

### Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Use descriptive test names
3. **Speed**: Unit tests should be fast (< 100ms)
4. **Coverage**: Aim for high coverage but focus on critical paths
5. **Documentation**: Add docstrings explaining what's being tested
6. **Fixtures**: Use fixtures for common setup
7. **Markers**: Apply appropriate markers for test categorization

## 🤖 CI/CD Integration

### GitHub Actions

The test suite runs automatically on:
- Push to main/develop branches
- Pull requests
- Daily schedule (2 AM UTC)
- Manual workflow dispatch

See `.github/workflows/test.yml` for configuration.

### Local CI Simulation

```bash
# Run full CI pipeline locally
make ci
```

## 📈 Performance Benchmarks

### Run Benchmarks
```bash
# Run and save benchmarks
pytest tests/performance/ --benchmark-autosave

# Compare with previous run
pytest tests/performance/ --benchmark-compare

# Generate HTML report
pytest tests/performance/ --benchmark-histogram
```

### Benchmark Thresholds
- File processing: < 100ms per file
- Repository scanning: < 1s for 1000 files
- Hook execution: < 500ms
- Memory usage: < 100MB increase

## 🛡️ Security Testing

### Run Security Scans
```bash
# Bandit security scan
bandit -r . -f json -o security-report.json

# Safety dependency check
safety check --json

# Full security suite
make security
```

## 🧹 Cleanup

### Remove Test Artifacts
```bash
# Clean all test artifacts
make clean

# Removes:
# - Coverage reports
# - Pytest cache
# - Benchmark results
# - Temporary files
```

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://testdriven.io/blog/testing-best-practices/)
- [Python Testing 101](https://realpython.com/python-testing/)

## 🤝 Contributing

When adding new features:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain coverage above 80%
4. Add appropriate test markers
5. Update this documentation

## 📄 License

Tests are part of the Cleanup Toolkit and follow the same MIT license.