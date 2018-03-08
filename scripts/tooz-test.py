from tooz import coordination
import time
import arrow
from database import *
from socket import gethostname

leader = None

def configure_db_publish():
    configure_publisher()


def configure_db_subscribe(node):
    configure_subscriber(PG_NODES[node])


def configure_db_standalone():
    configure_standalone()


def on_group_join(event):
    print('{}-EVENT: {} joined {}'.format(gethostname(),
                                          event.member_id.decode(),
                                          event.group_id.decode()))

def on_group_leave(event):
    print('{}-EVENT: {} left {}'.format(gethostname(),
                                        event.member_id.decode(),
                                        event.group_id.decode()))

def on_elected_leader(event):
    global leader
    leader = gethostname()
    print('{}-EVENT: I am now the leader of {}'.format(gethostname(),
                                                       event.group_id.decode()))
    print('{}-EVENT: Reconfiguring database to publish'.format(gethostname()))
    configure_db_publish()


def join(name):
    while 42:
        try:
            return coordinator.join_group_create(name)
        except coordination.MemberAlreadyExist:
            print('{}-EVENT: Someone with the name {} already part of the cluster. Retrying...'\
                  .format(gethostname(), gethostname()))
            time.sleep(1)

start_local_postgres()

coordinator = coordination.get_coordinator('kazoo://', gethostname().encode())
coordinator.start()

group_name = 'pg-cluster-1'.encode()
request = join(group_name)

coordinator.watch_join_group(group_name, on_group_join)
coordinator.watch_leave_group(group_name, on_group_leave)
coordinator.watch_elected_as_leader(group_name, on_elected_leader)

configure_db_standalone()

start = time.time()
try:
    while 42:
        req = coordinator.get_leader(group_name)
        current_leader = req.get()
        current_leader = None if not current_leader else current_leader.decode()
        print('{}-HEARTBEAT: {} is leader of {} at: {}'.format(gethostname(),
                                                               leader,
                                                               group_name.decode(),
                                                               arrow.utcnow()))
        if leader != current_leader:
            print('{}-EVENT: Leader change detected! {} -> {}'.format(gethostname(),
                                                                      leader,
                                                                      current_leader))
            if not current_leader:
                print('{}-EVENT: No leader detected, stopping subscriptions')
                configure_db_standalone()
            else:
                leader = current_leader
                print('{}-EVENT: Subscribing database to: {}'.format(gethostname(),
                                                                     leader))
                configure_db_subscribe(leader)
        coordinator.heartbeat()
        coordinator.run_watchers()
        time.sleep(1)
except KeyboardInterrupt as e:
    print("Keyboard Interrupt. Stopping...")
    stop_local_postgres()
    coordinator.stop()
    print("Done!")
    exit(0)
