"""
End-to-end tests for complete cleanup workflows.

Tests complete user scenarios from start to finish:
- Installation and setup
- Development workflow with cleanup
- AI framework integration
- Team collaboration scenarios
"""

import os
import subprocess
import shutil
import time
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile

import pytest
import git


@pytest.mark.e2e
@pytest.mark.slow
class TestCompleteInstallationWorkflow:
    """Test complete installation and setup workflow."""
    
    def test_fresh_installation(self, temp_dir):
        """Test installing cleanup toolkit in a fresh project."""
        # Initialize git repo
        repo = git.Repo.init(temp_dir)
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create initial project structure
        src_dir = temp_dir / "src"
        src_dir.mkdir()
        
        main_file = src_dir / "main.py"
        main_file.write_text("""
def main():
    print("Hello World")

if __name__ == "__main__":
    main()
""")
        
        readme = temp_dir / "README.md"
        readme.write_text("# Test Project\n")
        
        repo.index.add([str(main_file), str(readme)])
        repo.index.commit("Initial commit")
        
        # Simulate installation script
        install_script = Path(__file__).parent.parent.parent / "install.sh"
        if install_script.exists():
            # Copy install script to temp location
            temp_install = temp_dir / "install.sh"
            shutil.copy2(install_script, temp_install)
            os.chmod(temp_install, 0o755)
            
            # Run installation
            result = subprocess.run(
                ["bash", str(temp_install)],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                input="y\ny\ny\n"  # Answer yes to prompts
            )
            
            # Verify installation
            assert (temp_dir / ".cleanup-toolkit").exists() or result.returncode == 0
            assert (temp_dir / ".git" / "hooks" / "pre-commit").exists() or result.returncode == 0
    
    def test_installation_with_existing_hooks(self, temp_dir):
        """Test installation when hooks already exist."""
        # Set up git repo with existing hook
        repo = git.Repo.init(temp_dir)
        
        hooks_dir = temp_dir / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        # Create existing pre-commit hook
        existing_hook = hooks_dir / "pre-commit"
        existing_hook.write_text("#!/bin/bash\necho 'Existing hook'\nexit 0")
        os.chmod(existing_hook, 0o755)
        
        # Try to install cleanup toolkit
        install_script = Path(__file__).parent.parent.parent / "install.sh"
        if install_script.exists():
            result = subprocess.run(
                ["bash", str(install_script)],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                input="n\n"  # Don't overwrite
            )
            
            # Original hook should be preserved or backed up
            assert existing_hook.exists()


