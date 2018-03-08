import sys
from database import LOCALHOST, create_random_data_table, restart_local_postgres, create_role

# my_node_id = int(sys.argv[1])

# create_role(LOCALHOST, 'eugene', 'secure_password')
create_random_data_table(LOCALHOST)
restart_local_postgres()
