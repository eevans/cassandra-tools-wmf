

import logging

from .commands import call


class Nodetool(object):
    def __init__(self, host, port):
        self.host = host
        self.port = str(port)

    def run(self, *args):
        command = ["nodetool", "--host", self.host, "--port", self.port] + list(args)
        retcode = call(*command)
        if retcode != 0:
            raise NodetoolCmdException("nodetool returned status {}".format(retcode))

class NodetoolCmdException(Exception):
    pass
