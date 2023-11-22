import os
import pandas as pd
import paramiko
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

class Database:
    def __init__(self):
        load_dotenv()
        self.sql_hostname = os.getenv('SQL_HOSTNAME')
        self.sql_username = os.getenv('SQL_USERNAME')
        self.sql_password = os.getenv('SQL_PASSWORD')
        self.sql_main_database = os.getenv('SQL_MAIN_DATABASE')
        self.sql_port = int(os.getenv('SQL_PORT'))
        self.ssh_host = os.getenv('SSH_HOST')
        self.ssh_user = os.getenv('SSH_USER')
        self.ssh_port = int(os.getenv('SSH_PORT'))
        self.ssh_key_path = os.getenv('SSH_KEY_PATH')
        self.mypkey = paramiko.RSAKey.from_private_key_file(self.ssh_key_path)

    def __enter__(self):
        self.tunnel = SSHTunnelForwarder(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_user,
            ssh_pkey=self.mypkey,
            remote_bind_address=(self.sql_hostname, self.sql_port)
        )
        self.tunnel.start()

        db_url = f"mysql+pymysql://{self.sql_username}:{self.sql_password}@localhost:{self.tunnel.local_bind_port}/{self.sql_main_database}"
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()  # Create a session instance
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()  # Close the session
        self.engine.dispose()
        self.tunnel.stop()

    def query(self, sql):
        with self.Session() as session:
            result = session.execute(sql)
            return result.fetchall()

    def query_to_dataframe(self, sql):
        with self.engine.connect() as connection:
            return pd.read_sql_query(sql, connection)