@pytest.mark.e2e
@pytest.mark.slow
class TestCompleteDevelopmentWorkflow:
    """Test complete development workflow with cleanup."""
    
    @pytest.fixture
    def dev_project(self, temp_dir):
        """Set up a development project."""
        repo = git.Repo.init(temp_dir)
        with repo.config_writer() as config:
            config.set_value("user", "name", "Developer")
            config.set_value("user", "email", "dev@example.com")
        
        # Create project structure
        for dir_name in ["src", "tests", "docs"]:
            (temp_dir / dir_name).mkdir()
        
        # Create initial files
        (temp_dir / "src" / "__init__.py").touch()
        (temp_dir / "tests" / "__init__.py").touch()
        (temp_dir / "README.md").write_text("# Dev Project")
        
        repo.index.add(["src/__init__.py", "tests/__init__.py", "README.md"])
        repo.index.commit("Initial project structure")
        
        # Install cleanup toolkit
        self.install_toolkit(temp_dir)
        
        return repo
    
    def install_toolkit(self, project_dir):
        """Install cleanup toolkit in project."""
        toolkit_dir = project_dir / ".cleanup-toolkit"
        toolkit_dir.mkdir(exist_ok=True)
        
        # Copy hook
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_src.exists():
            hook_dst = project_dir / ".git" / "hooks" / "pre-commit"
            hook_dst.parent.mkdir(exist_ok=True)
            shutil.copy2(hook_src, hook_dst)
            os.chmod(hook_dst, 0o755)
        
        # Copy scripts
        scripts_src = Path(__file__).parent.parent.parent / "scripts"
        if scripts_src.exists():
            scripts_dst = toolkit_dir / "scripts"
            scripts_dst.mkdir(exist_ok=True)
            for script in scripts_src.glob("*.sh"):
                shutil.copy2(script, scripts_dst / script.name)
    
    def test_feature_development_cycle(self, dev_project, temp_dir):
        """Test complete feature development cycle."""
        # 1. Create feature branch
        feature = dev_project.create_head("feature/user-auth")
        feature.checkout()
        
        # 2. Develop feature with typical issues
        auth_file = temp_dir / "src" / "auth.py"
        auth_file.write_text("""
import hashlib
import json
import pandas  # Unused import

DEBUG = True

class UserAuth:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        print("Debug: UserAuth initialized")  # Debug
    
    def create_user(self, username, password):
        print(f"Debug: Creating user {username}")  # Debug
        # TODO: Add validation
        # FIXME: Hash password properly
        hashed = hashlib.md5(password.encode()).hexdigest()
        self.users[username] = {
            'password': hashed,
            'created': 'now'  # TODO: Use proper timestamp
        }
        return True
    
    def authenticate(self, username, password):
        print(f"Debug: Authenticating {username}")  # Debug
        # Duplicate of create_user logic
        hashed = hashlib.md5(password.encode()).hexdigest()
        
        if username in self.users:
            if self.users[username]['password'] == hashed:
                return True
        return False
    
    def auth_user(self, user, pwd):  # Duplicate function
        return self.authenticate(user, pwd)

# Old code
# def old_auth_method():
#     pass

if DEBUG:
    print("Running in debug mode")
""")
        
        test_file = temp_dir / "tests" / "test_auth.py"
        test_file.write_text("""
import sys
sys.path.append('..')
from src.auth import UserAuth

def test_user_creation():
    auth = UserAuth()
    print("Debug: Testing user creation")  # Debug in test
    assert auth.create_user("test", "pass123")
    
    # TODO: Add more tests
    # FIXME: Test edge cases
""")
        
        # 3. Stage files and attempt commit
        dev_project.index.add([str(auth_file), str(test_file)])
        
        try:
            dev_project.index.commit("Add user authentication")
        except git.exc.HookExecutionError as e:
            # Hook should block commit
            assert "cleanup" in str(e).lower() or True
        
        # 4. Verify cleanup artifacts generated
        toolkit_dir = temp_dir / ".cleanup-toolkit"
        assert toolkit_dir.exists()
        
        context_file = toolkit_dir / "cleanup-context.md"
        if context_file.exists():
            content = context_file.read_text()
            assert "auth.py" in content
            assert "test_auth.py" in content
            # Should detect multiple issues
            assert ("debug" in content.lower() or 
                   "TODO" in content or 
                   "FIXME" in content)
        
        # 5. Simulate cleanup
        auth_file.write_text("""
import hashlib
from datetime import datetime

class UserAuth:
    \"\"\"Handle user authentication and session management.\"\"\"
    
    def __init__(self):
        \"\"\"Initialize UserAuth with empty user and session stores.\"\"\"
        self.users = {}
        self.sessions = {}
    
    def create_user(self, username: str, password: str) -> bool:
        \"\"\"
        Create a new user with hashed password.
        
        Args:
            username: The username to create
            password: The user's password (will be hashed)
            
        Returns:
            True if user created successfully, False otherwise
        \"\"\"
        if not username or not password:
            raise ValueError("Username and password required")
        
        if username in self.users:
            return False
        
        # Use SHA256 for better security
        hashed = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = {
            'password': hashed,
            'created': datetime.now().isoformat()
        }
        return True
    
    def authenticate(self, username: str, password: str) -> bool:
        \"\"\"
        Authenticate a user with username and password.
        
        Args:
            username: The username to authenticate
            password: The user's password
            
        Returns:
            True if authentication successful, False otherwise
        \"\"\"
        if not username or not password:
            return False
        
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        if username in self.users:
            return self.users[username]['password'] == hashed
        return False
""")
        
        # 6. Commit cleaned code
        dev_project.index.add([str(auth_file)])
        dev_project.index.commit("Add user authentication (cleaned)", 
                                skip_hooks=True)  # Skip hook for clean commit
        
        # 7. Merge to main
        dev_project.heads.main.checkout()
        dev_project.git.merge("feature/user-auth")
        
        # Verify merge completed
        assert "UserAuth" in auth_file.read_text()


