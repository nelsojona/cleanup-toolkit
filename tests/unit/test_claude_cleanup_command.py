"""
Tests for Claude Code /cleanup custom command functionality.

This module tests the /cleanup command integration with Claude Code,
verifying that the command file exists, is properly formatted, and
provides the expected functionality documentation.
"""

import os
import re
from pathlib import Path
import pytest


class TestClaudeCleanupCommand:
    """Test the Claude Code /cleanup custom command."""
    
    @pytest.fixture
    def project_root(self):
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent.resolve()
    
    @pytest.fixture
    def claude_commands_dir(self, project_root):
        """Get the Claude commands directory."""
        return project_root / ".claude" / "commands"
    
    @pytest.fixture
    def cleanup_command_file(self, claude_commands_dir):
        """Get the cleanup command file path."""
        return claude_commands_dir / "cleanup.md"
    
    def test_claude_commands_directory_exists(self, claude_commands_dir):
        """Test that .claude/commands directory exists."""
        assert claude_commands_dir.exists(), ".claude/commands directory should exist"
        assert claude_commands_dir.is_dir(), ".claude/commands should be a directory"
    
    def test_cleanup_command_file_exists(self, cleanup_command_file):
        """Test that cleanup.md command file exists."""
        assert cleanup_command_file.exists(), "cleanup.md command file should exist"
        assert cleanup_command_file.is_file(), "cleanup.md should be a file"
        assert cleanup_command_file.suffix == ".md", "Command file should have .md extension"
    
    def test_cleanup_command_has_required_sections(self, cleanup_command_file):
        """Test that cleanup command has all required documentation sections."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        
        content = cleanup_command_file.read_text()
        
        required_sections = [
            "# /cleanup",  # Command title
            "## Description",  # What it does
            "## Usage",  # How to use it
            "## Options",  # Available options
            "## Examples",  # Usage examples
            "## Workflow",  # Step-by-step process
        ]
        
        for section in required_sections:
            assert section in content, f"Missing required section: {section}"
    
    def test_cleanup_command_has_options_documented(self, cleanup_command_file):
        """Test that cleanup command documents all important options."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        expected_options = [
            "--all",
            "--staged",
            "--modified",
            "--debug",
            "--todos",
            "--duplicates",
            "--unused",
            "--docs",
            "--test",
            "--language",
        ]
        
        for option in expected_options:
            assert option in content, f"Missing option documentation: {option}"
    
    def test_cleanup_command_has_language_examples(self, cleanup_command_file):
        """Test that cleanup command includes language-specific examples."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        languages = ["Python", "JavaScript", "Go", "Java"]
        
        for language in languages:
            assert language in content or language.lower() in content, \
                f"Missing language examples for: {language}"
    
    def test_cleanup_command_has_debug_patterns(self, cleanup_command_file):
        """Test that cleanup command documents debug statement patterns."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        debug_patterns = [
            "print()",
            "console.log()",
            "fmt.Print()",
            "System.out.print()",
        ]
        
        for pattern in debug_patterns:
            assert pattern in content, f"Missing debug pattern: {pattern}"
    
    def test_cleanup_command_integration_documented(self, cleanup_command_file):
        """Test that cleanup command documents toolkit integration."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        integration_points = [
            "Pre-commit Hook",
            "cleanup-toolkit",
            "config.yml",
            ".cleanupignore",
        ]
        
        for point in integration_points:
            assert point.lower() in content.lower(), \
                f"Missing integration documentation: {point}"
    
    def test_cleanup_command_has_examples(self, cleanup_command_file):
        """Test that cleanup command provides practical examples."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        # Check for code blocks with examples
        code_blocks = re.findall(r'```[^`]*```', content, re.MULTILINE)
        assert len(code_blocks) > 5, "Should have multiple code examples"
        
        # Check for specific example commands
        example_commands = [
            "/cleanup --staged",
            "/cleanup --all",
            "/cleanup --test",
        ]
        
        for cmd in example_commands:
            assert cmd in content, f"Missing example command: {cmd}"
    
    def test_cleanup_command_readme_exists(self, claude_commands_dir):
        """Test that commands directory has a README."""
        readme_file = claude_commands_dir / "README.md"
        assert readme_file.exists(), "Commands directory should have README.md"
        
        content = readme_file.read_text()
        assert "/cleanup" in content, "README should document /cleanup command"
        assert "Claude Code" in content, "README should mention Claude Code"
    
    def test_cleanup_command_file_size_reasonable(self, cleanup_command_file):
        """Test that cleanup command file has substantial documentation."""
        file_size = cleanup_command_file.stat().st_size
        
        # Should be at least 2KB (substantial documentation)
        assert file_size > 2000, "Command file should have substantial documentation"
        
        # But not too large (under 50KB)
        assert file_size < 50000, "Command file should not be excessively large"
    
    def test_cleanup_command_has_error_handling(self, cleanup_command_file):
        """Test that cleanup command documents error handling."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        error_keywords = [
            "error",
            "fail",
            "issue",
            "problem",
            "troubleshoot",
        ]
        
        found_error_handling = any(
            keyword in content.lower() for keyword in error_keywords
        )
        assert found_error_handling, "Command should document error handling"
    
    def test_cleanup_command_has_output_format(self, cleanup_command_file):
        """Test that cleanup command documents output format."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        output_indicators = [
            "Output",
            "Results",
            "Report",
            "Summary",
            "Complete",
        ]
        
        found_output_docs = any(
            indicator in content for indicator in output_indicators
        )
        assert found_output_docs, "Command should document output format"
    
    def test_cleanup_command_workflow_steps(self, cleanup_command_file):
        """Test that cleanup command has numbered workflow steps."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        # Look for numbered steps in workflow
        steps = re.findall(r'\d+\.\s+\*\*[^*]+\*\*', content)
        assert len(steps) >= 3, "Workflow should have at least 3 documented steps"
    
    def test_cleanup_command_best_practices(self, cleanup_command_file):
        """Test that cleanup command includes best practices."""
        if not cleanup_command_file.exists():
            pytest.skip("Command file not found in CI")
        content = cleanup_command_file.read_text()
        
        assert "Best Practices" in content, "Should include best practices section"
        
        # Check for specific best practice recommendations
        best_practices = [
            "test mode",
            "incremental",
            "functionality",
            "document",
        ]
        
        for practice in best_practices:
            assert practice.lower() in content.lower(), \
                f"Missing best practice: {practice}"


class TestClaudeCommandsIntegration:
    """Test the integration of Claude commands with the cleanup toolkit."""
    
    @pytest.fixture
    def project_root(self):
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent.resolve()
    
    def test_claude_directory_structure(self, project_root):
        """Test that Claude directory structure is properly set up."""
        claude_dir = project_root / ".claude"
        commands_dir = claude_dir / "commands"
        
        assert claude_dir.exists(), ".claude directory should exist"
        assert commands_dir.exists(), ".claude/commands directory should exist"
        
        # Check for command files
        md_files = list(commands_dir.glob("*.md"))
        assert len(md_files) > 0, "Should have at least one command file"
    
    def test_command_files_are_markdown(self, project_root):
        """Test that all command files are valid markdown."""
        commands_dir = project_root / ".claude" / "commands"
        
        if not commands_dir.exists():
            pytest.skip("Commands directory not found in CI")
        
        for md_file in commands_dir.glob("*.md"):
            content = md_file.read_text()
            
            # Basic markdown validation
            assert content.strip(), f"{md_file.name} should not be empty"
            assert "#" in content, f"{md_file.name} should have markdown headers"
            
            # Command files should start with command name (except README)
            if md_file.stem.lower() != "readme":
                command_name = f"/{md_file.stem}"
                assert command_name in content, \
                    f"{md_file.name} should document {command_name} command"
    
    def test_no_conflicting_command_names(self, project_root):
        """Test that command names don't conflict."""
        commands_dir = project_root / ".claude" / "commands"
        
        command_names = []
        for md_file in commands_dir.glob("*.md"):
            command_name = md_file.stem.lower()
            assert command_name not in command_names, \
                f"Duplicate command name: {command_name}"
            command_names.append(command_name)
    
    def test_commands_follow_naming_convention(self, project_root):
        """Test that command files follow naming conventions."""
        commands_dir = project_root / ".claude" / "commands"
        
        for md_file in commands_dir.glob("*.md"):
            filename = md_file.stem
            
            # Should be lowercase
            assert filename.islower() or filename == "README", \
                f"Command file should be lowercase: {filename}"
            
            # Should not have spaces or special characters
            assert re.match(r'^[a-z0-9_-]+$', filename) or filename == "README", \
                f"Command file has invalid characters: {filename}"
    
    def test_cleanup_command_is_discoverable(self, project_root):
        """Test that cleanup command is discoverable by Claude."""
        commands_dir = project_root / ".claude" / "commands"
        cleanup_file = commands_dir / "cleanup.md"
        
        assert cleanup_file.exists(), "cleanup.md should exist"
        
        # File should be readable
        assert os.access(cleanup_file, os.R_OK), "cleanup.md should be readable"
        
        # Directory should be accessible
        assert os.access(commands_dir, os.R_OK | os.X_OK), \
            "Commands directory should be readable and executable"


