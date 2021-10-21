from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from music_website.collection.models import Like_Artist


def home_index(request):
    HttpResponse("Welcome!")


def search(request, collection_id = None):
    pass


def artist(request, collection_id):
    collection_to_add = None
    like = False
    if request.user.is_authenticated:
        if collection_id is not None:
            collection_to_add = collection_id
        like = Like_Artist.objects.get(user_id=request.user.id).like
    # mostra nome de artista
    # mostra bio de artista
    # mostra foto do artista
    # mostra lista de albums do artista
    
    