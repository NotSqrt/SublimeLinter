import sys
import json
"""
This file has to be valid for the maximum number of python versions.
OK for python2.7, python3.3

The json library has to be importable.
Ok for python >= 2.7
Certainly not for python<2.6
For 2.6, this module is not called.
"""


def compile_for_sublimelinter():
    "massively inspired from the python linter module"

    code = sys.stdin.read()
    import _ast

    try:
        # useful if you need the tree, but duplicate arguments don't get raised
        tree = compile(code, '<string>', "exec", _ast.PyCF_ONLY_AST)
        # builds the tree into bytecode, raises duplicate argument errors
        compile(tree, '<string>', 'exec')
    except (SyntaxError, IndentationError) as value:
        msg = value.args[0]

        (lineno, offset, text) = value.lineno, value.offset, value.text

        # If there's an encoding problem with the file, the text is None.
        if text is None:
            # Avoid using msg, since for the only known case, it contains a
            # bogus message that claims the encoding the file declared was
            # unknown.
            if msg.startswith('duplicate argument'):
                arg = msg.split('duplicate argument ', 1)[1].split(' ', 1)[0].strip('\'"')
                error = {'class': 'DuplicateArgument', 'line': lineno, 'msg': msg, 'arg': arg}
            else:
                error = {'class': 'PythonError', 'line': lineno, 'msg': msg}
        else:
            line = text.splitlines()[-1]

            if offset is not None:
                offset = offset - (len(text) - len(line))

            if offset is not None:
                error = {'class': 'OffsetError', 'line': lineno, 'msg': msg, 'offset': offset}
            else:
                error = {'class': 'PythonError', 'line': lineno, 'msg': msg}
        return error
    except ValueError as e:
        return {'class': 'PythonError', 'line': 0, 'msg': e.args[0]}


def main():
    if len(sys.argv) == 2 and sys.argv[1] == '-v':
        # SublimeLinter is testing for the usability of this file
        pass
    else:
        error = compile_for_sublimelinter()
        if error:
            print(json.dumps(error))


if __name__ == '__main__':
    main()
