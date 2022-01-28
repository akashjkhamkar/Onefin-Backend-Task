from django.http import JsonResponse
from .utils.utils import getMovies, getCollection, updateCollection, deleteCollection, addCollection, getCollections
from .utils.authenticate import registerUser, login_required

def hello(req):
    return JsonResponse({'msg': 'Hello World!'})

def register(req):
    if(req.method != 'POST'):
        return JsonResponse({'message': f'No such endpoint {req.method} /register'})
    return registerUser(req)

@login_required
def movies(req):
    return getMovies(req)

@login_required
def get_update_delete_Collection(req, id):
    if(req.method == 'GET'):
        return getCollection(req, id)
    elif(req.method == 'PUT'):
        return updateCollection(req, id)
    elif(req.method == 'DELETE'):
        return deleteCollection(req, id)
    else:
        return JsonResponse({'message': f'No such endpoint {req.method} /collection/id'})

@login_required
def get_add_Collections(req):
    if(req.method == 'POST'):
        return addCollection(req)
    elif(req.method == 'GET'):
        return getCollections(req)
    else:
        return JsonResponse({'message': f'No such endpoint {req.method} /collection'})