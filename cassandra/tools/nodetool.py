
import logging

from .commands import call


class Nodetool(object):
    def __init__(self, host, port):
        self.host = host
        self.port = str(port)

    def disablebinary(self):
        logging.debug("Disabling binary protocol (%s:%s)", self.host, self.port)
        self.__run("disablebinary")

    def disablethrift(self):
        logging.debug("Disabling thrift (%s:%s)", self.host, self.port)
        self.__run("disablethrift")

    def drain(self):
        logging.debug("Performing drain (%s:%s)", self.host, self.port)
        self.__run("drain")

    def __run(self, *args):
        command = ["nodetool", "--host", self.host, "--port", self.port] + list(args)
        retcode = call(*command)
        if retcode != 0:
            raise NodetoolCmdException("nodetool returned status {}".format(retcode))

class NodetoolCmdException(Exception):
    pass
