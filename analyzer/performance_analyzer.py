import ast

class PerformanceAnalyzer:
    def check(self, code):
        """Check for performance issues"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Check for nested loops
            issues.extend(self._find_nested_loops(tree))
            
            # Check for expensive operations in loops
            issues.extend(self._find_expensive_operations(tree, code))
            
            # Check for unused imports
            issues.extend(self._find_unused_imports(tree, code))
            
        except SyntaxError:
            pass
        
        return {'issues': issues}
    
    def _find_nested_loops(self, tree):
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                # Check if this loop contains another loop
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.For, ast.While)):
                        issues.append("Nested loops detected - consider optimization")
                        break
        return issues
    
    def _find_expensive_operations(self, tree, code):
        issues = []
        expensive_calls = ['re.compile', 'sorted(', 'list.sort(']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Simple check for expensive operations
                call_code = ast.get_source_segment(code, node)
                if call_code:
                    for expensive in expensive_calls:
                        if expensive in call_code:
                            issues.append(f"Expensive operation '{expensive}' found")
                            break
        return issues
    
    def _find_unused_imports(self, tree, code):
        issues = []
        imported_names = set()
        used_names = set()
        
        # Find all imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_names.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_names.add(alias.name)
            
            # Find name usage
            if isinstance(node, ast.Name):
                used_names.add(node.id)
        
        # Check for unused imports
        for imported in imported_names:
            if imported not in used_names:
                issues.append(f"Unused import: {imported}")
        
        return issues