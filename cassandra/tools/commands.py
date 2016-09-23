
import logging

from subprocess import Popen, PIPE

from .config import DRY_RUN


def call(*args):
    if DRY_RUN:
        logging.info("%s (dry-run)", " ".join(list(args)))
        return 0
    else:
        process = Popen(args, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = process.communicate()
        return (process.returncode, stdout, stderr)