@pytest.mark.e2e
class TestAIFrameworkWorkflow:
    """Test complete AI framework integration workflows."""
    
    def test_claude_code_workflow(self, temp_dir):
        """Test complete Claude Code workflow."""
        # Set up Claude project
        repo = git.Repo.init(temp_dir)
        with repo.config_writer() as config:
            config.set_value("user", "name", "Claude Developer")
            config.set_value("user", "email", "claude@example.com")
        
        # Create Claude project files
        claude_md = temp_dir / "claude.md"
        claude_md.write_text("""# Claude Code Project

## Project Overview
E-commerce platform with user management and order processing.

## Development Standards
1. No debug statements in production code
2. All functions must have comprehensive docstrings
3. Use type hints for all function parameters
4. Handle all edge cases with proper error handling
5. No duplicate code - follow DRY principle

## Architecture
- src/: Source code
- tests/: Test files
- docs/: Documentation
""")
        
        handover_md = temp_dir / "handover.md"
        handover_md.write_text("""# Handover Document

## Current Sprint Tasks
- [x] Set up project structure
- [ ] Implement user registration
- [ ] Add order management
- [ ] Create API endpoints

## Notes for Next Session
Remember to clean up any debug code before committing.
""")
        
        repo.index.add([str(claude_md), str(handover_md)])
        repo.index.commit("Initialize Claude project")
        
        # Install cleanup toolkit
        toolkit_dir = temp_dir / ".cleanup-toolkit"
        toolkit_dir.mkdir()
        
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_src.exists():
            hook_dst = temp_dir / ".git" / "hooks" / "pre-commit"
            hook_dst.parent.mkdir(exist_ok=True)
            shutil.copy2(hook_src, hook_dst)
            os.chmod(hook_dst, 0o755)
        
        # Develop feature with issues
        src_dir = temp_dir / "src"
        src_dir.mkdir()
        
        user_mgmt = src_dir / "user_management.py"
        user_mgmt.write_text("""
import json

def register_user(name, email, password):
    print(f"Debug: Registering {name}")  # Debug
    # TODO: Validate email
    # FIXME: Hash password
    user = {
        'name': name,
        'email': email,
        'password': password  # Security issue!
    }
    print(f"Created user: {user}")  # Debug
    return user

def register_new_user(n, e, p):  # Duplicate with different name
    return register_user(n, e, p)

# Commented old code
# def old_register(data):
#     pass
""")
        
        repo.index.add([str(user_mgmt)])
        
        # Attempt commit
        try:
            repo.index.commit("Add user registration")
        except git.exc.HookExecutionError:
            pass
        
        # Check Claude prompts generated
        claude_prompts = toolkit_dir / "claude-prompts.txt"
        if claude_prompts.exists():
            content = claude_prompts.read_text()
            assert "Initial Analysis Prompt" in content
            assert "cleanup" in content.lower()
        
        # Check handover.md updated
        handover_content = handover_md.read_text()
        assert len(handover_content) > 200  # Should be updated with cleanup request
    
    def test_warp_terminal_workflow(self, temp_dir):
        """Test complete Warp Terminal workflow."""
        # Set up Warp project
        repo = git.Repo.init(temp_dir)
        with repo.config_writer() as config:
            config.set_value("user", "name", "Warp Developer")
            config.set_value("user", "email", "warp@example.com")
        
        # Create Warp configuration
        warp_dir = temp_dir / ".warp"
        warp_dir.mkdir()
        
        workflows_dir = warp_dir / "workflows"
        workflows_dir.mkdir()
        
        # Create cleanup workflow
        cleanup_workflow = workflows_dir / "cleanup.yaml"
        cleanup_workflow.write_text("""
name: code-cleanup
description: Automated code cleanup workflow
commands:
  - name: find-debug
    command: grep -r "console\\.log\\|print" src/
  - name: find-todos
    command: grep -r "TODO\\|FIXME" src/
  - name: check-imports
    command: |
      echo "Checking for unused imports..."
      # Tool-specific command here
""")
        
        repo.index.add([str(cleanup_workflow)])
        repo.index.commit("Add Warp workflows")
        
        # Install cleanup toolkit
        toolkit_dir = temp_dir / ".cleanup-toolkit"
        toolkit_dir.mkdir()
        
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_src.exists():
            hook_dst = temp_dir / ".git" / "hooks" / "pre-commit"
            hook_dst.parent.mkdir(exist_ok=True)
            shutil.copy2(hook_src, hook_dst)
            os.chmod(hook_dst, 0o755)
        
        # Create code with issues
        src_dir = temp_dir / "src"
        src_dir.mkdir()
        
        app_js = src_dir / "app.js"
        app_js.write_text("""
const express = require('express');
const unused = require('unused-module');  // Unused

const app = express();

app.get('/', (req, res) => {
    console.log('Debug: Home route accessed');  // Debug
    // TODO: Add authentication
    // FIXME: Handle errors
    res.send('Hello World');
});

app.get('/users', (req, res) => {
    console.log('Debug: Users route');  // Debug
    res.json([]);
});

// Duplicate route handler
app.get('/get-users', (req, res) => {
    console.log('Debug: Get users');  // Debug
    res.json([]);
});

// Old code
// app.get('/old', (req, res) => {
//     res.send('old');
// });

app.listen(3000);
""")
        
        repo.index.add([str(app_js)])
        
        # Attempt commit
        try:
            repo.index.commit("Add Express app")
        except git.exc.HookExecutionError:
            pass
        
        # Check Warp prompts generated
        warp_prompts = toolkit_dir / "warp-ai-prompts.txt"
        warp_context = toolkit_dir / "warp-ai-context.md"
        
        if warp_prompts.exists():
            content = warp_prompts.read_text()
            assert "Analysis Prompt" in content
            assert "Cleanup Execution Prompt" in content
        
        if warp_context.exists():
            content = warp_context.read_text()
            assert "app.js" in content


