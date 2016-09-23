
import logging
import subprocess

from .config import DRY_RUN


def __ansi_color(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner


RED     = __ansi_color("31")
GREEN   = __ansi_color("32")
YELLOW  = __ansi_color("33")
BLUE    = __ansi_color("34")
MAGENTA = __ansi_color("35")
CYAN    = __ansi_color("36")
WHITE   = __ansi_color("37")


def call(*args, **kwargs):
    if DRY_RUN:
        logging.info("%s (dry-run)", " ".join(list(args)))
        return 0
    else:
        return subprocess.call(list(args))
