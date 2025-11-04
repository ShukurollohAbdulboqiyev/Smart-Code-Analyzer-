import ast
import re

class SecurityScanner:
    def scan(self, code):
        """Scan for security vulnerabilities"""
        issues = []
        
        # Check for dangerous functions
        dangerous_functions = [
            'eval', 'exec', 'input', 'pickle.loads', 'marshal.loads',
            'os.system', 'subprocess.call', 'execfile'
        ]
        
        for func in dangerous_functions:
            if func in code:
                issues.append(f"Use of dangerous function: {func}")
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
        ]
        
        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append("Potential hardcoded secret detected")
        
        # SQL injection patterns
        sql_patterns = [
            r"\.execute\s*\(\s*f?[\"'][^\"']*\%s",
            r"\.execute\s*\(\s*[\"'][^\"']*\+"
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, code):
                issues.append("Potential SQL injection vulnerability")
        
        return {'issues': issues, 'risk_level': self._calculate_risk_level(issues)}
    
    def _calculate_risk_level(self, issues):
        if not issues:
            return "LOW"
        elif len(issues) <= 2:
            return "MEDIUM"
        else:
            return "HIGH"