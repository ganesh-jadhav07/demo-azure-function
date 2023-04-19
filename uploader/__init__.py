import logging
from uploader.upload_to_location import *
import json

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body_data = req.get_body()
    if req_body_data:
        return func.HttpResponse(req_body_data)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user_email in the query string or in the request body for a personalized response.",
             status_code=200
        )