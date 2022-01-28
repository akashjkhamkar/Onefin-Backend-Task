from django.http import JsonResponse
import json
import bcrypt
import jwt
from functools import wraps

from ..models import Users

def login_required(f):
    @wraps(f)
    def decorated_function(req):
        token = req.META.get('HTTP_AUTHORIZATION')
        if(token is None):
            return JsonResponse({'error':'No token provided | User is not authenticated'})
        else:
            token = token.split(' ')[1]
            
        try:
            payload = jwt.decode(token, key='secretstuff', algorithms=['HS256'])
            req.USERID = payload['id']
            return f(req)
        except Exception as e:
            return JsonResponse({'error':'Invalid token | Please login again'})

    return decorated_function

def createToken(id):
    token = jwt.encode(
        payload={'id': id},
        key="secretstuff"
    )

    return token.decode('utf-8')

def registerUser(req):
    data = json.loads(req.body)
    if({'username', 'password'} != set(data.keys())):
        return JsonResponse({'message': 'username or password not provided!'})
    elif(data['username'] == '' or data['password'] == ''):
        return JsonResponse({'message': 'username or password can not be empty!'})

    # checks if the user already exists or not
    queryResults = None
    try:
        queryResults = Users.objects.filter(name=data['username'])
    except Exception as e:
        return JsonResponse({'error': str(e)})

    # if username does not exist, create a new user
    # if user does exist, verify the password
    user = None
    if(len(queryResults) == 0):
        hashedPassword = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
        user = Users(name=data['username'], password=hashedPassword.decode('utf8'))
        user.save()
    else:
        user = queryResults[0]
        if(not bcrypt.checkpw(data['password'].encode('utf8'), user.password.encode('utf8'))):
            return JsonResponse({'error': 'username or password is wrong'})

    return JsonResponse({'access_token': createToken(user.id)})