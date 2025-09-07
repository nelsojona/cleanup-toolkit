#!/usr/bin/env python3
"""
Test runner script for Cleanup Toolkit.

This script provides a convenient way to run different test suites
with appropriate configurations and generate reports.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestRunner:
    """Test runner for Cleanup Toolkit."""
    
    def __init__(self, verbose: bool = False):
        """Initialize test runner."""
        self.verbose = verbose
        self.project_root = PROJECT_ROOT
        self.test_dir = self.project_root / "tests"
    
    def run_command(self, cmd: List[str]) -> int:
        """Run a command and return exit code."""
        if self.verbose:
            print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd=self.project_root)
        return result.returncode
    
    def run_unit_tests(self, coverage: bool = True) -> int:
        """Run unit tests."""
        print("🧪 Running unit tests...")
        cmd = ["pytest", "tests/unit", "-v"]
        
        if coverage:
            cmd.extend(["--cov=.", "--cov-report=term"])
        
        return self.run_command(cmd)
    
    def run_integration_tests(self, coverage: bool = True) -> int:
        """Run integration tests."""
        print("🔗 Running integration tests...")
        cmd = ["pytest", "tests/integration", "-v"]
        
        if coverage:
            cmd.extend(["--cov=.", "--cov-report=term"])
        
        return self.run_command(cmd)
    
    def run_e2e_tests(self, coverage: bool = True) -> int:
        """Run end-to-end tests."""
        print("🎯 Running end-to-end tests...")
        cmd = ["pytest", "tests/e2e", "-v", "--timeout=300"]
        
        if coverage:
            cmd.extend(["--cov=.", "--cov-report=term"])
        
        return self.run_command(cmd)
    
    def run_performance_tests(self) -> int:
        """Run performance tests."""
        print("⚡ Running performance tests...")
        cmd = ["pytest", "tests/performance", "-v", "--benchmark-only"]
        return self.run_command(cmd)
    
    def run_security_tests(self) -> int:
        """Run security tests."""
        print("🔒 Running security tests...")
        cmd = ["pytest", "tests/security", "-v"]
        return self.run_command(cmd)
    
    def run_all_tests(self, coverage: bool = True) -> int:
        """Run all test suites."""
        print("🚀 Running all tests...")
        cmd = ["pytest", "tests/", "-v"]
        
        if coverage:
            cmd.extend([
                "--cov=.",
                "--cov-report=term-missing",
                "--cov-report=html",
                "--cov-fail-under=80"
            ])
        
        return self.run_command(cmd)
    
    def run_fast_tests(self) -> int:
        """Run fast tests (exclude slow tests)."""
        print("⚡ Running fast tests...")
        cmd = ["pytest", "tests/", "-v", "-m", "not slow"]
        return self.run_command(cmd)
    
    def run_coverage_report(self) -> int:
        """Generate coverage report."""
        print("📊 Generating coverage report...")
        
        # Run tests with coverage
        cmd = [
            "pytest", "tests/", "-v",
            "--cov=.",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-report=xml"
        ]
        
        result = self.run_command(cmd)
        
        if result == 0:
            print("\n✅ Coverage report generated:")
            print("  - HTML: htmlcov/index.html")
            print("  - XML: coverage.xml")
            
            # Try to open HTML report
            import webbrowser
            html_report = self.project_root / "htmlcov" / "index.html"
            if html_report.exists():
                webbrowser.open(f"file://{html_report}")
        
        return result
    
    def run_linting(self) -> int:
        """Run code quality checks."""
        print("🔍 Running code quality checks...")
        
        tools = [
            (["black", "--check", "tests/"], "Black"),
            (["isort", "--check-only", "tests/"], "isort"),
            (["flake8", "tests/"], "Flake8"),
            (["pylint", "tests/", "--exit-zero"], "Pylint"),
            (["mypy", "tests/", "--ignore-missing-imports"], "MyPy"),
        ]
        
        failed = []
        for cmd, name in tools:
            print(f"  Running {name}...")
            if self.run_command(cmd) != 0:
                failed.append(name)
        
        if failed:
            print(f"\n⚠️  Some checks failed: {', '.join(failed)}")
            return 1
        
        print("\n✅ All code quality checks passed!")
        return 0
    
    def run_ci_pipeline(self) -> int:
        """Run complete CI pipeline."""
        print("🔄 Running CI pipeline...")
        
        steps = [
            ("Linting", self.run_linting),
            ("Unit Tests", self.run_unit_tests),
            ("Integration Tests", self.run_integration_tests),
            ("E2E Tests", self.run_e2e_tests),
            ("Security Tests", self.run_security_tests),
            ("Coverage Report", self.run_coverage_report),
        ]
        
        for step_name, step_func in steps:
            print(f"\n{'='*60}")
            print(f"Step: {step_name}")
            print('='*60)
            
            if step_func() != 0:
                print(f"\n❌ CI pipeline failed at: {step_name}")
                return 1
        
        print("\n✅ CI pipeline completed successfully!")
        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test runner for Cleanup Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --all              # Run all tests
  python run_tests.py --unit            # Run unit tests only
  python run_tests.py --coverage        # Generate coverage report
  python run_tests.py --ci              # Run full CI pipeline
  python run_tests.py --fast            # Run fast tests only
        """
    )
    
    # Test suite options
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--fast", action="store_true", help="Run fast tests only")
    
    # Additional options
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--lint", action="store_true", help="Run code quality checks")
    parser.add_argument("--ci", action="store_true", help="Run full CI pipeline")
    parser.add_argument("--no-cov", action="store_true", help="Disable coverage collection")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Create test runner
    runner = TestRunner(verbose=args.verbose)
    coverage = not args.no_cov
    
    # Determine what to run
    if args.ci:
        return runner.run_ci_pipeline()
    elif args.coverage:
        return runner.run_coverage_report()
    elif args.lint:
        return runner.run_linting()
    elif args.all:
        return runner.run_all_tests(coverage=coverage)
    elif args.unit:
        return runner.run_unit_tests(coverage=coverage)
    elif args.integration:
        return runner.run_integration_tests(coverage=coverage)
    elif args.e2e:
        return runner.run_e2e_tests(coverage=coverage)
    elif args.performance:
        return runner.run_performance_tests()
    elif args.security:
        return runner.run_security_tests()
    elif args.fast:
        return runner.run_fast_tests()
    else:
        # Default: run all tests
        print("No specific test suite selected. Running all tests...")
        return runner.run_all_tests(coverage=coverage)


if __name__ == "__main__":
    sys.exit(main())