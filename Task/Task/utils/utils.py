from django.http import JsonResponse
import json

from ..models import Users, Collections
from .helper import favouriteGenre, updateHelper, urlExchange, makeRequest 

def getMovies(req):
    response = makeRequest(req)

    if('count' in response):
        urlExchange(response)

    return JsonResponse(response)

def getCollection(req, id):
    collection = Collections.objects.filter(userid=req.USERID, id=id)

    if(len(collection) == 0):
        return JsonResponse({'message': f'User does not have a collection with id {id}'})
    
    collection = collection[0].toDictionary(True)
    return JsonResponse(collection)

def updateCollection(req, id):
    data = json.loads(req.body)
    collection = Collections.objects.filter(userid=req.USERID, id=id)

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
    collection = Collections.objects.filter(userid=req.USERID, id=id).delete()

    if(collection[0] == 0):
        return JsonResponse({'message': f'User does not have a collection with id {id}'})

    return JsonResponse({'message': f'Deleted the collection {id}'})

def addCollection(req):
    data = json.loads(req.body)
    requiredFields = {'title', 'description', 'movies'}

    if(set(data.keys()) != requiredFields):
        return JsonResponse({'message': 'one or more fields are not present | make sure all the fields are in lowercase'})

    newCollection = Collections(
        name = data['title'],
        description = data['description'],
        movies = {'movies': data['movies']},
        userid = Users.objects.get(id=req.USERID)
    )

    newCollection.save()
    return JsonResponse({'collection_uuid': newCollection.id})

def getCollections(req):
    collections = Collections.objects.filter(userid=req.USERID)
    result = {
        'is_success': True,
        'data': {
            'collections': [],
            'favourite_genres': favouriteGenre(collections)
        }
    }

    for c in collections:
        result['data']['collections'].append(c.toDictionary(False))

    return JsonResponse(result)
