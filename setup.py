
from distutils.core import setup


setup(
    name="cassandra",
    version="1.0.0",
    packages=["cassandra", "cassandra.tools"],
    scripts=["c-foreach-restart"]
)
