import logging
from uploader.upload_to_location import *
import json

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_email = req.params.get('user_email')
    if user_email:
        value = get_upload_location(user_email)
        response = {"container_name": value}
        return func.HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user_email in the query string or in the request body for a personalized response.",
             status_code=200
        )