from math import factorial
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json

from .models import Users, Collections

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

# --------------------------------------------------------------

def hello(req):
    return HttpResponse('Hello World')

def getMovies(req):
    response = makeRequest(req)

    if('count' in response):
        urlExchange(response)

    return JsonResponse(response)

# --------------------------------------------------------------

def getCollection(req, id):
    collection = Collections.objects.filter(userid=USERID, id=id)

    if(len(collection) == 0):
        return JsonResponse({'message': f'User does not have a collection with id {id}'})
    
    collection = collection[0].toDictionary(True)
    return JsonResponse(collection)

def updateHelper(data, collection):
    if('title' in data and data['title'] is not None):
        collection.name = data['title']
    
    if('description' in data and data['description'] is not None):
        collection.description = data['description']
    
    if('movies' in data and data['movies'] is not None):
        collection.movies = data['movies']

def updateCollection(req, id):
    data = json.loads(req.body)
    collection = Collections.objects.filter(userid=USERID, id=id)

    if(len(collection) == 0):
        return JsonResponse({'message': f'User does not have a collection with id {id}'})

    collection = collection[0]
    updateHelper(data, collection)

    try:
        collection.save()
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
    return JsonResponse({'message':f'Updated the collection {id}'})

def deleteCollection(req, id):
    collection = Collections.objects.filter(userid=USERID, id=id).delete()

    if(collection[0] == 0):
        return JsonResponse({'message': f'User does not have a collection with id {id}'})

    return JsonResponse({'message': f'Deleted the collection {id}'})

def get_update_delete_Collection(req, id):
    if(req.method == 'GET'):
        return getCollection(req, id)
    elif(req.method == 'PUT'):
        return updateCollection(req, id)
    elif(req.method == 'DELETE'):
        return deleteCollection(req, id)
    else:
        return JsonResponse({'message': f'No such endpoint {req.method} /collection/id'})

# --------------------------------------------------------------

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

def getCollections(req):
    collections = Collections.objects.filter(userid=USERID)
    result = {
        'is_success': True,
        'data': {
            'collections': []
        },
        'favourite_genres': favouriteGenre(collections)
    }

    for c in collections:
        result['data']['collections'].append(c.toDictionary(False))

    return JsonResponse(result)

def addCollection(req):
    data = json.loads(req.body)
    requiredFields = {'title', 'description', 'movies'}

    if(set(data.keys()) != requiredFields):
        return JsonResponse({'message': 'one or more fields are not present | make sure all the fields are in lowercase'})

    newCollection = Collections(
        name = data['title'],
        description = data['description'],
        movies = {'movies': data['movies']},
        userid = Users.objects.get(id=USERID)
    )

    newCollection.save()
    return JsonResponse({'collection_uuid': newCollection.id})

def get_add_Collections(req):
    if(req.method == 'POST'):
        return addCollection(req)
    elif(req.method == 'GET'):
        return getCollections(req)
    else:
        return JsonResponse({'message': f'No such endpoint {req.method} /collection'})