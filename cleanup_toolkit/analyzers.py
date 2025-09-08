"""
Code analysis utilities for the cleanup toolkit.
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set


class PatternMatcher:
    """Pattern matching for code cleanup."""
    
    def __init__(self):
        """Initialize the pattern matcher."""
        self.patterns = {
            "debug": {
                "python": [
                    r"print\s*\(",
                    r"breakpoint\s*\(\)",
                    r"import\s+pdb",
                    r"pdb\.set_trace",
                    r"import\s+ipdb",
                    r"ipdb\.set_trace",
                ],
                "javascript": [
                    r"console\.(log|debug|info|warn|error)",
                    r"debugger\s*;",
                    r"alert\s*\(",
                ],
                "go": [
                    r"fmt\.Print",
                    r"log\.Print",
                    r"println\(",
                ],
            },
            "todo": [
                r"#\s*(TODO|FIXME|XXX|HACK|NOTE):",
                r"//\s*(TODO|FIXME|XXX|HACK|NOTE):",
                r"/\*\s*(TODO|FIXME|XXX|HACK|NOTE):",
            ],
        }
    
    def find_patterns(self, content: str, pattern_type: str, language: str = None) -> List[Dict[str, Any]]:
        """Find patterns in code content."""
        matches = []
        lines = content.splitlines()
        
        if pattern_type == "debug" and language:
            patterns = self.patterns["debug"].get(language, [])
        elif pattern_type == "todo":
            patterns = self.patterns["todo"]
        else:
            patterns = []
        
        for pattern_str in patterns:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            for i, line in enumerate(lines, 1):
                if pattern.search(line):
                    matches.append({
                        "line": i,
                        "content": line.strip(),
                        "pattern": pattern_str,
                        "type": pattern_type,
                    })
        
        return matches
    
    def add_custom_pattern(self, pattern_type: str, pattern: str, language: str = None):
        """Add a custom pattern for matching."""
        if pattern_type not in self.patterns:
            self.patterns[pattern_type] = {}
        
        if language:
            if language not in self.patterns[pattern_type]:
                self.patterns[pattern_type][language] = []
            self.patterns[pattern_type][language].append(pattern)
        else:
            if pattern_type not in self.patterns:
                self.patterns[pattern_type] = []
            self.patterns[pattern_type].append(pattern)


class CodeAnalyzer:
    """Analyze code for various quality issues."""
    
    def __init__(self):
        """Initialize the code analyzer."""
        self.pattern_matcher = PatternMatcher()
        self.supported_languages = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "javascript",
            ".tsx": "javascript",
            ".go": "go",
            ".java": "java",
            ".rb": "ruby",
            ".php": "php",
        }
    
    def analyze(self, file_path: str) -> Dict[str, Any]:
        """Analyze a code file for issues."""
        path = Path(file_path)
        if not path.exists():
            return {"error": "File not found"}
        
        language = self._detect_language(file_path)
        results = {
            "file": file_path,
            "language": language,
            "issues": [],
            "metrics": {},
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find debug statements
            debug_matches = self.pattern_matcher.find_patterns(content, "debug", language)
            results["issues"].extend(debug_matches)
            
            # Find TODOs
            todo_matches = self.pattern_matcher.find_patterns(content, "todo")
            results["issues"].extend(todo_matches)
            
            # Calculate metrics
            lines = content.splitlines()
            results["metrics"] = {
                "total_lines": len(lines),
                "blank_lines": sum(1 for line in lines if not line.strip()),
                "comment_lines": self._count_comment_lines(lines, language),
                "debug_statements": len(debug_matches),
                "todos": len(todo_matches),
            }
            
            # Language-specific analysis
            if language == "python":
                results["python_analysis"] = self._analyze_python(content)
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def find_duplicates(self, directory: str) -> List[Dict[str, Any]]:
        """Find duplicate code blocks in a directory."""
        duplicates = []
        file_hashes = {}
        
        for file_path in Path(directory).rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Simple hash-based duplicate detection
                    content_hash = hash(content)
                    if content_hash in file_hashes:
                        duplicates.append({
                            "file1": str(file_hashes[content_hash]),
                            "file2": str(file_path),
                            "type": "exact_duplicate",
                        })
                    else:
                        file_hashes[content_hash] = file_path
                
                except Exception:
                    pass
        
        return duplicates
    
    def find_unused_imports(self, file_path: str) -> List[str]:
        """Find unused imports in a Python file."""
        if not file_path.endswith('.py'):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            imported_names = set()
            used_names = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_names.add(alias.asname or alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imported_names.add(alias.asname or alias.name)
                elif isinstance(node, ast.Name):
                    used_names.add(node.id)
            
            unused = imported_names - used_names
            return list(unused)
        
        except Exception:
            return []
    
    def _detect_language(self, file_path: str) -> str:
        """Detect the programming language of a file."""
        ext = Path(file_path).suffix.lower()
        return self.supported_languages.get(ext, "unknown")
    
    def _is_code_file(self, file_path: Path) -> bool:
        """Check if a file is a code file."""
        return file_path.suffix.lower() in self.supported_languages
    
    def _count_comment_lines(self, lines: List[str], language: str) -> int:
        """Count comment lines in code."""
        count = 0
        comment_patterns = {
            "python": r"^\s*#",
            "javascript": r"^\s*(//|/\*|\*)",
            "go": r"^\s*//",
            "java": r"^\s*(//|/\*|\*)",
        }
        
        pattern_str = comment_patterns.get(language)
        if not pattern_str:
            return 0
        
        pattern = re.compile(pattern_str)
        for line in lines:
            if pattern.match(line):
                count += 1
        
        return count
    
    def _analyze_python(self, content: str) -> Dict[str, Any]:
        """Perform Python-specific analysis."""
        try:
            tree = ast.parse(content)
            return {
                "classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
                "functions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                "imports": len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]),
            }
        except Exception:
            return {}