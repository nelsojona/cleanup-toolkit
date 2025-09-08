"""
Command interface for the cleanup toolkit.
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

from cleanup_toolkit.core import CleanupEngine, CleanupConfig
from cleanup_toolkit.analyzers import CodeAnalyzer


class CleanupCommand:
    """Command-line interface for cleanup operations."""
    
    def __init__(self, config: Optional[CleanupConfig] = None):
        """Initialize the cleanup command."""
        self.config = config or CleanupConfig()
        self.engine = CleanupEngine(self.config)
        self.analyzer = CodeAnalyzer()
    
    def run(self, 
            files: List[str] = None,
            all_files: bool = False,
            staged: bool = False,
            modified: bool = False,
            debug: bool = False,
            todos: bool = False,
            duplicates: bool = False,
            unused: bool = False,
            docs: bool = False,
            test_mode: bool = False,
            language: str = None) -> Dict[str, Any]:
        """Run cleanup command with specified options."""
        
        # Determine which files to process
        target_files = self._get_target_files(files, all_files, staged, modified)
        
        if not target_files:
            return {"error": "No files to process"}
        
        results = {
            "files_analyzed": len(target_files),
            "issues_found": 0,
            "issues_fixed": 0,
            "details": [],
        }
        
        # Process each file
        for file_path in target_files:
            if language and not self._matches_language(file_path, language):
                continue
            
            file_results = self._process_file(
                file_path,
                debug=debug,
                todos=todos,
                unused=unused,
                test_mode=test_mode
            )
            
            results["details"].append(file_results)
            results["issues_found"] += len(file_results.get("issues", []))
        
        # Find duplicates if requested
        if duplicates:
            dup_results = self.analyzer.find_duplicates(".")
            results["duplicates"] = dup_results
        
        # Generate summary
        results["summary"] = self.engine.get_summary()
        
        return results
    
    def _get_target_files(self, 
                         files: List[str],
                         all_files: bool,
                         staged: bool,
                         modified: bool) -> List[str]:
        """Get list of files to process based on options."""
        if files:
            return files
        
        if all_files:
            return self._get_all_files()
        
        if staged:
            return self._get_staged_files()
        
        if modified:
            return self._get_modified_files()
        
        return []
    
    def _get_all_files(self) -> List[str]:
        """Get all files in the project."""
        files = []
        for path in Path(".").rglob("*"):
            if path.is_file() and not self.config.is_excluded(str(path)):
                files.append(str(path))
        return files
    
    def _get_staged_files(self) -> List[str]:
        """Get git staged files."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            return [f for f in result.stdout.strip().split("\n") if f]
        except subprocess.CalledProcessError:
            return []
    
    def _get_modified_files(self) -> List[str]:
        """Get modified files in git."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            modified = [f for f in result.stdout.strip().split("\n") if f]
            
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                capture_output=True,
                text=True,
                check=True
            )
            untracked = [f for f in result.stdout.strip().split("\n") if f]
            
            return modified + untracked
        except subprocess.CalledProcessError:
            return []
    
    def _process_file(self,
                     file_path: str,
                     debug: bool,
                     todos: bool,
                     unused: bool,
                     test_mode: bool) -> Dict[str, Any]:
        """Process a single file for cleanup."""
        results = self.analyzer.analyze(file_path)
        
        # Filter issues based on options
        if not debug and not todos and not unused:
            # If no specific options, include all
            pass
        else:
            filtered_issues = []
            for issue in results.get("issues", []):
                if debug and issue["type"] == "debug":
                    filtered_issues.append(issue)
                elif todos and issue["type"] == "todo":
                    filtered_issues.append(issue)
            results["issues"] = filtered_issues
        
        # Check for unused imports if requested
        if unused and file_path.endswith('.py'):
            unused_imports = self.analyzer.find_unused_imports(file_path)
            for imp in unused_imports:
                results["issues"].append({
                    "type": "unused_import",
                    "content": f"Unused import: {imp}",
                })
        
        # Apply fixes if not in test mode
        if not test_mode and results.get("issues") and self.config.auto_fix:
            # Implementation for automatic fixing would go here
            pass
        
        return results
    
    def _matches_language(self, file_path: str, language: str) -> bool:
        """Check if file matches the specified language."""
        language_extensions = {
            "python": [".py"],
            "javascript": [".js", ".jsx", ".ts", ".tsx"],
            "go": [".go"],
            "java": [".java"],
            "ruby": [".rb"],
            "php": [".php"],
        }
        
        extensions = language_extensions.get(language.lower(), [])
        return any(file_path.endswith(ext) for ext in extensions)
    
    def format_output(self, results: Dict[str, Any]) -> str:
        """Format results for display."""
        output = []
        output.append("🧹 Code Cleanup Analysis")
        output.append("=" * 40)
        output.append(f"📁 Files analyzed: {results['files_analyzed']}")
        output.append(f"🐛 Issues found: {results['issues_found']}")
        
        if results.get("duplicates"):
            output.append(f"🔄 Duplicate files: {len(results['duplicates'])}")
        
        summary = results.get("summary", {})
        if summary:
            output.append("")
            output.append("Summary:")
            output.append(f"  Debug statements: {summary.get('debug_statements', 0)}")
            output.append(f"  TODOs/FIXMEs: {summary.get('todos', 0)}")
            output.append(f"  Duplicates: {summary.get('duplicates', 0)}")
        
        if results['issues_fixed'] > 0:
            output.append("")
            output.append("✨ Cleanup Complete!")
            output.append(f"  Fixed {results['issues_fixed']} issues")
        
        return "\n".join(output)