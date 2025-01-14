import ast
import os
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CodeIssue:
    """Class to represent a code issue found during review."""
    file_path: str
    line_number: int
    issue_type: str
    message: str
    severity: str

class CodeReviewTool:
    def __init__(self):
        self.issues: List[CodeIssue] = []
        
    def review_file(self, file_path: str) -> List[CodeIssue]:
        """Review a single file for code issues."""
        if not file_path.endswith('.py'):
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Parse the code into an AST
            tree = ast.parse(content)
            
            # Reset issues for this file
            self.issues = []
            
            # Run various checks
            self._check_line_length(content, file_path)
            self._check_naming_conventions(tree, file_path)
            self._check_complexity(tree, file_path)
            self._check_docstrings(tree, file_path)
            self._check_import_style(content, file_path)
            
            return self.issues
            
        except Exception as e:
            self.issues.append(CodeIssue(
                file_path=file_path,
                line_number=0,
                issue_type='ERROR',
                message=f'Failed to parse file: {str(e)}',
                severity='HIGH'
            ))
            return self.issues
    
    def review_directory(self, directory_path: str) -> Dict[str, List[CodeIssue]]:
        """Review all Python files in a directory and its subdirectories."""
        results = {}
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    results[file_path] = self.review_file(file_path)
        return results

    def _check_line_length(self, content: str, file_path: str, max_length: int = 79):
        """Check if any lines exceed the maximum length."""
        for i, line in enumerate(content.split('\n'), 1):
            if len(line) > max_length:
                self.issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='LINE_LENGTH',
                    message=f'Line length exceeds {max_length} characters',
                    severity='LOW'
                ))

    def _check_naming_conventions(self, tree: ast.AST, file_path: str):
        """Check naming conventions for variables, functions, and classes."""
        class NamingConventionChecker(ast.NodeVisitor):
            def __init__(self, review_tool):
                self.review_tool = review_tool

            def visit_ClassDef(self, node):
                if not node.name[0].isupper():
                    self.review_tool.issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=node.lineno,
                        issue_type='NAMING_CONVENTION',
                        message=f'Class name "{node.name}" should use CapWords convention',
                        severity='MEDIUM'
                    ))
                self.generic_visit(node)

            def visit_FunctionDef(self, node):
                if not node.name.islower() and '_' not in node.name:
                    self.review_tool.issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=node.lineno,
                        issue_type='NAMING_CONVENTION',
                        message=f'Function name "{node.name}" should use lowercase_with_underscores',
                        severity='MEDIUM'
                    ))
                self.generic_visit(node)

        checker = NamingConventionChecker(self)
        checker.visit(tree)

    def _check_complexity(self, tree: ast.AST, file_path: str, max_complexity: int = 10):
        """Check cyclomatic complexity of functions."""
        class ComplexityChecker(ast.NodeVisitor):
            def __init__(self, review_tool):
                self.review_tool = review_tool

            def visit_FunctionDef(self, node):
                complexity = 1  # Base complexity
                # Count branches
                for n in ast.walk(node):
                    if isinstance(n, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                        complexity += 1
                    elif isinstance(n, ast.BoolOp):
                        complexity += len(n.values) - 1

                if complexity > max_complexity:
                    self.review_tool.issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=node.lineno,
                        issue_type='COMPLEXITY',
                        message=f'Function "{node.name}" has complexity of {complexity} (max is {max_complexity})',
                        severity='HIGH'
                    ))
                self.generic_visit(node)

        checker = ComplexityChecker(self)
        checker.visit(tree)

    def _check_docstrings(self, tree: ast.AST, file_path: str):
        """Check for missing docstrings in functions and classes."""
        class DocstringChecker(ast.NodeVisitor):
            def __init__(self, review_tool):
                self.review_tool = review_tool

            def visit_FunctionDef(self, node):
                if not ast.get_docstring(node):
                    self.review_tool.issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=node.lineno,
                        issue_type='MISSING_DOCSTRING',
                        message=f'Function "{node.name}" is missing a docstring',
                        severity='LOW'
                    ))
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                if not ast.get_docstring(node):
                    self.review_tool.issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=node.lineno,
                        issue_type='MISSING_DOCSTRING',
                        message=f'Class "{node.name}" is missing a docstring',
                        severity='LOW'
                    ))
                self.generic_visit(node)

        checker = DocstringChecker(self)
        checker.visit(tree)

    def _check_import_style(self, content: str, file_path: str):
        """Check import statement style and organization."""
        lines = content.split('\n')
        import_lines = []
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append((i, line.strip()))

        # Check for multiple imports on one line
        for line_num, line in import_lines:
            if ',' in line and not 'import {' in line:  # Ignore f-strings or formatted strings
                self.issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=line_num,
                    issue_type='IMPORT_STYLE',
                    message='Multiple imports on one line should be split',
                    severity='LOW'
                ))

def generate_report(issues: Dict[str, List[CodeIssue]]) -> str:
    """Generate a formatted report from the code review results."""
    report = "Code Review Report\n"
    report += "=================\n\n"
    
    total_issues = sum(len(file_issues) for file_issues in issues.values())
    report += f"Total files analyzed: {len(issues)}\n"
    report += f"Total issues found: {total_issues}\n\n"
    
    for file_path, file_issues in issues.items():
        if file_issues:
            report += f"\nFile: {file_path}\n"
            report += "-" * (len(file_path) + 6) + "\n"
            
            # Group issues by severity
            severity_groups = {
                'HIGH': [],
                'MEDIUM': [],
                'LOW': []
            }
            
            for issue in file_issues:
                severity_groups[issue.severity].append(issue)
            
            for severity in ['HIGH', 'MEDIUM', 'LOW']:
                if severity_groups[severity]:
                    report += f"\n{severity} Priority Issues:\n"
                    for issue in severity_groups[severity]:
                        report += f"- Line {issue.line_number}: {issue.message} ({issue.issue_type})\n"
    
    return report

# Example usage
if __name__ == "__main__":
    reviewer = CodeReviewTool()
    
    # Example of reviewing a single file
    file_path = "example.py"
    issues = reviewer.review_file(file_path)
    
    # Example of reviewing an entire directory
    directory_path = "project/"
    all_issues = reviewer.review_directory(directory_path)
    
    # Generate and print the report
    report = generate_report(all_issues)
    print(report)
