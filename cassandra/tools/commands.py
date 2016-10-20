
"""
Functions related to the invocation of commands.
"""

import logging

from subprocess import Popen, PIPE

from .config import DRY_RUN


def call(*args):
    """
    Invokes a command, and returns a 3-tuple containing the return code, and
    the contents of stdout and stderr respectively.
    """
    if DRY_RUN:
        logging.info("%s (dry-run)", " ".join(list(args)))
        return 0
    else:
        process = Popen(args, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = process.communicate()
        return (process.returncode, stdout, stderr)
