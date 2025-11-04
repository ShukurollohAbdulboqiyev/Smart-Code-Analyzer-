import ast
import math

class CodeMetrics:
    def analyze(self, code):
        """Analyze code metrics"""
        try:
            tree = ast.parse(code)
            return {
                'line_count': self._count_lines(code),
                'function_count': self._count_functions(tree),
                'class_count': self._count_classes(tree),
                'comment_ratio': self._calculate_comment_ratio(code),
                'cyclomatic_complexity': self._calculate_complexity(tree),
                'maintainability_index': self._calculate_maintainability_index(code, tree)
            }
        except SyntaxError:
            return {'error': 'Syntax error in code'}
    
    def _count_lines(self, code):
        return len(code.splitlines())
    
    def _count_functions(self, tree):
        return len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
    
    def _count_classes(self, tree):
        return len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
    
    def _calculate_comment_ratio(self, code):
        lines = code.splitlines()
        if not lines:
            return 0
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        return (comment_lines / len(lines)) * 100
    
    def _calculate_complexity(self, tree):
        complexity = 1  # Base complexity
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, 
                               ast.Try, ast.With, ast.AsyncWith)):
                complexity += 1
        return complexity
    
    def _calculate_maintainability_index(self, code, tree):
        # Simplified maintainability index calculation
        lines = self._count_lines(code)
        complexity = self._calculate_complexity(tree)
        comment_ratio = self._calculate_comment_ratio(code)
        
        if lines == 0:
            return 100
            
        # Heuristic formula
        mi = 171 - 5.2 * math.log(complexity) - 0.23 * lines + 0.99 * comment_ratio
        return max(0, min(100, mi))