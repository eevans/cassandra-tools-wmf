
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
    for descr in sorted(os.listdir(DESCRIPTOR_DIR)):
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
    def restart(self, retries=10, delay=6):
        self.__log_debug("Restarting instance... (retries=%s, delay=%s)", retries, delay)
        self.__log_info("Disabling client ports...")
        self.nodetool.run("disablebinary")
        self.nodetool.run("disablethrift")
        self.__log_info("Draining...")
        self.nodetool.run("drain")
        self.__log_info("Restarting service %s", self.service_name)
        call("systemctl", "restart", self.service_name)
        listening = False
        for i in range(0, retries):
            logging.debug("Testing CQL port (attempt #%s)", (i + 1))
            if self.listening(self.rpc_address, self.native_transport_port):
                self.__log_info("CQL (%s:%s) is UP", self.rpc_address, self.native_transport_port)
                listening = True
                break
            elif (i % 2) == 0 and i < 9:
                self.__log_warn(
                    "CQL (%s:%s) not listening (will retry)...",
                    self.rpc_address,
                    self.native_transport_port
                )
            sleep(delay)
        if not listening:
            self.__log_error("CQL (%s:%s) DOWN", self.rpc_address, self.native_transport_port)
            raise Exception("{} restart FAILED".format(self.service_name))

    def __log_debug(self, msg, *args, **kwargs):
        self.__log(logging.DEBUG, msg, *args, **kwargs)

    def __log_info(self, msg, *args, **kwargs):
        self.__log(logging.INFO, msg, *args, **kwargs)

    def __log_warn(self, msg, *args, **kwargs):
        self.__log(logging.WARN, msg, *args, **kwargs)

    def __log_error(self, msg, *args, **kwargs):
        self.__log(logging.ERROR, msg, *args, **kwargs)

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