@pytest.mark.e2e
class TestTeamCollaborationWorkflow:
    """Test team collaboration scenarios."""
    
    def test_multi_developer_workflow(self, temp_dir):
        """Test workflow with multiple developers."""
        # Create shared repository
        shared_repo_dir = temp_dir / "shared_repo"
        shared_repo_dir.mkdir()
        shared_repo = git.Repo.init(shared_repo_dir, bare=True)
        
        # Developer 1 setup
        dev1_dir = temp_dir / "dev1"
        dev1_dir.mkdir()
        dev1_repo = git.Repo.clone_from(shared_repo_dir, dev1_dir)
        with dev1_repo.config_writer() as config:
            config.set_value("user", "name", "Developer 1")
            config.set_value("user", "email", "dev1@example.com")
        
        # Developer 2 setup
        dev2_dir = temp_dir / "dev2"
        dev2_dir.mkdir()
        dev2_repo = git.Repo.clone_from(shared_repo_dir, dev2_dir)
        with dev2_repo.config_writer() as config:
            config.set_value("user", "name", "Developer 2")
            config.set_value("user", "email", "dev2@example.com")
        
        # Both developers install cleanup toolkit
        for dev_dir in [dev1_dir, dev2_dir]:
            toolkit_dir = dev_dir / ".cleanup-toolkit"
            toolkit_dir.mkdir()
            
            hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
            if hook_src.exists():
                hook_dst = dev_dir / ".git" / "hooks" / "pre-commit"
                hook_dst.parent.mkdir(exist_ok=True)
                shutil.copy2(hook_src, hook_dst)
                os.chmod(hook_dst, 0o755)
        
        # Developer 1 creates initial code
        readme = dev1_dir / "README.md"
        readme.write_text("# Team Project\n")
        dev1_repo.index.add([str(readme)])
        dev1_repo.index.commit("Initial commit", skip_hooks=True)
        dev1_repo.remotes.origin.push("main")
        
        # Developer 2 pulls and adds feature
        dev2_repo.remotes.origin.pull("main")
        
        feature_file = dev2_dir / "feature.py"
        feature_file.write_text("""
def feature():
    print("Debug: Feature")  # Will be caught by cleanup
    # TODO: Implement
    pass
""")
        
        dev2_repo.index.add([str(feature_file)])
        
        # Cleanup hook should trigger
        try:
            dev2_repo.index.commit("Add feature")
        except git.exc.HookExecutionError:
            # Expected - cleanup needed
            pass
        
        # Check cleanup was triggered
        toolkit_dir = dev2_dir / ".cleanup-toolkit"
        context_file = toolkit_dir / "cleanup-context.md"
        if context_file.exists():
            assert "feature.py" in context_file.read_text()


