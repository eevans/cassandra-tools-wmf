cassandra-tools-wmf
===================

Cluster management tools for [Apache Cassandra](http://cassandra.apache.org).

Debian package
--------------
    $ git checkout master
    $ make orig.tar.gz
    $ git checkout debian
    $ git merge master
    $ # Update debian/changelog accordingly
    $ dpkg-buildpackage -rfakeroot
