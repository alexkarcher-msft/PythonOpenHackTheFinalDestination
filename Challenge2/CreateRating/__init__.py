import logging

import azure.functions as func
import requests
import uuid
import time
import datetime
import json

def main(req: func.HttpRequest, docs: func.Out[func.Document]) -> func.HttpResponse:

    getProducturl = "http://serverlessohproduct.trafficmanager.net/api/GetProduct"
    getUserurl = "http://serverlessohuser.trafficmanager.net/api/GetUser"

    userId = req.params.get('userId')
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userId = req_body.get('userId')

    productId = req.params.get('productId')
    if not productId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            productId = req_body.get('productId')

    locationName = req.params.get('locationName')
    if not locationName:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            locationName = req_body.get('locationName')


    rating = req.params.get('rating')
    if not rating:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            rating = req_body.get('rating')

    userNotes = req.params.get('userNotes')
    if not userNotes:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userNotes = req_body.get('userNotes')

    if userId and productId and locationName and rating and userNotes:
        ts = time.time()

        userVerifyRequest = requests.get(url=getUserurl, params={'userId': userId})
        userData = {}
        try:
            userData = userVerifyRequest.json()
        except:
            return func.HttpResponse("Cannot validate userID")

        if 'userId' not in userData:
            return func.HttpResponse("Cannot validate userID")

        productVerifyRequest = requests.get(url=getProducturl, params={'productId': productId})
        productData = []
        try:
            productData = productVerifyRequest.json()
        except:
            return func.HttpResponse("Cannot validate productID")
        if 'productId' not in productData:
            return func.HttpResponse("Cannot validate productID")

        entry = {
            'userId': str(userId),
            'id': str(uuid.uuid4()),
            'productId': str(productId),
            'timestamp': str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')),
            'locationName': str(locationName),
            'rating': str(rating),
            'userNotes': str(userNotes)
        }
        docs.set(func.Document.from_json(json.dumps(entry)))
        return func.HttpResponse(f"Success! ID: {entry['id']} for UserID: {userId}")

    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
