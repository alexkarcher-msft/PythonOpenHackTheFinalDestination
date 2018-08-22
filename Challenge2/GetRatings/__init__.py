import logging

import azure.functions as func

def main(req: func.HttpRequest,
         docs: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('userId')

    output = "["

    for row in docs:
        if name in row.to_json():
            output += row.to_json() + ","

    output = output[:-1] + "]"

    if name:
        return func.HttpResponse(output)
    else:
        return func.HttpResponse(
             "Please pass a userId on the query string",
             status_code=400
        )