import psycopg2
from socket import gethostname
from subprocess import check_call
from psycopg2.sql import SQL, Literal, Identifier
from psycopg2.extras import NamedTupleCursor

USERNAME = 'vagrant'
PASSWORD = 'vagrant'
DATABASE = 'testdb'
MY_ID = gethostname()[-1]

# Database Hosts
LOCALHOST = "dbname='testdb' user='{}' host='localhost' password='{}'".format(USERNAME, PASSWORD)
PG_NODES = {'pg-node-1': "dbname='testdb' user='{}' host='pg-node-1' password='{}'".format(USERNAME, PASSWORD),
            'pg-node-2': "dbname='testdb' user='{}' host='pg-node-2' password='{}'".format(USERNAME, PASSWORD),
            'pg-node-3': "dbname='testdb' user='{}' host='pg-node-3' password='{}'".format(USERNAME, PASSWORD),
            'pg-node-4': "dbname='testdb' user='{}' host='pg-node-4' password='{}'".format(USERNAME, PASSWORD),
            'pg-node-5': "dbname='testdb' user='{}' host='pg-node-5' password='{}'".format(USERNAME, PASSWORD)}

# Query Formats
CREATE_PUBLICATION_ALL = SQL('CREATE PUBLICATION cluster_publication FOR ALL TABLES')
CREATE_SUBSCRIPTION_NOCOPY = SQL('CREATE SUBSCRIPTION sub_{} CONNECTION {} PUBLICATION cluster_publication WITH (copy_data=false)'.format(MY_ID, '{}'))
CREATE_SUBSCRIPTION = SQL('CREATE SUBSCRIPTION sub_{} CONNECTION {} PUBLICATION cluster_publication'.format(MY_ID, '{}'))
TRUNCATE_TABLE = SQL("TRUNCATE TABLE random_data")
SET_SUB_SLOT_NONE = SQL("ALTER SUBSCRIPTION sub_{} SET (slot_name = NONE)".format(MY_ID))
DROP_SUBSCRIPTION = SQL("DROP SUBSCRIPTION IF EXISTS sub_{}".format(MY_ID))
DROP_PUBLICATION = SQL("DROP PUBLICATION IF EXISTS cluster_publication")
GET_SEQ_VALUE = SQL("SELECT MAX(id) FROM random_data")
RESET_SEQUENCE = SQL("ALTER SEQUENCE random_data_id_seq RESTART WITH {}")
REFRESH_PUBLICATION_NOCOPY = SQL("ALTER SUBSCRIPTION sub_{} REFRESH PUBLICATION WITH (copy_data=false)".format(MY_ID))
REFRESH_PUBLICATION = SQL("ALTER SUBSCRIPTION sub_{} REFRESH PUBLICATION".format(MY_ID))

def sync_up(node):
    pass

def execute(node, query):
    with psycopg2.connect(node) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query)
        conn.commit()

def reset_sequence():
    with psycopg2.connect(LOCALHOST, cursor_factory=NamedTupleCursor) as conn:
        with conn.cursor() as cursor:
            cursor.execute(GET_SEQ_VALUE)
            res = cursor.fetchone()
            seq_value = (0 if not res.max else res.max) + 1
            cursor.execute(RESET_SEQUENCE.format(Literal(seq_value)))
        conn.commit()

def restart_local_postgres():
    check_call(['service', 'postgresql', 'restart'])

def stop_local_postgres():
    check_call(['service', 'postgresql', 'stop'])

def start_local_postgres():
    check_call(['service', 'postgresql', 'start'])
    
def drop_publication():
    execute(LOCALHOST, DROP_PUBLICATION)
    
def drop_subscription():
    print("Attempting clean subscription drop")
    try:
        print("Attempting clean subscription drop")
        execute(LOCALHOST, DROP_SUBSCRIPTION)
    except:
        print("Clean subscription drop failed. Resorting to unclean drop.")
        execute(LOCALHOST, SET_SUB_SLOT_NONE)
        execute(LOCALHOST, DROP_SUBSCRIPTION)
    print("Subscription dropped!")
    
def configure_standalone():
    print("Configuring node as a standalone")
    print("Dropping subscription")
    drop_subscription()
    print("Dropping publication")
    drop_publication()
    print("Resetting sequences")
    reset_sequence()

def configure_publisher():
    print("Configuring node as publisher")
    drop_subscription()
    print("Restarting local postgres")
    restart_local_postgres()
    print("Creating publication...")
    execute(LOCALHOST, CREATE_PUBLICATION_ALL)
    print("Publication created!")

def configure_subscriber(pub_node):
    print("Configuring node as subscriber")
    print("Dropping publication")
    drop_publication()
    print("Restarting local postgres")
    restart_local_postgres()
    print("Dropping tables")
    execute(LOCALHOST, TRUNCATE_TABLE)
    print("Subscribing to '{}'".format(pub_node))
    execute(LOCALHOST, CREATE_SUBSCRIPTION.format(Literal(pub_node)))
    # print("Refreshing publication")
    # execute(LOCALHOST, REFRESH_PUBLICATION)
