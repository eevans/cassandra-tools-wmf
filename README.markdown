cassandra-tools-wmf
===================

Cluster management tools for [Apache Cassandra](http://cassandra.apache.org).


Table of contents
-----------------
- [The tools](#the-tools)
  - [c-cqlsh](#c-cqlsh)
  - [c-any-nt](#c-any-nt)
  - [c-foreach-nt](#c-foreach-nt)
  - [c-foreach-restart](#c-foreach-restart)
  - [c-ls](#c-ls)
  - [streams](#streams)
  - [uyaml](#uyaml)
- [Building a Debian package](#building-a-debian-package)


The tools
---------

### c-cqlsh
#### Synopsis
`c-cqlsh <id>`
#### Description
Given an instance ID, executes `cqlsh` on that instance.  Uses the the `cqlshrc` file located in the instance's configuration directory.
#### Example
    $ c-cqlsh a
    Connected to services-test at 10.64.0.202:9042.
    [cqlsh 5.0.1 | Cassandra 2.2.6 | CQL spec 3.3.1 | Native protocol v4]
    Use HELP for help.
    cassandra@cqlsh>

### c-any-nt
#### Synopsis
`c-any-nt <arg> [arg ...]`
#### Description
In a WMF multi-instance environment, executes nodetool on a randomly chosen instance (any instance).
#### Example
    $ c-any-nt status -r
    ...

### c-foreach-nt
#### Synopsis
`c-foreach-nt <arg> [arg ...]`
#### Description
In a WMF multi-instance environment, iteratively execute nodetool on all local Cassandra instances.
#### Example
    $ c-foreach-nt version
    a: ReleaseVersion: 2.2.6
    b: ReleaseVersion: 2.2.6

### c-foreach-restart
#### Synopsis
    c-foreach-restart [-h] [-r RETRIES] [-d DELAY] [--execute-post-shutdown CMD]
    
    Cassandra instance restarter.
    
    optional arguments:
      -h, --help            show this help message and exit
      -r RETRIES, --retries RETRIES
                            Maximum number of times to check if service is up.
      -d DELAY, --delay DELAY
                            Number seconds between connection attempts, in
                            seconds.
      --execute-post-shutdown CMD
                            Command to execute after Cassandra has been shutdown,
                            and before it is started back up.
    
#### Description
In a WMF multi-instance environment, iteratively restart instances.

Each instance is drained prior to being restarted.  After each restart, the process blocks
until the CQL port is listening.

Commands specified by `--execute-post-shutdown` can include the `{id}` template which will
be substituted with the ID of the instance being restarted.
#### Example
    $ sudo c-foreach-restart --execute-post-shutdown="echo '{id} is a teapot, short and stout'"
    ...

### c-ls
#### Synopsis
`c-ls`
#### Description
List the IDs of the locally configured instance IDs.
#### Example
    $ c-ls
    a
    b
    c

### streams
#### Synopsis
    streams [-h] [-nt CMD]
    
    Cassandra streams monitor
    
    optional arguments:
      -h, --help            show this help message and exit
      -nt CMD, --nodetool CMD
                            Nodetool command to use
    
#### Description
Realtime console monitoring of streaming operations.
#### Example
    $ streams -nt nodetool-b

### uyaml
#### Synopsis
    uyaml [-h] yaml path
    
    YAML parser
    
    positional arguments:
      yaml        YAML file to parse
      path        Path to parse from file
    
    optional arguments:
      -h, --help  show this help message and exit
    
#### Description
Query attributes from a YAML file.
#### Example
    $ uyaml /etc/cassandra-instances.d/restbase1007-a.yaml /jmx_port
    7189
    $ for i in `c-ls`; do uyaml /etc/cassandra-instances.d/restbase1007-$i.yaml /jmx_port; done
    7189
    7190
    7191


Building a Debian package
-------------------------
    $ git checkout master
    $ make orig.tar.gz
    $ git checkout debian
    $ git merge master
    $ # Update debian/changelog accordingly
    $ dpkg-buildpackage -rfakeroot # or alternately...
    $ gbp buildpackage -rfakeroot -us -uc --git-upstream-branch=master --git-debian-branch=debian
    
