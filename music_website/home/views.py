from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from music_website.collection.models import Like_Artist
import requests
from django.http import JsonResponse
import discogs_client


def home_index(request):
    HttpResponse("Welcome!")


def search(request, collection_id = None):
    pass


def artist(request, collection_id, artist_id):
    collection_to_add_to = None
    like = False
    if request.user.is_authenticated:
        if collection_id is not None:
            collection_to_add_to = collection_id
        like = Like_Artist.objects.get(user_id=request.user.id).like #TODO: verificar atributo
    
    # TODO: montar acesso/autenticação discogs

    discogs_artist = d.artist(artist_id) # d = acesso discogs
    # mostra nome de artista
    artist_name = discogs_artist.name  #TODO: verificar atributo
    # mostra bio de artista
    artist_bio = discogs_artist.profile # TODO: verfificar atributo
    # mostra foto do artista
    artist_pic = discogs_artist.images # TODO: verfificar atributo
    # mostra lista de albums do artista
    artist_releases = discogs_artist.releases # TODO: verfificar atributo
    context = {'artist_name': artist_name, 'artist_bio': artist_bio, 'artist_pic': artist_pic, 'artist_releases': artist_releases}
    template = 'home/artist.html'
    return render(request, template, context)
