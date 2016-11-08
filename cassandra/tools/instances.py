
"""
Cassandra instances.
"""

from contextlib import closing

import logging
import os
import socket
from   subprocess import Popen, PIPE
from   time       import sleep
import yaml

from .config    import DESCRIPTOR_DIR
from .nodetool  import Nodetool


def __get_descriptor_files():
    for descr in sorted(os.listdir(DESCRIPTOR_DIR)):
        if descr.endswith("yaml") or descr.endswith("yml"):
            yield os.path.join(DESCRIPTOR_DIR, descr)

def get_instances():
    """
    Iterates over configured local Cassandra instances.
    """
    for descr in __get_descriptor_files():
        yield Instance(descr)

class Instance(object):
    """
    A Cassandra instance.
    """
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

    def restart(self, attempts=10, retry=6, post_shutdown=None):
        """
        Restarts this Cassandra instance.
        """
        self.__log_debug("Restarting instance... (attempts=%s, retry=%s)", attempts, retry)
        self.__log_info("Disabling client ports...")
        self.nodetool.run("disablebinary")
        self.nodetool.run("disablethrift")
        self.__log_info("Draining...")
        self.nodetool.run("drain")

        # Restart Cassandra
        self.__log_info("Stopping service %s", self.service_name)
        self.__execute_command("systemctl stop {}".format(self.service_name))

        # If an `execute-post-shutdown' command was given, run it too.
        if post_shutdown:
            self.__log_info("Executing post-shutdown command: %s", post_shutdown)
            self.__execute_command(post_shutdown.strip().format(id=self.name))

        self.__log_info("Starting service %s", self.service_name)
        self.__execute_command("systemctl start {}".format(self.service_name))

        # Wait for Cassandra to come back up before continuing
        listening = False
        for i in range(0, attempts):
            logging.debug("Testing CQL port (attempt #%s)", (i + 1))
            if self.listening(self.rpc_address, self.native_transport_port):
                self.__log_info("CQL (%s:%s) is UP", self.rpc_address, self.native_transport_port)
                listening = True
                break
            elif (i % 2) == 0 and i < 9:
                self.__log_warn(
                    "CQL (%s:%s) not listening (will retry)...",
                    self.rpc_address,
                    self.native_transport_port)
            sleep(retry)
        if not listening:
            self.__log_error("CQL (%s:%s) DOWN", self.rpc_address, self.native_transport_port)
            raise Exception("{} restart FAILED".format(self.service_name))

    # XXX: This is a hot mess.
    def __execute_command(self, cmd):
        assert isinstance(cmd, str)
        command = cmd.strip()
        processes = {}
        current = None
        exe = None

        # If command contains pipes, wire this up as a chain of Popen objs
        if '|' in command:
            previous = None
            for sub in command.split('|'):
                stdout = PIPE
                if previous:
                    assert isinstance(previous, Popen)
                    stdout = previous.stdout
                parts = sub.split()
                exe = parts[0]
                current = Popen(parts, stdin=stdout, stdout=PIPE, stderr=PIPE)
                processes[exe] = current
                previous = current
        else:
            parts = command.split()
            exe = parts[0]
            current = Popen(parts, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            processes[exe] = current

        # First, handle the command at the end of the chain
        output, error = current.communicate()

        self.__log_lines(logging.INFO, output)
        self.__log_lines(logging.ERROR, error)

        if current.returncode != 0:
            self.__log_error("%s command returned exit code %s", exe, current.returncode)
            raise RuntimeError("{} returned exit code {}".format(exe, current.returncode))

        # Handle any failures earlier in the chain
        for (name, process) in processes.items():
            process.wait()
            if process.returncode != 0:
                (_, error) = process.communicate()
                self.__log_lines(logging.ERROR, error)
                self.__log_error("%s command returned exit code %s", name, process.returncode)
                raise RuntimeError("{} returned exit code {}".format(name, process.returncode))

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

    def __log_lines(self, level, message):
        """
        Breaks a message into lines, and logs each individually.
        """
        lines = message.rstrip()
        if lines:
            for line in lines.splitlines():
                self.__log(level, line)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Instance(name={}, listen_address={})".format(self.name, self.listen_address)

    @classmethod
    def listening(cls, host, port):
        """
        Perform a simple TCP port check.
        """
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            return sock.connect_ex((host, port)) == 0
