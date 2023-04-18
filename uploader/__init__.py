import logging
from uploader.upload_to_blob import *

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body_data = req.get_body()
    if req_body_data:
        try:
          mgu_id = req_body_data.get('mgu_id')
      
        except ValueError:
            pass

    if mgu_id:
#         return_value = upload_to_blob(mgu_id,req_file)
        return func.HttpResponse(mgu_id)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Please upload a file",
             status_code=200
        )
