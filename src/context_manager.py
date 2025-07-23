import os
from typing import Dict, List, Optional
from pathlib import Path

class ContextManager:
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.file_cache = {}
        self.context_history = []
        
    def get_project_structure(self) -> Dict[str, List[str]]:
        """Get project file structure"""
        structure = {}
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden directories and common build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist']]
            
            rel_root = os.path.relpath(root, self.project_root)
            structure[rel_root] = []
            
            for file in files:
                if not file.startswith('.') and self._is_code_file(file):
                    structure[rel_root].append(file)
        
        return structure
    
    def get_related_files(self, current_file: str) -> List[str]:
        """Find files related to current file"""
        related = []
        current_path = Path(current_file)
        
        # Same directory files
        if current_path.parent.exists():
            for file in current_path.parent.iterdir():
                if file.is_file() and self._is_code_file(file.name) and file != current_path:
                    related.append(str(file))
        
        # Files with similar names
        base_name = current_path.stem
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if base_name in file and file != current_path.name:
                    related.append(os.path.join(root, file))
        
        return related[:10]  # Limit to 10 related files
    
    def read_file(self, file_path: str) -> Optional[str]:
        """Read file content with caching"""
        abs_path = os.path.abspath(file_path)
        
        if abs_path in self.file_cache:
            return self.file_cache[abs_path]
        
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.file_cache[abs_path] = content
                return content
        except (IOError, UnicodeDecodeError):
            return None
    
    def get_file_context(self, file_path: str) -> Dict[str, any]:
        """Get comprehensive context for a file"""
        content = self.read_file(file_path)
        if not content:
            return {}
        
        return {
            'content': content,
            'size': len(content),
            'lines': len(content.split('\n')),
            'related_files': self.get_related_files(file_path),
            'language': self._detect_language(file_path)
        }
    
    def _is_code_file(self, filename: str) -> bool:
        """Check if file is a code file"""
        code_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp',
            '.go', '.rs', '.rb', '.php', '.cs', '.swift', '.kt', '.scala',
            '.html', '.css', '.scss', '.less', '.xml', '.json', '.yaml', '.yml'
        }
        
        return Path(filename).suffix.lower() in code_extensions
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language"""
        ext = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.cs': 'csharp',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml'
        }
        
        return language_map.get(ext, 'text')