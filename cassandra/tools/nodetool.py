
from .commands import call


class Nodetool(object):
    def __init__(self, host, port):
        self.host = host
        self.port = str(port)

    def run(self, *args, **kwargs):
        command = ["nodetool", "--host", self.host, "--port", self.port] + list(args)
        retcode = call(*command, color=kwargs.get("color"))
        if retcode != 0:
            raise NodetoolCmdException("nodetool returned status {}".format(retcode))

class NodetoolCmdException(Exception):
    pass
