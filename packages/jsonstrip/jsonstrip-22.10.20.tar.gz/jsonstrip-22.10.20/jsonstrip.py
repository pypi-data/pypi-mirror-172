"""
Strip JSON comments while keeping the line/column positions of JSON text intact.

Author: Vlado Potisk
License: MIT
Project homepage: https://github.com/xitop/jsonstrip
"""

import enum

__all__ = ['strip']

State = enum.Enum('State',
    'JSON STRING ESCAPE SLASH SL_COMMENT ML_COMMENT ML_COMMENT_END')
Cmd = enum.Enum('Cmd',
    'FLUSH0 FLUSH1 ECHO BLANK START0 START1')
DEFAULT = None  # anything but a valid char

TRANS = {
    State.JSON: {
        '/': (State.SLASH,),
        '"': (State.STRING,),
        '#': (State.SL_COMMENT, Cmd.FLUSH0),
    },
    State.STRING: {
        '\\': (State.ESCAPE,),
        '"': (State.JSON,),
    },
    State.ESCAPE: {
        DEFAULT: (State.STRING,),
    },
    State.SLASH: {
        '/': (State.SL_COMMENT, Cmd.FLUSH1),
        '*': (State.ML_COMMENT, Cmd.FLUSH1),
        '#': (State.SL_COMMENT, Cmd.FLUSH0),    # can't be valid JSON
        DEFAULT: (State.JSON,),
    },
    State.SL_COMMENT: {
        '\r': (State.JSON, Cmd.START0),
        '\n': (State.JSON, Cmd.START0),
    },
    State.ML_COMMENT: {
        '\r': (Cmd.ECHO, Cmd.START1),
        '\n': (Cmd.ECHO, Cmd.START1),
        '*': (State.ML_COMMENT_END,),
    },
    State.ML_COMMENT_END: {
        '/': (State.JSON, Cmd.BLANK, Cmd.START1),
        '*': (),
        DEFAULT: (State.ML_COMMENT,),
    },
}

def strip(json_str: str) -> str:
    """
    Remove comments from a JSON document.

    Removed are:
        /* JS multi-line comments */
        // JS single-line comments
        # line comments

    Add whitespace where necessary to keep the text position
    (i.e. line/column numbers) unchanged.
    """
    result = []
    pos = 0
    state = State.JSON
    trans = TRANS[state]
    for i, ch in enumerate(json_str):
        # not using try-except, because frequent KeyErrors slow down parsing
        if ch in trans:
            new = trans[ch]
        elif DEFAULT in trans:
            new = trans[DEFAULT]
        else:
            continue
        for n in new:
            if isinstance(n, State):
                state = n
                trans = TRANS[state]
            elif n is Cmd.ECHO:
                result.append(ch)
            elif n is Cmd.START0:
                pos = i
            elif n is Cmd.START1:
                pos = i + 1
            elif n is Cmd.FLUSH0:
                result.append(json_str[pos:i])
                pos = i
            elif n is Cmd.FLUSH1:
                result.append(json_str[pos:i-1])
                pos = i - 1
            elif n is Cmd.BLANK:
                result.append(' ' * (i - pos + 1))
    if state not in {State.SL_COMMENT, State.ML_COMMENT, State.ML_COMMENT_END}:
        result.append(json_str[pos:])
    return "".join(result)


if __name__ == "__main__":
    import sys
    print(strip(sys.stdin.read()), end="")
