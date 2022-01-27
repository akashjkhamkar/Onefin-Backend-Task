from gc import collect
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json

from .models import Users, Collections
from django.core import serializers

moviesEndpoint = 'https://demo.credy.in/api/v1/maya/movies'
local_moviesEndpoint = 'http://localhost:8000/movies'
username = 'iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
password = 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'

USERID = 1

def urlExchange(response):
    nextlink = response['next']
    prevlink = response['previous']

    if(nextlink):
        response['next'] = nextlink.replace(moviesEndpoint, local_moviesEndpoint)
    
    if(prevlink):
        response['previous'] = prevlink.replace(moviesEndpoint, local_moviesEndpoint)

def makeRequest(req):
    url = moviesEndpoint
    page = req.GET.get('page', '')
    if(page):
        url = moviesEndpoint + f'?page={page}'

    response = None
    
    try:
        response = requests.get(url, auth = HTTPBasicAuth(username, password)).json()
    except Exception as e:
        print("Error makeRequest(): ", e)
        response = { 'message': 'Internal Server Error', 'detail': 'could not make requst to the movies api'}

    return response    

# -------------------------------------------------------------

def hello(req):
    return HttpResponse('Hello World')

def getMovies(req):
    response = makeRequest(req)

    if('count' in response):
        urlExchange(response)

    return HttpResponse(json.dumps(response))

def getCollections(req):
    collections = Collections.objects.filter(userid=USERID)
    result = {
        'is_success': True,
        'data': {
            'collections': []
        }
    }

    for c in collections:
        result['data']['collections'].append(c.toDictionary(False))

    return HttpResponse(json.dumps(result))

def getCollection(req, id):
    collection = Collections.objects.filter(userid=USERID, id=id)

    if(len(collection) == 0):
        return HttpResponse(json.dumps({'message': f'User does not have a collection with id {id}'}))
    
    collection = collection[0].toDictionary(True)
    return HttpResponse(json.dumps(collection))