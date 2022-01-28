from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.id} {self.name}'

class Collections(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    movies = models.JSONField()
    userid = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} {self.name} {self.description} {self.movies}'
    
    def toDictionary(self, needMovies):
        dictionary = {}
        dictionary['uuid'] = self.id
        dictionary['title'] = self.name
        dictionary['description'] = self.description
        
        if needMovies:
            dictionary['movies'] = self.movies['movies']


        return dictionary