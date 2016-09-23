
def __ansi_color(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

def __none(text, bold=False):
    return text


RED     = __ansi_color("31")
GREEN   = __ansi_color("32")
YELLOW  = __ansi_color("33")
BLUE    = __ansi_color("34")
MAGENTA = __ansi_color("35")
CYAN    = __ansi_color("36")
WHITE   = __ansi_color("37")
NONE    = __none
