"""
Core cleanup engine functionality.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional


class CleanupConfig:
    """Configuration for cleanup operations."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize cleanup configuration."""
        self.config_path = config_path or ".cleanup-toolkit/config.yml"
        self.enabled = True
        self.auto_fix = False
        self.exclude_patterns = [
            "*.min.js",
            "node_modules/",
            "vendor/",
            "__pycache__/",
            ".git/",
        ]
        self.debug_patterns = {
            "python": [r"print\(", r"breakpoint\(\)", r"import pdb"],
            "javascript": [r"console\.(log|debug|info)", r"debugger;"],
            "go": [r"fmt\.Print", r"log\.Print"],
        }
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        return {
            "enabled": self.enabled,
            "auto_fix": self.auto_fix,
            "exclude_patterns": self.exclude_patterns,
            "debug_patterns": self.debug_patterns,
        }
    
    def is_excluded(self, file_path: str) -> bool:
        """Check if file should be excluded from cleanup."""
        path = Path(file_path)
        for pattern in self.exclude_patterns:
            if pattern in str(path):
                return True
        return False


class CleanupEngine:
    """Main engine for code cleanup operations."""
    
    def __init__(self, config: Optional[CleanupConfig] = None):
        """Initialize the cleanup engine."""
        self.config = config or CleanupConfig()
        self.stats = {
            "files_processed": 0,
            "issues_found": 0,
            "issues_fixed": 0,
            "debug_statements": 0,
            "todos": 0,
            "duplicates": 0,
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file for cleanup opportunities."""
        if self.config.is_excluded(file_path):
            return {"skipped": True, "reason": "excluded"}
        
        results = {
            "file": file_path,
            "issues": [],
            "stats": {},
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
            
            # Check for debug statements
            language = self._detect_language(file_path)
            if language in self.config.debug_patterns:
                for pattern_str in self.config.debug_patterns[language]:
                    pattern = re.compile(pattern_str)
                    for i, line in enumerate(lines, 1):
                        if pattern.search(line):
                            results["issues"].append({
                                "type": "debug",
                                "line": i,
                                "content": line.strip(),
                            })
                            self.stats["debug_statements"] += 1
            
            # Check for TODOs
            todo_pattern = re.compile(r"(TODO|FIXME|XXX|HACK):")
            for i, line in enumerate(lines, 1):
                if todo_pattern.search(line):
                    results["issues"].append({
                        "type": "todo",
                        "line": i,
                        "content": line.strip(),
                    })
                    self.stats["todos"] += 1
            
            self.stats["files_processed"] += 1
            self.stats["issues_found"] += len(results["issues"])
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def analyze_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Analyze all files in a directory."""
        results = []
        path = Path(directory)
        
        for file_path in path.rglob("*"):
            if file_path.is_file():
                result = self.analyze_file(str(file_path))
                if not result.get("skipped"):
                    results.append(result)
        
        return results
    
    def cleanup_file(self, file_path: str, fix: bool = False) -> Dict[str, Any]:
        """Clean up a single file."""
        analysis = self.analyze_file(file_path)
        
        if fix and self.config.auto_fix and analysis.get("issues"):
            # Implementation for automatic fixing would go here
            pass
        
        return analysis
    
    def get_summary(self) -> Dict[str, Any]:
        """Get cleanup summary statistics."""
        return self.stats.copy()
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        ext = Path(file_path).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "javascript",
            ".tsx": "javascript",
            ".go": "go",
            ".java": "java",
            ".rb": "ruby",
            ".php": "php",
            ".c": "c",
            ".cpp": "cpp",
            ".cs": "csharp",
            ".rs": "rust",
        }
        return language_map.get(ext, "unknown")