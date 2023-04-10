from azure.storage.blob import AppendBlobService
from dotenv import load_dotenv
import os
import logging
from uploader.connection import ConnectionFactory
import json
from time import localtime

load_dotenv()

STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME')
STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY')


def get_db_connection():
        try:
                factory = ConnectionFactory()
                conn = factory.get_connection('mysql')
                return conn.cursor()
        except Exception as e:
                logging.exception(e)

def upload_to_blob(mgu_id,file):
        try:
                # chunk_size=4*1024*1024 
                # size = file
                # start_time = localtime()
                query = "SELECT * FROM config_tbl WHERE MGU_ID={0}".format(mgu_id)
                cursor = get_db_connection()
                cursor.execute(query)
                record = cursor.fetchone()
                logging.info(record)
                blob_service_client =AppendBlobService(
                        account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
                container_name = record[3]
                blob_name = file.filename
                blob_service_client.create_blob(container_name, blob_name)
                while True:
                        read_data = file.read(chunk_size)
                        if not read_data:
                            return "Uploaded" 
                        blob_service_client.append_blob_from_stream(container_name, blob_name, read_data)
                return "Hello"
        except Exception as e:
                logging.error(e)
                return {"msg:":"File {0} upload failed".format(blob_name)}
               
 
if __name__ =='__main__':
    upload_to_blob()
       