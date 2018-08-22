import logging

import azure.functions as func

import json

def main(req: func.HttpRequest,
         docs: func.DocumentList) -> func.HttpResponse:
    
    id = req.params.get('ratingId')

    for row in docs:
        if id in row.to_json():
            output = row.to_json()

    return func.HttpResponse(output)