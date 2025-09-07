"""
Performance tests for the Cleanup Toolkit.

Tests performance characteristics including:
- Large file processing
- Repository size handling
- Concurrent operations
- Memory usage
"""

import os
import time
import tempfile
import shutil
from pathlib import Path
from typing import List
import subprocess

import pytest
import git


@pytest.mark.performance
class TestPerformance:
    """Performance test suite."""
    
    @pytest.fixture
    def large_repository(self, tmp_path) -> Path:
        """Create a large test repository."""
        repo_path = tmp_path / "large_repo"
        repo_path.mkdir()
        repo = git.Repo.init(repo_path)
        
        with repo.config_writer() as config:
            config.set_value("user", "name", "Perf Test")
            config.set_value("user", "email", "perf@test.com")
        
        # Create many files
        for i in range(100):
            module_dir = repo_path / f"module_{i}"
            module_dir.mkdir()
            
            for j in range(10):
                file_path = module_dir / f"file_{j}.py"
                content = self.generate_large_file(lines=500)
                file_path.write_text(content)
        
        # Add all files
        repo.index.add(["*"])
        repo.index.commit("Initial large commit")
        
        return repo_path
    
    def generate_large_file(self, lines: int = 1000) -> str:
        """Generate a large Python file."""
        content = []
        content.append("#!/usr/bin/env python3")
        content.append("import os")
        content.append("")
        
        for i in range(lines // 10):
            content.extend([
                f"def function_{i}(x, y):",
                f"    # Function {i}",
                "    result = x + y",
                f"    print(f'Debug: function_{i} result={{result}}')",  # Debug statement
                "    return result",
                "",
                f"# TODO: Optimize function_{i}",
                ""
            ])
        
        return "\n".join(content)
    
    @pytest.mark.benchmark(group="file-processing")
    def test_large_file_processing(self, benchmark, tmp_path):
        """Test processing of large files."""
        # Create large file
        large_file = tmp_path / "large.py"
        content = self.generate_large_file(lines=10000)
        large_file.write_text(content)
        
        def process_file():
            # Simulate file processing
            with open(large_file, 'r') as f:
                lines = f.readlines()
                
            # Check for issues
            debug_count = sum(1 for line in lines if 'print(' in line)
            todo_count = sum(1 for line in lines if 'TODO' in line)
            
            return debug_count, todo_count
        
        result = benchmark(process_file)
        assert result[0] > 0  # Should find debug statements
        assert result[1] > 0  # Should find TODOs
    
    @pytest.mark.benchmark(group="repository-operations")
    def test_repository_scanning(self, benchmark, large_repository):
        """Test scanning large repository."""
        def scan_repository():
            file_count = 0
            issue_count = 0
            
            for root, dirs, files in os.walk(large_repository):
                for file in files:
                    if file.endswith('.py'):
                        file_count += 1
                        file_path = Path(root) / file
                        
                        with open(file_path, 'r') as f:
                            content = f.read()
                            if 'print(' in content:
                                issue_count += 1
            
            return file_count, issue_count
        
        result = benchmark(scan_repository)
        assert result[0] == 1000  # 100 modules * 10 files
        assert result[1] > 0  # Should find issues
    
    @pytest.mark.benchmark(group="git-operations")
    def test_git_operations_performance(self, benchmark, large_repository):
        """Test git operations on large repository."""
        repo = git.Repo(large_repository)
        
        def perform_git_operations():
            # Get status
            status = repo.git.status()
            
            # Get diff
            diff = repo.git.diff()
            
            # Get log
            log = repo.git.log('--oneline', '-10')
            
            return len(status) + len(diff) + len(log)
        
        result = benchmark(perform_git_operations)
        assert result > 0
    
    @pytest.mark.benchmark(group="hook-execution")
    def test_pre_commit_hook_performance(self, benchmark, large_repository):
        """Test pre-commit hook performance."""
        # Install hook
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if not hook_src.exists():
            pytest.skip("Pre-commit hook not found")
        
        hooks_dir = large_repository / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        hook_dst = hooks_dir / "pre-commit"
        shutil.copy2(hook_src, hook_dst)
        os.chmod(hook_dst, 0o755)
        
        # Stage some files
        repo = git.Repo(large_repository)
        test_file = large_repository / "test_new.py"
        test_file.write_text("print('test')")
        repo.index.add([str(test_file)])
        
        def execute_hook():
            env = os.environ.copy()
            env["SKIP_CLEANUP"] = "true"  # Skip to measure performance only
            
            result = subprocess.run(
                ["bash", str(hook_dst)],
                cwd=large_repository,
                env=env,
                capture_output=True,
                text=True
            )
            return result.returncode
        
        benchmark(execute_hook)
    
    @pytest.mark.slow
    def test_memory_usage_large_files(self, tmp_path):
        """Test memory usage with large files."""
        import psutil
        import gc
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create and process large files
        for i in range(10):
            large_file = tmp_path / f"large_{i}.py"
            content = self.generate_large_file(lines=10000)
            large_file.write_text(content)
            
            # Process file
            with open(large_file, 'r') as f:
                lines = f.readlines()
                # Simulate processing
                issues = [line for line in lines if 'print(' in line or 'TODO' in line]
            
            # Clean up
            del lines
            del issues
            gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 100MB)
        assert memory_increase < 100, f"Memory increased by {memory_increase:.2f} MB"
    
    @pytest.mark.benchmark(group="parallel-processing")
    def test_parallel_file_processing(self, benchmark, large_repository):
        """Test parallel processing of files."""
        import concurrent.futures
        
        def process_file(file_path):
            """Process a single file."""
            with open(file_path, 'r') as f:
                content = f.read()
            
            issues = []
            if 'print(' in content:
                issues.append('debug')
            if 'TODO' in content:
                issues.append('todo')
            
            return file_path.name, issues
        
        def parallel_processing():
            python_files = list(Path(large_repository).glob("**/*.py"))
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(process_file, python_files))
            
            return len(results)
        
        result = benchmark(parallel_processing)
        assert result == 1000  # Should process all files
    
    def test_incremental_processing(self, large_repository):
        """Test incremental processing of changes."""
        repo = git.Repo(large_repository)
        
        # Baseline: process all files
        start = time.time()
        all_files = list(Path(large_repository).glob("**/*.py"))
        baseline_time = time.time() - start
        
        # Make small change
        changed_file = all_files[0]
        content = changed_file.read_text()
        changed_file.write_text(content + "\n# Modified")
        repo.index.add([str(changed_file)])
        
        # Incremental: process only changed files
        start = time.time()
        changed = repo.index.diff("HEAD")
        incremental_time = time.time() - start
        
        # Incremental should be much faster
        assert incremental_time < baseline_time / 10
    
    @pytest.mark.benchmark(group="cleanup-operations")
    def test_cleanup_operations_performance(self, benchmark, tmp_path):
        """Test performance of cleanup operations."""
        # Create test file with issues
        test_file = tmp_path / "messy.py"
        test_file.write_text("""
import os
import sys
import unused  # unused import

DEBUG = True

def calculate(x, y):
    print(f"Debug: calculating {x} + {y}")  # debug
    result = x + y
    print(f"Result: {result}")  # debug
    return result

def calc(a, b):  # duplicate
    return a + b

# TODO: Add more functions
# FIXME: Handle errors

# Old code
# def old_func():
#     pass
""")
        
        def cleanup_file():
            content = test_file.read_text()
            lines = content.split('\n')
            
            # Remove debug statements
            lines = [l for l in lines if 'print(' not in l or 'Debug' not in l]
            
            # Remove TODO/FIXME
            lines = [l for l in lines if not any(marker in l for marker in ['TODO', 'FIXME'])]
            
            # Remove commented code
            lines = [l for l in lines if not (l.strip().startswith('#') and 'def ' in l)]
            
            cleaned = '\n'.join(lines)
            test_file.write_text(cleaned)
            
            return len(lines)
        
        result = benchmark(cleanup_file)
        assert result > 0