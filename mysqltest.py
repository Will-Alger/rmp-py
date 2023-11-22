import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
import os  # Import the os module
from dotenv import load_dotenv

load_dotenv()
sql_hostname = os.getenv('SQL_HOSTNAME')
sql_username = os.getenv('SQL_USERNAME')
sql_password = os.getenv('SQL_PASSWORD')
sql_main_database = os.getenv('SQL_MAIN_DATABASE')
sql_port = int(os.getenv('SQL_PORT'))
ssh_host = os.getenv('SSH_HOST')
ssh_user = os.getenv('SSH_USER')
ssh_port = int(os.getenv('SSH_PORT'))
sql_ip = os.getenv('SQL_IP')
ssh_key_path = os.getenv('SSH_KEY_PATH')

mypkey = paramiko.RSAKey.from_private_key_file(ssh_key_path)

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = pymysql.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)
    query = '''SELECT VERSION();'''
    data = pd.read_sql_query(query, conn)
    print(data)
    conn.close()