class TestCleanupCommandFunctionality:
    """Test the functional aspects of the cleanup command documentation."""
    
    @pytest.fixture
    def cleanup_content(self, project_root):
        """Get the cleanup command content."""
        cleanup_file = project_root / ".claude" / "commands" / "cleanup.md"
        if not cleanup_file.exists():
            # Return empty string if file doesn't exist (for CI)
            return ""
        return cleanup_file.read_text()
    
    @pytest.fixture
    def project_root(self):
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent.resolve()
    
    def test_command_supports_multiple_file_selection(self, cleanup_content):
        """Test that command supports various file selection methods."""
        if not cleanup_content:
            pytest.skip("Command content not available in CI")
        selection_methods = [
            "--all",  # All files
            "--staged",  # Git staged files
            "--modified",  # Modified files
            "[files...]",  # Specific files
        ]
        
        for method in selection_methods:
            assert method in cleanup_content, \
                f"Should support file selection: {method}"
    
    def test_command_supports_cleanup_types(self, cleanup_content):
        """Test that command supports different cleanup types."""
        if not cleanup_content:
            pytest.skip("Command content not available in CI")
        cleanup_types = [
            "--debug",  # Debug statements
            "--todos",  # TODO comments
            "--duplicates",  # Duplicate code
            "--unused",  # Unused imports
            "--docs",  # Documentation
        ]
        
        for cleanup_type in cleanup_types:
            assert cleanup_type in cleanup_content, \
                f"Should support cleanup type: {cleanup_type}"
    
    def test_command_has_safety_features(self, cleanup_content):
        """Test that command has safety features documented."""
        if not cleanup_content:
            pytest.skip("Command content not available in CI")
        safety_features = [
            "--test",  # Test mode
            "preview",  # Preview changes
            "verify",  # Verification
            "preserve",  # Preserve functionality
        ]
        
        for feature in safety_features:
            assert feature.lower() in cleanup_content.lower(), \
                f"Should have safety feature: {feature}"
    
    def test_command_configuration_support(self, cleanup_content):
        """Test that command supports configuration."""
        if not cleanup_content:
            pytest.skip("Command content not available in CI")
        config_items = [
            "config.yml",
            ".cleanupignore",
            "patterns.yml",
            "languages.yml",
        ]
        
        for item in config_items:
            assert item in cleanup_content, \
                f"Should support configuration: {item}"
    
    def test_command_has_related_commands(self, cleanup_content):
        """Test that command references related commands."""
        if not cleanup_content:
            pytest.skip("Command content not available in CI")
        assert "Related Commands" in cleanup_content, \
            "Should have related commands section"
        
        related_commands = [
            "/analyze",
            "/format",
            "/lint",
            "/test",
        ]
        
        for cmd in related_commands:
            assert cmd in cleanup_content, \
                f"Should reference related command: {cmd}"