
import logging
import sys

from subprocess import Popen, PIPE

from .config import DRY_RUN


def __ansi_color(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

def __no_color(output):
    return output

red     = __ansi_color("31")
green   = __ansi_color("32")
yellow  = __ansi_color("33")
blue    = __ansi_color("34")
magenta = __ansi_color("35")
cyan    = __ansi_color("36")
white   = __ansi_color("37")


def call(*args, **kwargs):
    color = kwargs.get("color", __no_color)

    if DRY_RUN:
        logging.info("%s (dry-run)", " ".join(list(args)))
        return 0
    else:
        process = Popen(args, stdout=PIPE, stderr=PIPE)

        (stdout, stderr) = process.communicate()

        if stdout:
            sys.stdout.write(color(stdout))
        if stderr:
            sys.stderr.write(color(stderr, True))

        return process.returncode
