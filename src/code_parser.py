import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class CodeParser:
    def __init__(self):
        self.language_extensions = {
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
            '.kt': 'kotlin'
        }
    
    def detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        return self.language_extensions.get(ext, 'text')
    
    def parse_functions(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Parse functions from code"""
        functions = []
        
        patterns = {
            'python': r'def\s+(\w+)\s*\([^)]*\):',
            'javascript': r'function\s+(\w+)\s*\([^)]*\)|(\w+)\s*=\s*\([^)]*\)\s*=>',
            'java': r'(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\([^)]*\)',
            'cpp': r'\w+\s+(\w+)\s*\([^)]*\)',
            'go': r'func\s+(\w+)\s*\([^)]*\)',
            'rust': r'fn\s+(\w+)\s*\([^)]*\)',
        }
        
        pattern = patterns.get(language)
        if pattern:
            matches = re.finditer(pattern, code, re.MULTILINE)
            for match in matches:
                func_name = match.group(1) if match.group(1) else match.group(2)
                if func_name:
                    functions.append({
                        'name': func_name,
                        'start': match.start(),
                        'end': match.end(),
                        'signature': match.group(0)
                    })
        
        return functions
    
    def find_context_around_cursor(self, code: str, cursor_position: int, 
                                 context_lines: int = 10) -> Tuple[str, int, int]:
        """Find context around cursor position"""
        lines = code.split('\n')
        
        # Find line number of cursor
        char_count = 0
        cursor_line = 0
        
        for i, line in enumerate(lines):
            if char_count + len(line) >= cursor_position:
                cursor_line = i
                break
            char_count += len(line) + 1  # +1 for newline
        
        # Get context lines
        start_line = max(0, cursor_line - context_lines)
        end_line = min(len(lines), cursor_line + context_lines + 1)
        
        context_code = '\n'.join(lines[start_line:end_line])
        
        return context_code, start_line, end_line
    
    def extract_imports(self, code: str, language: str) -> List[str]:
        """Extract import statements"""
        imports = []
        
        patterns = {
            'python': r'(import\s+\w+|from\s+\w+\s+import\s+.*)',
            'javascript': r'(import\s+.*\s+from\s+[\'"].*[\'"]|const\s+.*\s+=\s+require\([\'"].*[\'"]\))',
            'java': r'import\s+[\w.]+;',
            'cpp': r'#include\s*[<"][^>"]*[>"]',
            'go': r'import\s+\([^)]*\)|import\s+"[^"]*"',
        }
        
        pattern = patterns.get(language)
        if pattern:
            matches = re.findall(pattern, code, re.MULTILINE)
            imports.extend(matches)
        
        return imports