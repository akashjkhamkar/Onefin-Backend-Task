from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json

moviesEndpoint = 'https://demo.credy.in/api/v1/maya/movies'
local_moviesEndpoint = 'http://localhost:8000/movies'
username = 'iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
password = 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'

def urlExchange(response):
    nextlink = response['next']
    prevlink = response['previous']

    if(nextlink):
        response['next'] = nextlink.replace(moviesEndpoint, local_moviesEndpoint)
    
    if(prevlink):
        response['previous'] = prevlink.replace(moviesEndpoint, local_moviesEndpoint)

def hello(req):
    return HttpResponse('Hello World')

def getMovies(req):
    url = moviesEndpoint
    page = req.GET.get('page', '')

    if(page):
        url = moviesEndpoint + f'?page={page}'
    
    response = requests.get(url, auth = HTTPBasicAuth(username, password)).json()
    urlExchange(response)

    return HttpResponse(json.dumps(response))