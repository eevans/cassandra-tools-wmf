
import logging
import subprocess

from .config import DRY_RUN


def call(*args):
    if DRY_RUN:
        logging.info("%s (dry-run)", " ".join(list(args)))
        return 0
    else:
        return subprocess.call(list(args))
