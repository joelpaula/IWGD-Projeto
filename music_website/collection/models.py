from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

#22h23

class Collection(models.Model):
    """collection of records | id; user_id (FK); name; creation_date"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) #user_id FK
    #collection_id PK
    name = models.CharField(max_length=50) # collection name/title
    creation_date = models.DateTimeField('Data de Criação') # collection creation date

    def __str__(self):
        return f"Coleção {self.name}, do user {self.user_id}"


class Artist(models.Model):
    """artist | id; discogs_artist_id; name; bio; picture_url"""
    #artist_id PK
    discogs_artist_id = models.IntegerField() # artist id as in discogs
    name = models.CharField(max_length=200) 
    bio = models.TextField() # artist biography
    picture_url = models.URLField() # artist picture url

    def __str__(self):
        return self.name


class Record(models.Model):
    """artist album | id; artist_id; (FK); discogs_release_id; title; year; cover_url """
    #record_id PK
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE) #artist_id FK
    discogs_release_id = models.IntegerField() # album id as in discogs
    title = models.CharField(max_length=200) # album title
    year = models.IntegerField() # album release date
    cover_url = models.URLField() # album front cover url

    def __str__(self):
        return self.title


class Collection_Record(models.Model):
    """links unique record to a user collection | id; record_id(FK PK); collection_id(FK PK); tag"""
    record_id = models.ForeignKey(Record, on_delete=models.CASCADE) # FK
    collection_id = models.ForeignKey(Collection, on_delete=models.CASCADE) # FK
    tag = models.CharField(max_length=100) #tag field, editable by user

    def __str__(self):
        return f"Album {Record.objects.get(pk=self.record_id).title} na coleção {Collection.objects.get(pk=self.collection_id).name} do user {Collection.objects.get(pk=self.collection_id).user_id}" # TODO: tentar aceder a atributos de classes do models assim funciona?
    class Meta:
        managed = False
        db_table = 'Collection_Record'
        unique_together = (('record_id', 'collection_id'),)


class Rating(models.Model):
    """links a user to a rating/review of a specif record | id; user_id(FK PK); discogs_release_id(FK PK); rating; review"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # user_id FK PK
    record_id = models.ForeignKey(Record, on_delete=models.CASCADE) # PK FK
    rating = models.IntegerField(validators=[MinValueValidator(0, message="Rating mínimo é 0"), MaxValueValidator(5, message="Rating máximo é 5")])
    review = models.TextField() # review
    class Meta:
        managed = False
        db_table = 'Rating'
        unique_together = (('user_id', 'record_id'),)


class Like_Artist(models.Model):
    """links a user to a like option of a given artist | id; user_id(FK PK); artist_id(FK PK); like"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # user_id FK PK
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE) # artist_id FK PK
    like = models.BooleanField() # True/false
    class Meta:
        managed = False
        db_table = 'Like_Artist'
        unique_together = (('user_id', 'artist_id'),)


# TODO: update com as classes adicionais do esquema