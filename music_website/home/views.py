from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from home.models import Artist, Rating, Record, Like_Artist
from home.discogs import DiscogsArtist, DiscogsRecord
from django.contrib.auth.decorators import login_required

from home.models import Collection, Collection_Record
from .forms import NewUserForm
from django.contrib import messages
from home.search import Search, Result

# from models import Like_Artist
# from discogs import discog_artist, discog_record


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"form":form})    


def home_index(request):
    return render(request, "index.html")


def search(request):
    context = {}
    if request.method == "POST" and request.POST["query"]:
        context["query"] = request.POST["query"]
        res = Search().search(request.POST["query"])
        context["results"] = res
    return render(request, "search.html", context=context)

def artist_discogs_save(request, discogs_id):
    print(f"Saving discogs artist {discogs_id} to database...")
    
    print(f"Redirecting to proper artist page")
    return render(request, "search.html", context=context)

def search_artist(request, collection_id = None):
    pass
    #return d_artist


def save_like_artist(request, artist_id, like):
    if like == False:
        #get POST do like
        pass


def get_artist(request, artist_id):
    pass


def artist(request, artist_id):
    """IN: d_artist (class discog_artist), collection_id (int) |
    processa dados para página do Artista;
    se user autenticado, busca info do like"""
    
    like = False
    if request.user.is_authenticated:
        like = Like_Artist.objects.get(user_id=request.user.id).like #TODO: verificar atributo

    artist_name = Artist.objects.get(artist_id=artist_id).name  # para mostrar nome de artista
    artist_bio = Artist.objects.get(artist_id=artist_id).bio # para mostrar bio de artista 
    artist_pic =  Artist.objects.get(artist_id=artist_id).picture_url # para mostrar foto do artista 
    # artist_releases = d_artist.releases # para mostrar lista de albums do artista # TODO: artist_releases
    
    context = {'like': like, 'artist_name': artist_name, 'artist_bio': artist_bio, 'artist_pic': artist_pic}
    template = 'home/artist.html'
    
    return render(request, template, context)


def record(request, record_id, collection_id=None):
    if request.user.is_authenticated:
        if collection_id is not None: # se user parte de colecção para lhe adicionar um record
            collection_to_add_to = collection_id
        try:
            user_rating = Rating.objects.filter(user_id=request.user.id, record_id=record_id).rating    # TODO: testar 
        except:
            user_rating = None
        try:
            record_found_in =  Collection_Record.objects.filter(record_id=record_id, collection_id=Collection.objects.filter(user_id = request.user.id)) # lista de nomes de coleções do user onde o record está    # TODO: testar
        except:
            record_found_in = []
   
    collection_to_add_to = collection_id
    artist_name = Artist.objects.get(id=Record.objects.get(id=record_id).artist_id).name
    record_name = Record.objects.get(id=record_id).title
    release_year = Record.objects.get(id=record_id).year
    # track_list = d_record.tracklist # lista de faixas do album    # TODO: get track_list
    # ??track_times = d_record.tracktimes # tempos de cada faixa do album   # TODO: get tracktimes
    votes_count = Rating.objects.filter(record_id=record_id).count() # contagem de pares de (record_id=rating_id, user_id) em Rating
    rating_sums = 0
    i = 0
    for rating in Rating.objects.filter(record_id=record_id).rating:
        rating_sums += rating
        i += 1
    avg_rating = rating_sums / i    # TODO: simplificar
    record_cover = Record.objects.get(record_id=record_id).cover_url
    
    context = {'collection_to_add_to': collection_to_add_to, 'user_rating': user_rating, 'record_found_in': record_found_in, 'collection_to_add_to': collection_to_add_to, 'artist_name': artist_name, 'record_name': record_name, 'release_year': release_year, 'votes_count': votes_count, 'avg_rating': avg_rating, 'record_cover': record_cover}
    template = 'home/record.html'
    
    return render(request, template, context)


def play_record(request):
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


def collections(request):
    pass


def mycollection(request, collection_id):
    pass




