
"""
Abstractions for Cassanra's nodetool utility.
"""

from sys        import stdout, stderr

from .commands  import call
from .output    import RED, NONE


# pylint: disable=R0903
class Nodetool(object):
    """
    Nodetool interface for a Cassandra instance.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self, *args, **kwargs):
        """
        Invoke a nodetool subcommand.
        """
        writer = kwargs.get("output", NodetoolOutputWriter())
        assert isinstance(writer, NodetoolOutputWriter)

        command = ["nodetool", "--host", self.host, "--port", str(self.port)] + list(args)
        (retcode, output, error) = call(*command)

        writer.output(output)
        writer.error(error)

        if retcode != 0:
            raise NodetoolCommandException(
                "nodetool command returned exit code {}".format(retcode),
                retcode)

    def __repr__(self):
        return "Nodetool({}, {})".format(self.host, self.port)

    def __str__(self):
        return "{}:{}".format(self.host, self.port)

# pylint: enable=R0903

class NodetoolOutputWriter(object):
    """
    Writes nodetool output, optionally using ansi console colors and a
    provided prefix.
    """
    def __init__(self, color=None, bold=False, prefix=None):
        self.color = color if color else NONE
        self.bold = bold
        self.prefix = prefix

    def output(self, text):
        """
        Write text to standard output.
        """
        data = text.rstrip()
        if data:
            for line in data.split('\n'):
                print >>stdout, self.color("{}{}".format(self.__prefix(), line), self.bold)

    def error(self, text):
        """
        Write text to standard error.
        """
        data = text.rstrip()
        if data:
            for line in data.split('\n'):
                print >>stderr, RED("{}{}".format(self.__prefix(), line), True)

    def __prefix(self):
        return "{}: ".format(self.prefix) if self.prefix else ""

    def __repr__(self):
        return "NodetoolOutputWriter(prefix={})".format(self.prefix)

    def __str__(self):
        return repr(self)

class NodetoolCommandException(Exception):
    """
    Represents an error in invoking a nodetool command.
    """
    def __init__(self, message, retcode):
        self.retcode = retcode
        super(NodetoolCommandException, self).__init__(message)

