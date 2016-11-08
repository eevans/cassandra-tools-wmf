

import getpass
import logging
import socket


# Cribbed from: https://phabricator.wikimedia.org/diffusion/MSCA/browse/master/scap/log.py;d407eaf
class IrcBot(object):
    def __init__(self, host, port, timeout=1.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def log(self, msg, *args, **kwargs):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.host, self.port))
            sock.sendall(IrcBot.format_message(msg, *args, **kwargs))
        except (socket.timeout, socket.error, socket.gaierror), err:
            logging.error(
                "Unable to send to logmsgbot (SAL): socket.error (%s) %s",
                err.errno,
                err.strerror
            )
        finally:
            if sock:
                sock.close()

    @classmethod
    def format_message(cls, msg, *args, **kwargs):
        username = getpass.getuser()
        hostname = socket.gethostbyaddr(socket.gethostname())[0]
        return "!log {}@{}: ".format(username, hostname) + msg.format(*args, **kwargs)
