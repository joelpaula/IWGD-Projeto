from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from home.discogs import discog_artist, discog_record
from home.models import Rating, Record, Like_Artist
from django.contrib.auth.decorators import login_required

# from models import Like_Artist
# from discogs import discog_artist, discog_record


def home_index(request):
    return render(request, "index.html")


def search_artist(request, collection_id = None):
    pass
    #return d_artist


def save_like_artist(request, artist_id, like):
    if like == False:
        #get POST do like
        pass


def get_artist(request, artist_id):
    pass


def artist(request, d_artist):
    """IN: d_artist (class discog_artist), collection_id (int) |
    processa dados para página do Artista;
    se user autenticado, busca info do like"""
    
    like = False
    if request.user.is_authenticated:
        like = Like_Artist.objects.get(user_id=request.user.id).like #TODO: verificar atributo

    artist_name = d_artist.title  # para mostrar nome de artista
    artist_bio = d_artist.bio # para mostrar bio de artista 
    artist_pic = d_artist.cover_image # para mostrar foto do artista 
    # artist_releases = d_artist.releases # para mostrar lista de albums do artista # TODO: artist_releases
    
    context = {'like': like, 'artist_name': artist_name, 'artist_bio': artist_bio, 'artist_pic': artist_pic, 'artist_releases': artist_releases, 'd_artist_id': d_artist.discogs_id}
    template = 'home/artist.html'
    
    return render(request, template, context)


def record(request, d_record, d_artist, collection_id=None):
    collection_to_add_to = collection_id
    artist_name = d_artist.title
    record_name = d_record.title
    # track_list = d_record.tracklist # lista de faixas do album # TODO: track_list
    # ??track_times = d_record.tracktimes # tempos de cada faixa do album # TODO: tracktimes
    if request.user.is_authenticated:
        if collection_id is not None: # se user parte de colecção para lhe adicionar um record
            collection_to_add_to = collection_id
        try:
            user_rating = Rating.objects.filter(user_id=request.user.id, record_id=Record.objects.filter(discogs_release_id=d_record.discogs_master_id)).rating # TODO: testar 
        except:
            user_rating = None
        try:
            record_found_in =  #TODO: lista de nomes de coleções do user onde o record está
        except:
            record_found_in = []
    # se user loggado:
        # se há rating do user:
            # user_rating
        # se album em alguma colecao do user:
            # collection_name
    # votes_count
    # avg_rating
    # record_cover
    context = {'collection_to_add_to': collection_to_add_to}
    
    pass


def play(request):
    pass

@login_required
def add_to_collection(request):
    pass

@login_required
def add_to_collection_save(request):
    pass

@login_required
def add_ratreview(request):
    pass

@login_required
def add_ratreview_save(request):
    pass





def collections(request, user_id):
    pass


def mycollection(request, user_id, collection_id):
    pass
