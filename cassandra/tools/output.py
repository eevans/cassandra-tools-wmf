
"""
Output-related functions.
"""

# pylint: disable=C0111
# pylint: disable=W0613

def __ansi_color(code):
    def inner(text, bold=False):
        inner_code = code
        if bold:
            inner_code = "1;%s" % inner_code
        return "\033[%sm%s\033[0m" % (inner_code, text)
    return inner

def __none(text, bold=False):
    return text


RED = __ansi_color("31")
GREEN = __ansi_color("32")
YELLOW = __ansi_color("33")
BLUE = __ansi_color("34")
MAGENTA = __ansi_color("35")
CYAN = __ansi_color("36")
WHITE = __ansi_color("37")
NONE = __none
