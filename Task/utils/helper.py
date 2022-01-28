import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


moviesEndpoint = 'https://demo.credy.in/api/v1/maya/movies'
local_moviesEndpoint = 'https://onefin-backend-task-akash.herokuapp.com/movies'
username = 'iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
password = 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'

if(settings.DEBUG):
    print('DEBUG is on')
    local_moviesEndpoint = 'http://localhost:8000/movies'

# helper functions 

def favouriteGenre(collections):
    allgenres = {}

    for c in collections:
        c = c.toDictionary(True)
        for movie in c['movies']:
            if('genres' not in movie):
                continue
            
            movieGenres = movie['genres'].split(',')

            for genre in movieGenres:
                if genre in allgenres:
                    allgenres[genre] += 1
                else:
                    allgenres[genre] = 1

    favourites = sorted(allgenres, key=allgenres.get, reverse=True)
    return ','.join(favourites[:3])

def updateHelper(data, collection):
    if('title' in data and data['title'] is not None):
        collection.name = data['title']
    
    if('description' in data and data['description'] is not None):
        collection.description = data['description']
    
    if('movies' in data and data['movies'] is not None):
        collection.movies = {'movies': data['movies']}

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
