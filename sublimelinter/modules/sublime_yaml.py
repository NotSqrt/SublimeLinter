# example error messages
#
# ParserError : expected the node content, but found ']' while parsing a block node
# ScannerError : could not found expected ':' while scanning a simple key

"""
bad syntax example 1: "unbalanced blackets: ]["
bad syntax example 2:
'''
- elem1
elem2
'''

requires pyyaml

stops at the first error
"""

from base_linter import BaseLinter

try:
    import yaml
    PYYAML_AVAILABLE = True
except ImportError:
    PYYAML_AVAILABLE = False


CONFIG = {
    'language': 'YAML'
}


class ErrorType:
    WARNING = 'warning'
    VIOLATION = 'violation'
    ERROR = 'error'


class Linter(BaseLinter):

    def get_executable(self, view):
        return (PYYAML_AVAILABLE, None, 'built in' if PYYAML_AVAILABLE else 'the yaml module could not be imported')

    def built_in_check(self, view, code, filename):

        errors = []

        if PYYAML_AVAILABLE:
            try:
                yaml.safe_load(code)
            except yaml.YAMLError, exc:
                if hasattr(exc, 'problem_mark'):
                    mark = exc.problem_mark

                    errors.append({
                        'type': ErrorType.ERROR,
                        'message': '%s : %s %s' % (type(exc).__name__, exc.problem, exc.context),
                        'lineno': mark.line+1,
                        'col': mark.column+1,
                    })

        return errors

    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):

        for error in errors:
            error_type = error.get('type', ErrorType.ERROR)
            col = error.get('col', 0)

            messages = {
                ErrorType.WARNING: warningMessages,
                ErrorType.VIOLATION: violationMessages,
                ErrorType.ERROR: errorMessages,
            }[error_type]

            underlines = {
                ErrorType.WARNING: warningUnderlines,
                ErrorType.VIOLATION: violationUnderlines,
                ErrorType.ERROR: errorUnderlines,
            }[error_type]

            self.add_message(error['lineno'], lines, error['message'], messages)
            self.underline_range(view, error['lineno'], col, underlines, length=1)
