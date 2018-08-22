import logging

import azure.functions as func

def main(req: func.HttpRequest,
         docs: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('userId')

    if name:
        return func.HttpResponse(docs[0].to_json())
    else:
        return func.HttpResponse(
             "Please pass a userId on the query string",
             status_code=400
        )