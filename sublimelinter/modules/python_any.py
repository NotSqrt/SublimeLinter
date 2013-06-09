from base_linter import BaseLinter

import re
import os
import json

CONFIG = {
    'language': 'python_any',
    'executable': 'python',  # or path to the adequate python version
    'lint_args': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs', 'pythoncheck.py')
}


class Linter(BaseLinter):

    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        def underline_duplicate_argument(lineno, word, underlines):
            "from python.py linter : interpret the errors exactly as in the python linter"
            regex = 'def [\w_]+\(.*?(?P<underline>[\w]*{0}[\w]*)'.format(re.escape(word))
            self.underline_regex(view, lineno, regex, lines, underlines, word)

        for line in errors.splitlines():
            error = json.loads(line)

            self.add_message(error.get('line'), lines, error.get('msg'), errorMessages)

            if error.get('class') == u'OffsetError':
                self.underline_range(view, error.get('line'), error.get('offset'), errorUnderlines)

            elif error.get('class') == u'DuplicateArgument':  # same as pyflakes.messages.DuplicateArgument
                underline_duplicate_argument(error.get('line'), error.get('arg'), errorUnderlines)
