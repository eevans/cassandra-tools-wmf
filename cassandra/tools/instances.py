
from contextlib import closing

import logging
import os
import socket
import yaml

from time      import sleep

from .commands import call
from .config   import DESCRIPTOR_DIR
from .nodetool import Nodetool


def __get_descriptor_files():
    for descr in os.listdir(DESCRIPTOR_DIR):
        if descr.endswith("yaml") or descr.endswith("yml"):
            yield os.path.join(DESCRIPTOR_DIR, descr)

def get_instances():
    for descr in __get_descriptor_files():
        yield Instance(descr)


class Instance(object):
    def __init__(self, descr):
        with open(descr) as fobj:
            obj = yaml.load(fobj)

        def __get(key):
            if not obj.has_key(key):
                raise RuntimeError("{} is missing attribute {}".format(descr, key))
            return obj[key]

        self.name = __get("name")
        self.listen_address = __get("listen_address")
        self.native_transport_port = __get("native_transport_port")
        self.rpc_address = __get("rpc_address")
        self.service_name = __get("service_name")
        self.jmx_port = __get("jmx_port")

        self.nodetool = Nodetool(self.listen_address, self.jmx_port)

    """
    Restart this Cassandra instance.
    """
    def restart(self):
        self.__log_info("Shutting down client ports...")
        self.nodetool.disablebinary()
        self.nodetool.disablethrift()
        self.__log_info("Draining...")
        self.nodetool.drain()
        self.__log_info("Restarting service %s", self.service_name)
        call("systemctl", "restart", self.service_name)
        listening = False
        # TODO: The number of retries and timeout used should be configurable
        for i in range(0, 10):
            logging.debug("Testing CQL port (attempt #%s)", (i + 1))
            if self.listening(self.rpc_address, self.native_transport_port):
                logging.info("CQL (%s:%s) is UP", self.rpc_address, self.native_transport_port)
                listening = True
                break
            sleep(2)
        if not listening:
            logging.error("CQL (%s:%s) DOWN", self.rpc_address, self.native_transport_port)
            raise Exception("{} restart FAILED".format(self.service_name))

    def __log_info(self, msg, *args, **kwargs):
        self.__log(logging.INFO, msg, *args, **kwargs)

    def __log(self, level, msg, *args, **kwargs):
        logging.log(level, "[{}] {}".format(self.name, msg), *args, **kwargs)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Instance(name={}, listen_address={})".format(self.name, self.listen_address)

    """
    Perform a simple TCP port check.
    """
    @classmethod
    def listening(cls, host, port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            return sock.connect_ex((host, port)) == 0
