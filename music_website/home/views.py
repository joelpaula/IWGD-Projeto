from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from music_website.collection.models import Like_Artist
import discogs_client


def home_index(request):
    HttpResponse("Welcome!")


def search(request, collection_id = None):
    pass


def save_like_artist(request, artist_id, like):
    if like == False:
        #get POST
    
    pass


def artist(request, artist_id, collection_id=None):
    collection_to_add_to = collection_id
    like = False
    if request.user.is_authenticated:
        if collection_id is not None:
            collection_to_add_to = collection_id
        like = Like_Artist.objects.get(user_id=request.user.id).like #TODO: verificar atributo
    
    # TODO: montar acesso/autenticação discogs

    discogs_artist = d_session.artist(artist_id) # d_session = acesso através module python discogs
    artist_name = discogs_artist.name  # para mostrar nome de artista #TODO: verificar atributo
    artist_bio = discogs_artist.profile # para mostrar bio de artista # TODO: verfificar atributo
    artist_pic = discogs_artist.images # para mostrar foto do artista # TODO: verfificar atributo
    artist_releases = discogs_artist.releases # para mostrar lista de albums do artista # TODO: verfificar atributo
    
    context = {'collection_to_add_to': collection_to_add_to, 'like': like, 'artist_name': artist_name, 'artist_bio': artist_bio, 'artist_pic': artist_pic, 'artist_releases': artist_releases}
    template = 'home/artist.html'
    
    return render(request, template, context)


def record(request, record_id):
    # cover
    # rating
    # nbr of votes
    # collection name
    # nbr faixa, nome_faixa, duracao_faixa
    pass


def play(request):
    pass
