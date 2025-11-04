#!/usr/bin/env python3
"""
AI-Powered Code Analyzer
A comprehensive tool for analyzing Python code quality, security, and performance.
"""

import argparse
import os
import sys
from pathlib import Path
from analyzer.code_metrics import CodeMetrics
from analyzer.security_scanner import SecurityScanner
from analyzer.performance_analyzer import PerformanceAnalyzer
from analyzer.style_checker import StyleChecker

class CodeAnalyzer:
    def __init__(self):
        self.metrics = CodeMetrics()
        self.security = SecurityScanner()
        self.performance = PerformanceAnalyzer()
        self.style = StyleChecker()
    
    def analyze_file(self, file_path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            
            analysis = {
                'file': file_path,
                'metrics': self.metrics.analyze(code),
                'security': self.security.scan(code),
                'performance': self.performance.check(code),
                'style': self.style.check_style(code),
                'overall_score': 0
            }
            
            # Calculate overall score
            analysis['overall_score'] = self._calculate_score(analysis)
            
            return analysis
            
        except Exception as e:
            return {'error': f"Could not analyze {file_path}: {str(e)}"}
    
    def analyze_directory(self, directory_path):
        """Analyze all Python files in a directory"""
        results = []
        python_files = list(Path(directory_path).rglob("*.py"))
        
        print(f"🔍 Found {len(python_files)} Python files to analyze...")
        
        for file_path in python_files:
            print(f"📄 Analyzing {file_path}...")
            result = self.analyze_file(file_path)
            results.append(result)
        
        return results
    
    def _calculate_score(self, analysis):
        """Calculate overall code quality score (0-100)"""
        if 'error' in analysis:
            return 0
            
        score = 100
        
        # Deduct for security issues
        score -= len(analysis['security']['issues']) * 5
        
        # Deduct for performance issues
        score -= len(analysis['performance']['issues']) * 3
        
        # Deduct for style violations
        score -= len(analysis['style']['violations']) * 2
        
        # Reward for good metrics
        if analysis['metrics']['maintainability_index'] > 80:
            score += 10
        if analysis['metrics']['comment_ratio'] > 20:
            score += 5
            
        return max(0, min(100, score))
    
    def generate_report(self, results):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*60)
        print("🚀 CODE ANALYSIS REPORT")
        print("="*60)
        
        total_files = len(results)
        avg_score = sum(r.get('overall_score', 0) for r in results) / total_files
        
        print(f"📊 Total Files Analyzed: {total_files}")
        print(f"⭐ Average Quality Score: {avg_score:.1f}/100")
        print("\n" + "-"*60)
        
        for result in results:
            if 'error' in result:
                print(f"❌ {result['error']}")
                continue
                
            print(f"\n📁 File: {result['file']}")
            print(f"   🎯 Overall Score: {result['overall_score']}/100")
            print(f"   📏 Lines: {result['metrics']['line_count']}")
            print(f"   🔧 Functions: {result['metrics']['function_count']}")
            print(f"   🏛️ Classes: {result['metrics']['class_count']}")
            print(f"   💬 Comments: {result['metrics']['comment_ratio']:.1f}%")
            print(f"   🧠 Complexity: {result['metrics']['cyclomatic_complexity']}")
            print(f"   ⭐ Maintainability: {result['metrics']['maintainability_index']:.1f}")
            print(f"   🔒 Security: {len(result['security']['issues'])} issues ({result['security']['risk_level']} risk)")
            print(f"   ⚡ Performance: {len(result['performance']['issues'])} issues")
            print(f"   🎨 Style: {len(result['style']['violations'])} violations")
            
            # Show security issues if any
            for issue in result['security']['issues']:
                print(f"      ⚠️ {issue}")
            
            # Show performance issues if any
            for issue in result['performance']['issues']:
                print(f"      🐢 {issue}")
            
            # Show style violations if any
            for violation in result['style']['violations'][:3]:  # Show first 3
                print(f"      🎯 {violation}")

def main():
    parser = argparse.ArgumentParser(description='AI-Powered Code Analyzer')
    parser.add_argument('path', help='Path to Python file or directory')
    parser.add_argument('--output', '-o', help='Output file for report')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"❌ Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    analyzer = CodeAnalyzer()
    
    if os.path.isfile(args.path) and args.path.endswith('.py'):
        results = [analyzer.analyze_file(args.path)]
    elif os.path.isdir(args.path):
        results = analyzer.analyze_directory(args.path)
    else:
        print("❌ Error: Please provide a Python file or directory")
        sys.exit(1)
    
    analyzer.generate_report(results)

if __name__ == "__main__":
    main()
