
import logging

from os import environ


__all__ = ["DESCRIPTOR_DIR", "DRY_RUN", "LOG_LEVEL"]

DESCRIPTOR_DIR = environ.get("DESCRIPTOR_DIR", "/etc/cassandra-instances.d")
DRY_RUN = environ.get("DRY_RUN", "0").lower() in ("true", "1", "yes", "y")


def __get_log_level(level):
    if not level.upper() in ("DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL", "FATAL"):
        raise RuntimeError("Invalid logging level")
    return getattr(logging, level.upper())


LOG_LEVEL = __get_log_level(environ.get("LOG_LEVEL", "INFO"))