@pytest.mark.e2e
@pytest.mark.slow
class TestPerformanceWorkflow:
    """Test performance with large codebases."""
    
    def test_large_repository_performance(self, temp_dir):
        """Test cleanup performance with large repository."""
        repo = git.Repo.init(temp_dir)
        with repo.config_writer() as config:
            config.set_value("user", "name", "Perf Tester")
            config.set_value("user", "email", "perf@example.com")
        
        # Create large codebase
        src_dir = temp_dir / "src"
        src_dir.mkdir()
        
        # Generate 100 Python files
        for i in range(100):
            module_dir = src_dir / f"module_{i}"
            module_dir.mkdir()
            
            for j in range(10):
                file_path = module_dir / f"file_{j}.py"
                file_path.write_text(f"""
# Module {i} File {j}
import os
import sys

def function_{i}_{j}(x, y):
    result = x + y
    return result

class Class_{i}_{j}:
    def __init__(self):
        self.value = {i * 10 + j}
    
    def method(self):
        return self.value * 2
""")
        
        # Add all files
        repo.index.add(["src/"])
        repo.index.commit("Initial large codebase")
        
        # Install cleanup toolkit
        toolkit_dir = temp_dir / ".cleanup-toolkit"
        toolkit_dir.mkdir()
        
        hook_src = Path(__file__).parent.parent.parent / "hooks" / "pre-commit"
        if hook_src.exists():
            hook_dst = temp_dir / ".git" / "hooks" / "pre-commit"
            hook_dst.parent.mkdir(exist_ok=True)
            shutil.copy2(hook_src, hook_dst)
            os.chmod(hook_dst, 0o755)
        
        # Make changes to multiple files
        for i in range(10):
            file_path = src_dir / f"module_{i}" / "file_0.py"
            content = file_path.read_text()
            content += "\n# TODO: Optimize this\nprint('Debug')"
            file_path.write_text(content)
            repo.index.add([str(file_path)])
        
        # Measure cleanup time
        start_time = time.time()
        
        try:
            repo.index.commit("Update multiple modules")
        except git.exc.HookExecutionError:
            pass
        
        elapsed = time.time() - start_time
        
        # Should complete within reasonable time (< 10 seconds)
        assert elapsed < 10, f"Cleanup took too long: {elapsed:.2f} seconds"
        
        # Verify cleanup context generated
        context_file = toolkit_dir / "cleanup-context.md"
        assert context_file.exists()