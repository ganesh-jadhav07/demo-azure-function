from azure.storage.blob import BlockBlobService,AppendBlobService

import os
import logging
from uploader.connection import ConnectionFactory
import json
from time import localtime
from dotenv import load_dotenv

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

# def upload_to_blob(mgu_id,files):
#         try:
#                 # chunk_size=4*1024*1024 
#                 # size = file
#                 query = "SELECT * FROM config_tbl WHERE MGU_ID={0}".format(mgu_id)
#                 cursor = get_db_connection()
#                 cursor.execute(query)
#                 record = cursor.fetchone()
#                 blob_service_client = BlockBlobService(
#                         account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
#                 container_name = record[3]
#                 logging.info(files)
#                 for file in files:
#                         logging.info("Type {0}".format(type(file)))
#                         blob_name = file.filename
#                         logging.info(blob_name)
#                         container_client = blob_service_client.create_blob_from_stream(container_name, blob_name, file)
#                 # with file as stream:
#                 #         read_data = stream.read(chunk_size)
#                 # container_client = blob_service_client.create_blob_from_stream(container_name, blob_name, file)
#                 return "Files uploaded successfully"
#         except Exception as e:
#                 logging.error(e)
#                 return "File {0} upload failed"

CHUNK_SIZE = 4*1024*1024 
def read_in_chunks(file_object,CHUNK_SIZE):
        while True:
                data = file_object.read(C)
                logging("Data: {0}".format(data))
                if not data:
                        break
                yield data

def upload_to_blob(mgu_id,files):
        try:
                query = "SELECT * FROM config_tbl WHERE MGU_ID={0}".format(mgu_id)
                cursor = get_db_connection()
                cursor.execute(query)
                record = cursor.fetchone()
                blob_service_client = AppendBlobService(
                        account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
                container_name = record[3]
                for file in files:
                        blob_name = file.filename
                        blob_service_client.create_blob(container_name, blob_name)
                        while True:
                                read_data = file.read(CHUNK_SIZE)
                                logging.info('Read_Data {0}'.format(type(read_data)))
                                if not read_data:
                                        break
                                blob_service_client.append_blob_from_bytes(container_name, blob_name, read_data)
                return "Files uploaded successfully"
        except Exception as e:
                logging.error(e)
                return "Files upload failed"
               
 
if __name__ =='__main__':
    upload_to_blob()
       