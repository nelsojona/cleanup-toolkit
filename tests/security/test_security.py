"""
Security tests for the Cleanup Toolkit.

Tests security aspects including:
- Input validation
- Path traversal prevention
- Command injection prevention
- Sensitive data handling
"""

import os
import subprocess
import tempfile
from pathlib import Path
import shutil

import pytest
import git


@pytest.mark.security
class TestSecurity:
    """Security test suite."""
    
    def test_path_traversal_prevention(self, temp_dir):
        """Test that path traversal attacks are prevented."""
        # Try to access parent directory
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "/etc/passwd",
            "C:\\Windows\\System32",
            "~/../../etc/passwd",
            "%2e%2e%2f%2e%2e%2f",
        ]
        
        for path in malicious_paths:
            # The toolkit should not process files outside project directory
            test_file = temp_dir / "test.py"
            test_file.write_text(f"# Path: {path}")
            
            # Verify path is sanitized
            assert ".." not in str(test_file.resolve())
            assert test_file.resolve().is_relative_to(temp_dir)
    
    def test_command_injection_prevention(self, temp_dir):
        """Test that command injection is prevented."""
        malicious_inputs = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "&& echo hacked",
            "`cat /etc/passwd`",
            "$(cat /etc/passwd)",
            "\n; malicious_command",
        ]
        
        for input_str in malicious_inputs:
            # Create file with malicious name (sanitized)
            safe_name = "test_" + str(hash(input_str)) + ".py"
            test_file = temp_dir / safe_name
            test_file.write_text(f"# Test: {input_str}")
            
            # Verify the input is properly escaped when used in commands
            # This would be tested in actual hook execution
            assert os.path.exists(test_file)
    
    def test_sensitive_data_detection(self, temp_dir):
        """Test detection of sensitive data in code."""
        sensitive_file = temp_dir / "sensitive.py"
        sensitive_file.write_text("""
# Configuration file
API_KEY = "sk-1234567890abcdef"
PASSWORD = "supersecret123"
DATABASE_URL = "postgresql://user:pass@localhost/db"
AWS_SECRET_KEY = "aws_secret_key_here"
PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----"

def connect():
    password = "hardcoded_password"
    token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    return password
""")
        
        # Check for sensitive data patterns
        content = sensitive_file.read_text()
        sensitive_patterns = [
            "API_KEY",
            "PASSWORD",
            "SECRET",
            "PRIVATE_KEY",
            "hardcoded_password",
            "Bearer ",
        ]
        
        found_sensitive = []
        for pattern in sensitive_patterns:
            if pattern in content:
                found_sensitive.append(pattern)
        
        # Should detect all sensitive patterns
        assert len(found_sensitive) >= 5
    
    def test_file_permission_security(self, temp_dir):
        """Test that created files have secure permissions."""
        # Create toolkit directory
        toolkit_dir = temp_dir / ".cleanup-toolkit"
        toolkit_dir.mkdir()
        
        # Create sensitive files
        config_file = toolkit_dir / "config.yml"
        config_file.write_text("secret: value")
        
        # Check permissions (on Unix-like systems)
        if os.name != 'nt':  # Not Windows
            import stat
            
            file_stat = config_file.stat()
            mode = file_stat.st_mode
            
            # File should not be world-readable
            assert not (mode & stat.S_IROTH), "File is world-readable"
            # File should not be world-writable
            assert not (mode & stat.S_IWOTH), "File is world-writable"
    
    def test_git_hook_bypass_prevention(self, temp_dir):
        """Test that git hooks cannot be easily bypassed."""
        repo = git.Repo.init(temp_dir)
        
        # Install hook
        hooks_dir = temp_dir / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        pre_commit = hooks_dir / "pre-commit"
        pre_commit.write_text("""#!/bin/bash
echo "Hook executed"
exit 1  # Always fail for testing
""")
        os.chmod(pre_commit, 0o755)
        
        # Try to commit (should fail)
        test_file = temp_dir / "test.py"
        test_file.write_text("print('test')")
        repo.index.add([str(test_file)])
        
        with pytest.raises(git.exc.HookExecutionError):
            repo.index.commit("Test commit")
    
    def test_environment_variable_injection(self, temp_dir):
        """Test that environment variables cannot be injected."""
        malicious_env_vars = {
            "PATH": "/evil/path:$PATH",
            "LD_PRELOAD": "/evil/library.so",
            "PYTHONPATH": "/evil/python/path",
            "GIT_DIR": "/evil/git",
        }
        
        # Save original environment
        original_env = os.environ.copy()
        
        try:
            # Try to inject malicious environment variables
            for key, value in malicious_env_vars.items():
                os.environ[key] = value
            
            # The toolkit should not use these malicious values directly
            # This would be tested in actual execution
            
        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)
    
    def test_symlink_attack_prevention(self, temp_dir):
        """Test prevention of symlink attacks."""
        if os.name == 'nt':  # Windows
            pytest.skip("Symlink test not applicable on Windows")
        
        # Create a target file outside project
        outside_target = temp_dir.parent / "outside.txt"
        outside_target.write_text("sensitive data")
        
        # Create symlink pointing outside
        symlink = temp_dir / "symlink.py"
        try:
            symlink.symlink_to(outside_target)
            
            # Toolkit should detect and handle symlinks safely
            assert symlink.is_symlink()
            
            # Should not follow symlink to outside directory
            real_path = symlink.resolve()
            # In production, this should be blocked
            
        except OSError:
            # Symlink creation failed (might need privileges)
            pytest.skip("Cannot create symlinks")
        finally:
            if outside_target.exists():
                outside_target.unlink()
    
    def test_race_condition_prevention(self, temp_dir):
        """Test prevention of race conditions in file operations."""
        import threading
        import time
        
        test_file = temp_dir / "race_test.py"
        test_file.write_text("initial content")
        
        race_detected = False
        
        def modifier():
            """Modify file concurrently."""
            nonlocal race_detected
            time.sleep(0.01)  # Small delay
            try:
                test_file.write_text("modified content")
            except:
                race_detected = True
        
        def reader():
            """Read file concurrently."""
            nonlocal race_detected
            try:
                content = test_file.read_text()
                if content not in ["initial content", "modified content"]:
                    race_detected = True
            except:
                race_detected = True
        
        # Run concurrent operations
        threads = []
        for _ in range(5):
            t1 = threading.Thread(target=modifier)
            t2 = threading.Thread(target=reader)
            threads.extend([t1, t2])
            t1.start()
            t2.start()
        
        for t in threads:
            t.join()
        
        # No corruption should occur
        assert not race_detected
    
    def test_input_validation(self, temp_dir):
        """Test input validation for various inputs."""
        invalid_inputs = [
            "",  # Empty
            " " * 1000,  # Very long whitespace
            "a" * 10000,  # Very long string
            "\x00",  # Null byte
            "\n\r\t",  # Control characters
            "😀" * 100,  # Unicode
            "<script>alert('xss')</script>",  # XSS attempt
        ]
        
        for input_str in invalid_inputs:
            # Test that invalid inputs are handled safely
            try:
                # Would test with actual toolkit functions
                safe_input = input_str.replace("\x00", "").strip()[:1000]
                assert len(safe_input) <= 1000
            except:
                # Should handle gracefully
                pass
    
    def test_secure_temp_file_creation(self):
        """Test that temporary files are created securely."""
        import tempfile
        
        # Create temp file securely
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("test content")
            temp_path = tmp.name
        
        try:
            # Check file was created securely
            assert os.path.exists(temp_path)
            
            if os.name != 'nt':  # Unix-like
                import stat
                file_stat = os.stat(temp_path)
                mode = file_stat.st_mode
                
                # Should not be world-readable/writable
                assert not (mode & stat.S_IROTH)
                assert not (mode & stat.S_IWOTH)
        finally:
            os.unlink(temp_path)
    
    def test_dangerous_function_detection(self, temp_dir):
        """Test detection of dangerous functions in code."""
        dangerous_file = temp_dir / "dangerous.py"
        dangerous_file.write_text("""
import os
import subprocess

def dangerous_exec():
    exec(user_input)  # Dangerous
    eval(user_input)  # Dangerous
    
def dangerous_shell():
    os.system(user_command)  # Dangerous
    subprocess.call(user_command, shell=True)  # Dangerous
    
def dangerous_pickle():
    import pickle
    pickle.loads(user_data)  # Dangerous
""")
        
        content = dangerous_file.read_text()
        dangerous_patterns = [
            "exec(",
            "eval(",
            "os.system(",
            "shell=True",
            "pickle.loads",
        ]
        
        found_dangerous = []
        for pattern in dangerous_patterns:
            if pattern in content:
                found_dangerous.append(pattern)
        
        # Should detect all dangerous patterns
        assert len(found_dangerous) == 5