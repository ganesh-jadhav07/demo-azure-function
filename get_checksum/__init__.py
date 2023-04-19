import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
import json
import base64

load_dotenv()

STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME')
STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python checksum generator function started')

    req_body = req.get_json()
    logging.info(f"Body: {req_body}")
    file_name = req_body.get('file_name')
    logging.info(f"Filename: {file_name}")
    content_md5 = get_blob_md5(file_name)
    logging.info('Python checksum generator function ended')
    return func.HttpResponse(
            json.dumps({"checksum": content_md5}),
            mimetype="application/json"
        )

def get_blob_md5(file_name):
    service = BlobServiceClient(account_url="https://solvefinsstorage.blob.core.windows.net", credential={"account_name": STORAGE_ACCOUNT_NAME, "account_key":STORAGE_ACCOUNT_KEY})
    blob = service.get_blob_client(container="cylo", blob=file_name)
    md5 = blob.get_blob_properties().content_settings.content_md5
    return base64.b64encode(md5).decode('utf-8')