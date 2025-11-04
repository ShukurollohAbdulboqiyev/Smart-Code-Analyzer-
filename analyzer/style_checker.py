import re

class StyleChecker:
    def check_style(self, code):
        """Check code style against PEP8"""
        violations = []
        lines = code.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 79:
                violations.append(f"Line {i}: Line too long ({len(line)} > 79 characters)")
            
            # Check for trailing whitespace
            if line.rstrip() != line:
                violations.append(f"Line {i}: Trailing whitespace")
            
            # Check for multiple spaces around operator
            if re.search(r'[^=!<>]\s\s+[=!<>]', line):
                violations.append(f"Line {i}: Multiple spaces around operator")
        
        # Check function naming convention
        function_pattern = r'def ([a-z_][a-z0-9_]*)'
        functions = re.findall(function_pattern, code)
        for func in functions:
            if not self._is_snake_case(func):
                violations.append(f"Function '{func}' should be snake_case")
        
        return {'violations': violations, 'pep8_compliance': len(violations) == 0}
    
    def _is_snake_case(self, name):
        return re.match(r'^[a-z_][a-z0-9_]*$', name) is not None