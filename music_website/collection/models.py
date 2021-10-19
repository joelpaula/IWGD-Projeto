from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator



class Collection(models.Model):
    """collection of records"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) #user_id FK
    #collection_id PK
    name = models.CharField(max_length=50) # collection name/title
    creation_date = models.DateTimeField('Data de Criação') # collection creation date

    def __str__(self):
        return f"Coleção {self.name}, do user {self.user_id}"


class Artist(models.Model):
    #artist_id PK
    discogs_artist_id = models.IntegerField() # artist id as in discogs
    name = models.CharField(max_length=200) 
    bio = models.TextField() # artist biography
    picture_url = models.URLField() # artist picture url

    def __str__(self):
        return self.name


class Record(models.Model):
    #record_id PK
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE) #artist_id FK
    discogs_release_id = models.IntegerField() # album id as in discogs
    title = models.CharField(max_length=200) # album title
    year = models.IntegerField(max_length=4) # album release date
    cover_url = models.URLField() # album front cover url

    def __str__(self):
        return self.title


class Collection_Record(models.Model):
    """links unique record to a user collection | id; record_id(FK PK); collection_id(FK PK); tag"""
    record_id = models.ForeignKey(Record, on_delete=models.CASCADE, primary_key=True) # PK FK
    collection_id = models.ForeignKey(Collection, primary_key=True) # PK FK
    tag = models.CharField(max_length=100) #tag field, editable by user

    def __str__(self):
        return f"Album {Record.objects.get(pk=self.record_id).title} na coleção {Collection.objects.get(pk=self.collection_id).name} do user {Collection.objects.get(pk=self.collection_id).user_id}" # TODO: tentar aceder a atributos de classes do models assim funciona?

#    discogs_release_id = models.IntegerField(primary_key=True) #Record.objects.get(pk = record_id).discogs_release_id #discogs_release_id FK PK
 #   rating = models.ForeignKey(Rating, on_delete=CASCADE) #models.IntegerField(choices={0, 1, 2, 3, 4, 5})


class Rating(models.Model):
    """links a user to a rating/review of a specif record | id; user_id(FK PK); discogs_release_id(FK PK); rating; review"""
    # TODO
    # user_id FK PK
    # discogs_release_id FK PK
    rating = models.IntegerField(MinValueValidator(0, message="Rating mínimo é 0"), MaxValueValidator(5, message="Rating máximo é 5"))
    # review

    pass

# TODO: verificar se todas as classes têm um object.id por natureza
# TODO: uniformizar docstrings das classes
