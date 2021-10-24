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
    try:
        Like_Artist.objects.create(user_id_id = request.user.id, artist_id_id = artist_id, like=True)
    finally:
        return HttpResponseRedirect(reverse('home:artist', args=(artist_id,)))


def get_artist(request, artist_id):
    pass


def artist(request, artist_id):
    """IN: d_artist (class discog_artist), collection_id (int) |
    processa dados para página do Artista;
    se user autenticado, busca info do like"""

    like = False
    if request.user.is_authenticated:
        like = Like_Artist.objects.filter(user_id=request.user.id).count() > 0

    artist = Artist.objects.get(id=artist_id)
    
    context = {'like': like, 'artist': artist}
    template = "artist.html"
    
    return render(request, template, context)


def record(request, record_id, collection_id=None):
    user_rating = None
    record_found_in = None
    if request.user.is_authenticated:
        if collection_id is not None:  # se user parte de colecção para lhe adicionar um record
            collection_to_add_to = collection_id
        try:
            user_rating = Rating.objects.get(
                user_id=request.user.id, record_id_id=record_id).rating  
        except:
            user_rating = None
        try:
            record_found_in = Collection_Record.objects.filter(record_id_id=record_id, collection_id__in = Collection.objects.filter(
                user_id=request.user.id))  # lista de nomes de coleções do user onde o record está    # TODO: testar
        except:
            record_found_in = []

    collection_to_add_to = collection_id
    record = Record.objects.get(id=record_id) # obtém objecto record
    tracks = discogs.get_record_master_by_id(record.discogs_release_id).tracklist

    votes_count = Rating.objects.filter(record_id=record_id).count()
    rating_sums = 0
    avg_rating = None
    i = 0
    for item in Rating.objects.filter(record_id=record_id):
        rating_sums += item.rating
        i += 1
    if i>0: 
        avg_rating = rating_sums / i    # TODO: simplificar
    
    context = {'collection_to_add_to': collection_to_add_to, 
        'user_rating': user_rating, 
        'record_found_in': record_found_in, 
        'record': record, 
        'tracks': tracks,
        'votes_count': votes_count, 
        'avg_rating': avg_rating}
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
