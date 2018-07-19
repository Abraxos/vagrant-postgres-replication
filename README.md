# Fault Tolerant Logical Replication with PostGreSQL and Zookeeper

This is a proof-of-concept. It is designed to go together with my write-up of all that I learned while doing this here: https://eugene.kovalev.systems/blog/postgres10_cluster

## Useful

**Postgres Query to insert auto-generated, unique data:** `insert into random_data (timestamp, uuid) values(localtimestamp, CAST(uuid_generate_v4() AS VARCHAR(36)));`
**Get publication information:** `SELECT * FROM pg_stat_replication;`
**Get subscription information:** `SELECT * FROM pg_stat_subscription;`

## References

### PostgreSQL

+ PostGreSQL Documentation Chapter 31 - Logical Replication: https://www.postgresql.org/docs/10/static/logical-replication.html
+ Logical Replication Quick Setup: https://www.postgresql.org/docs/10/static/logical-replication-quick-setup.html
+ Logical Replication in PostgreSQL 10 by 2ndQuadrant: https://blog.2ndquadrant.com/logical-replication-postgresql-10/
+ Alter System Command: https://www.postgresql.org/docs/10/static/sql-altersystem.html
+ Alter Subscription: https://www.postgresql.org/docs/10/static/sql-altersubscription.html
+ Alter Publication: https://www.postgresql.org/docs/10/static/sql-alterpublication.html
+ Drop Publication: https://www.postgresql.org/docs/10/static/sql-droppublication.html
+ Create Publication: https://www.postgresql.org/docs/10/static/sql-createpublication.html
+ Create Subscription: https://www.postgresql.org/docs/10/static/sql-createsubscription.html

My Question on DBA Stack Exchange: https://dba.stackexchange.com/questions/199316/postgres-10-logical-replication-without-truncating-existing-table

### Tooz

+ Tooz on PyPi: https://pypi.python.org/pypi/tooz
+ Module reference: https://docs.openstack.org/tooz/latest/reference/index.html
+ Leader Election: https://docs.openstack.org/tooz/latest/user/tutorial/leader_election.html
+ User Documentation: https://docs.openstack.org/tooz/latest/user/index.html

### Zookeeper

+ Zookeeper/Linux DNS Name Problem: https://unix.stackexchange.com/questions/240506/zookeeper-dns-name-problems-with-leader-elections-when-migrating-from-windows-to
+ Zookeeper Server Issues: https://stackoverflow.com/questions/36361613/zookeeper-server-not-running
+ Zookeeper Documentation: https://zookeeper.apache.org/
