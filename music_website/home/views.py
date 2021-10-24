from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from home.models import Artist, Rating, Record, Like_Artist, Collection, Collection_Record
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from home import discogs
from .forms import NewUserForm
from django.contrib import messages
from home.search import Search
from django.urls import reverse
from home import discogs2db


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"form": form})


def home_index(request):
    return render(request, "index.html")


def search(request):
    context = {}
    if request.method == "POST" and request.POST["query"]:
        context["query"] = request.POST["query"]
        res = Search().search(request.POST["query"])
        context["results"] = res
    return render(request, "search.html", context=context)


def discogs_save_artist(request, discogs_id):
    print(f"Saving discogs artist {discogs_id} to database...")
    artist_id = discogs2db.save_artist_to_db(discogs_id)
    return HttpResponseRedirect(reverse('home:artist', args=(artist_id,)))


def discogs_save_record(request, discogs_master_id):
    print(f"Saving discogs record {discogs_master_id} to database...")
    record_id = discogs2db.save_record_to_db(discogs_master_id)
    return HttpResponseRedirect(reverse('home:record', args=(record_id,)))


def search_artist(request, collection_id = None):
    pass
    # return d_artist


@login_required
def save_like_artist(request, artist_id):
    Like_Artist.objects.create(user_id = request.user.id, artist_id = artist_id, like=True)
    
    return HttpResponseRedirect(reverse('artist.html', args=(artist_id)))


def get_artist(request, artist_id):
    pass


def artist(request, artist_id):
    """IN: d_artist (class discog_artist), collection_id (int) |
    processa dados para página do Artista;
    se user autenticado, busca info do like"""

    like = False
    if request.user.is_authenticated:
        like = Like_Artist.objects.filter(user_id=request.user.id).count() > 0 #TODO: verificar atributo

    artist = Artist.objects.get(id=artist_id)  # obtém objecto artista
    artist_releases = Record.objects.filter(artist_id=artist_id) # obtém listagem de objectos record pertencentes a artista 
    
    context = {'like': like, 'artist': artist, 'artist_releases': artist_releases}
    template = "artist.html"
    
    return render(request, template, context)


def record(request, record_id, collection_id=None):
    if request.user.is_authenticated:
        if collection_id is not None:  # se user parte de colecção para lhe adicionar um record
            collection_to_add_to = collection_id
        try:
            user_rating = Rating.objects.filter(
                user_id=request.user.id, record_id=record_id).rating    # TODO: testar
        except:
            user_rating = None
        try:
            record_found_in = Collection_Record.objects.filter(record_id=record_id, collection_id=Collection.objects.filter(
                user_id=request.user.id))  # lista de nomes de coleções do user onde o record está    # TODO: testar
        except:
            record_found_in = []

    collection_to_add_to = collection_id
    artist = Artist.objects.get(id=Record.objects.get(id=record_id)).artist_id # obtém objecto artist
    record = Record.objects.get(id=record_id) # obtém objecto record
    #release_year = Record.objects.get(id=record_id).year
    # track_list = d_record.tracklist # lista de faixas do album    # TODO: get track_list
    # ??track_times = d_record.tracktimes # tempos de cada faixa do album   # TODO: get tracktimes
    # contagem de pares de (record_id=rating_id, user_id) em Rating
    votes_count = Rating.objects.filter(record_id=record_id).count()
    rating_sums = 0
    i = 0
    for rating in Rating.objects.filter(record_id=record_id).rating:
        rating_sums += rating
        i += 1
    avg_rating = rating_sums / i    # TODO: simplificar
    #record_cover = Record.objects.get(record_id=record_id).cover_url
    
    context = {'collection_to_add_to': collection_to_add_to, 'user_rating': user_rating, 'record_found_in': record_found_in, 'collection_to_add_to': collection_to_add_to, 'artist': artist, 'record': record, 'votes_count': votes_count, 'avg_rating': avg_rating}
    template = 'record.html'
    
    return render(request, template_name=template, context=context)


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
