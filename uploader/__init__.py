import logging
from uploader.upload_to_blob import *

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body_data = req.get_body()
    if req_body_data:
        return func.HttpResponse(req_body_data)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Please upload a file",
             status_code=200
        )
