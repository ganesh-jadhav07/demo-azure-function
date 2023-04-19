import logging
import hashlib
import azure.functions as func
from azure.storage.blob import BlobClient, ContainerClient, BlobServiceClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME')
STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY')
STORAGE_ACCOUNT_URL = os.getenv('STORAGE_ACCOUNT_URL')
STORAGE_CONTAINER = os.getenv('STORAGE_CONTAINER')

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python checksum generator function started')
        req_body = req.get_json()
        logging.info(f"Body: {req_body}")
        file_name = req_body.get('file_name')
        logging.info(f"Filename: {file_name}")
        blob_data = get_blob_data(file_name)
        checksum = generate_checksum(blob_data)
        logging.info('Python checksum generator function ended')
        if checksum:
            return func.HttpResponse(
                json.dumps({"checksum": checksum}),
                headers= {},
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(
            json.dumps({"msg": "Server Error"}),
            mimetype="application/json"
        )


    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            json.dumps({"msg": "Server Error"}),
            mimetype="application/json"
        ) 

def get_blob_data(file_name):
    try:
        service = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential={"account_name": STORAGE_ACCOUNT_NAME, "account_key":STORAGE_ACCOUNT_KEY})
        blob = service.get_blob_client(container=STORAGE_CONTAINER, blob=file_name)
        return blob
    except Exception as e:
        logging.exception(e)

def generate_checksum(blob_data):
    try:
        md5_hash = hashlib.md5()
        blob = blob_data.download_blob()
        for chunk in blob.chunks():
            # logging.info(chunk)
            md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except Exception as e:
        logging.exception(e)
