import threading
from typing import Optional
import mysql.connector
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()
config = {
  'user': os.getenv('DB_USERNAME'),
  'password': os.getenv('DB_PASSWORD'),
  'host': os.getenv('DB_HOST'),
  'database': os.getenv('DB'),
  'raise_on_warnings': True
}

class MysqlConnection:
    _instance_lock = threading.Lock()
    _instance: Optional["MysqlConnection"] = None
    
    def __new__(cls):
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._connection = mysql.connector.connect(**config)
        return cls._instance

    def get_connection(self):
        return self._connection


class ConnectionFactory:
    def __init__(self):
        self._connections = {}

    def get_connection(self, connection_type):
        if connection_type not in self._connections:
            if connection_type == "snowflake":
                self._connections[connection_type] = SnowflakeConnection()
            elif connection_type == "mysql":
                self._connections[connection_type] = MysqlConnection()
            else:
                raise ValueError(f"Invalid connection type: {connection_type}")
        return self._connections[connection_type].get_connection()