cassandra-tools-wmf
===================

Cluster management tools for [Apache Cassandra](http://cassandra.apache.org).

The tools
---------
 * `c-any-nt <arg> [arg ...]`

   Execute nodetool on an instance (any instance).
   
 * `c-cqlsh <id>`

   Execute `cqlsh` on an instance (uses the cqlshrc file in the instance's
   configuration directory).

 * `c-foreach-nt <arg> [arg ...]`

   Iteratively execute nodetool on all local Cassandra instances.

 * `c-foreach-restart [-r RETRIES] [-d DELAY] [--execute-post-shutdown CMD]`

   Iteratively restart Cassandra instances.

   Each instance is drained prior to being restarted.  After each restart, the
   process will block until the CQL port opens up.

   Any command specified using `--execute-post-shutdown` will be executed after
   Cassandra is shutdown, and before it is restarted.  Commands can include the
   `{id}` template which will be substituted with the instance being restarted
   before executing the command.

 * `c-ls`

   List the locally configured instance IDs.

 * `streams [--nodetool CMD]`

   Realtime console monitoring of streaming operations.

 * `uyaml <yaml file> <attribute>`

   Query attributes from a yaml file.


Building a Debian package
-------------------------
    $ git checkout master
    $ make orig.tar.gz
    $ git checkout debian
    $ git merge master
    $ # Update debian/changelog accordingly
    $ dpkg-buildpackage -rfakeroot # or alternately...
    $ gbp buildpackage -rfakeroot -us -uc --git-upstream-branch=master --git-debian-branch=debian
    
