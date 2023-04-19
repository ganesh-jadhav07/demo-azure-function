import os
import logging
from uploader.connection import ConnectionFactory
import json

from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
        try:
                factory = ConnectionFactory()
                conn = factory.get_connection('mysql')
                return conn.cursor()
        except Exception as e:
                logging.exception(e)

def get_upload_location(user_email):
        try:
                query = "select upload_config as upload_location from config_tbl, users_tbl where users_tbl.mgu_id = config_tbl.mgu_id and users_tbl.user_email = '{0}'".format(user_email)
                cursor = get_db_connection()
                cursor.execute(query)
                record = cursor.fetchone()
                return record[0]
        except Exception as e:
                logging.error(e)
                return "No upload location configured"