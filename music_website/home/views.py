from django import http
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from home.models import Artist, Rating, Record, Like_Artist, Collection, Collection_Record, Staff_Picks
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from home import discogs
from .forms import NewUserForm
from django.contrib import messages
from home.search import Search
from django.urls import reverse
from home import discogs2db
from django.utils import timezone
from django.db.models import Avg, Count
from django.core.paginator import Paginator


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
    top_artists = Artist.objects.annotate(avg_rating=Avg('record__rating__rating'), review_count=Count(
        'record__rating'), likes=Count('like_artist')).order_by('-avg_rating', '-review_count')[:5]
    # .exclude(avg_rating=None) # se quisermos excluir artistas sem ratings

    top_records = Record.objects.annotate(avg_rating=Avg('rating__rating'), review_count=Count(
        'rating')).order_by('-avg_rating', '-review_count')[:5]

    top_reviews = Rating.objects.order_by('-creation_date')[:3]

    staff_picks = Staff_Picks.objects.annotate(avg_rating=Avg('record__rating__rating'), review_count=Count(
        'record__rating')).order_by('-creation_date')[:3]

    context = {
        "top_artists": top_artists,
        "top_records": top_records,
        "top_reviews": top_reviews,
        "staff_picks": staff_picks,
    }
    return render(request, "index.html", context=context)


def search(request, collection_id=None):
    context = {}
    if request.method == "POST" and request.POST["query"]:
        context["query"] = request.POST["query"]
        res = Search().search(request.POST["query"])
        context["results"] = res
    context['collection_id'] = collection_id
    return render(request, "search.html", context=context)


def discogs_save_artist(request, discogs_id):
    print(f"Saving discogs artist {discogs_id} to database...")
    artist_id = discogs2db.save_artist_to_db(discogs_id)
    return HttpResponseRedirect(reverse('home:artist', args=(artist_id,)))


def discogs_save_record(request, discogs_master_id):
    print(f"Saving discogs record {discogs_master_id} to database...")
    record_id = discogs2db.save_record_to_db(discogs_master_id)
    return HttpResponseRedirect(reverse('home:record', args=(record_id,)))


@login_required
def save_like_artist(request, artist_id):
    try:
        Like_Artist.objects.create(
            user_id_id=request.user.id, artist_id_id=artist_id, like=True)
    finally:
        return HttpResponseRedirect(reverse('home:artist', args=(artist_id,)))


@login_required
def save_unlike_artist(request, artist_id):
    try:
        Like_Artist.objects.filter(
            user_id_id=request.user.id, artist_id_id=artist_id, like=True).delete()
    finally:
        return HttpResponseRedirect(reverse('home:artist', args=(artist_id,)))


def review(request, review_id=None):
    # Depends on receiving 'record_id' either from the POST or the Get (url)
    rev = get_object_or_404(Rating, pk=review_id) if review_id else None
    if not rev and request.GET.get("record_id"):
        rec_id = int(request.GET.get("record_id"))
        rev = Rating.objects.get(user_id_id=request.user.id, record_id_id=rec_id) if Rating.objects.filter(user_id_id=request.user.id, record_id_id=rec_id).count()>0 else None
    edit_mode = False if rev and rev.user_id.id != request.user.id else True
    if request.method == "POST":
        rec = get_object_or_404(Record, pk=request.POST.get("record_id"))
        if not rev and Rating.objects.filter(user_id_id=request.user.id, record_id=rec).count() == 0:
            rev = Rating.objects.create(user_id_id=request.user.id, record_id=rec,
                                        rating=request.POST.get("rating", None), review=request.POST.get("review", None))
            return HttpResponseRedirect(reverse('home:review', args=(rev.pk,)))
        else:
            rev = rev or Rating.objects.get(user_id_id=request.user.id, record_id=rec)
            rev.rating = int(request.POST.get("rating", None))
            rev.review = request.POST.get("review", None)
            rev.save()
    else:
        record_id = rev.record_id.id if rev else request.GET.get("record_id")
        rec = get_object_or_404(Record, pk=record_id)
    tracks = discogs.get_record_master_by_id(rec.discogs_release_id).tracklist

    context = {
        "edit_mode": edit_mode,
        "review": rev,
        "record": rec,
        "tracks": tracks,
    }
    return render(request, "review.html", context=context)


def reviews(request):
    res = Rating.objects.filter(user_id_id=request.user.id)
    context = {"reviews": res, }
    return render(request, "reviews.html", context=context)


def artist(request, artist_id):
    like = False
    if request.user.is_authenticated:
        like = Like_Artist.objects.filter(user_id=request.user.id, artist_id_id=artist_id).count() > 0

    artist = get_object_or_404(Artist, id=artist_id)

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
            user_rating = 0
        try:
            record_found_in = Collection_Record.objects.filter(record_id_id=record_id, collection_id__in=Collection.objects.filter(
                user_id=request.user.id))  # lista de nomes de coleções do user onde o record está    # TODO: testar
        except:
            record_found_in = []

    collection_to_add_to = collection_id
    record = Record.objects.get(id=record_id)  # obtém objecto record
    discogs_record = discogs.get_record_master_by_id(record.discogs_release_id)
    tracks = discogs_record.tracklist
    videos = discogs_record.videos

    votes_count = Rating.objects.filter(record_id=record_id).count()
    avg_rating = Rating.objects.filter(record_id=record_id).aggregate(avg_rating=Avg('rating'))
    # convert to int (no half stars)
    avg_rating = int(avg_rating["avg_rating"]) if avg_rating["avg_rating"] else 0

    context = {'collection_to_add_to': collection_to_add_to,
               'user_rating': user_rating,
               'record_found_in': record_found_in,
               'record': record,
               'tracks': tracks,
               'videos': videos,
               'votes_count': votes_count,
               'avg_rating': avg_rating}
    template = 'record.html'

    return render(request, template_name=template, context=context)


def _is_super_user(user):
    return user.is_superuser


@user_passes_test(_is_super_user)
def staff_picks(request):
    picks = Staff_Picks.objects.all().order_by('-creation_date')
    paginator = Paginator(picks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'staff_picks.html', {'page_obj': page_obj})
    
@login_required
def add_to_collection(request, record_id):
    user_collections = Collection.objects.filter(user_id = request.user)
    context = {'user_collections': user_collections, 'record_id': record_id}
    return render(request, "add_to_collection.html", context)


@user_passes_test(_is_super_user)
def staff_pick_edit(request, pick_id):
    sp = get_object_or_404(Staff_Picks, pk=pick_id)
    if request.method=="POST":
        if request.POST.get("title") and request.POST.get("recommendation"):
            sp.title=request.POST.get("title") 
            sp.recommendations=request.POST.get("recommendation")
            sp.save()
            return HttpResponseRedirect(reverse('home:staff_picks'))
    rec = sp.record
    votes_count = Rating.objects.filter(record_id=rec).count()
    avg_rating = Rating.objects.filter(record_id=rec).aggregate(avg_rating=Avg('rating'))
    # convert to int (no half stars)
    avg_rating = int(avg_rating["avg_rating"]) if avg_rating["avg_rating"] else 0
    tracks = discogs.get_record_master_by_id(rec.discogs_release_id).tracklist
    context = {
        "record": rec,
        "votes_count": votes_count,
        "avg_rating": avg_rating,
        "tracks": tracks,
        "pick": sp,
        }
    return render(request, 'staff_pick.html', context)


@user_passes_test(_is_super_user)
def staff_pick_add(request, record_id):
    rec = get_object_or_404(Record, pk=record_id)
    if request.method=="POST":
        if request.POST.get("title") and request.POST.get("recommendation"):
            sp = Staff_Picks.objects.create(user=request.user, record=rec, 
                    title=request.POST.get("title"), 
                    recommendations=request.POST.get("recommendation"))
            return HttpResponseRedirect(reverse('home:staff_picks'))
    votes_count = Rating.objects.filter(record_id=record_id).count()
    avg_rating = Rating.objects.filter(record_id=record_id).aggregate(avg_rating=Avg('rating'))
    # convert to int (no half stars)
    avg_rating = int(avg_rating["avg_rating"]) if avg_rating["avg_rating"] else 0
    tracks = discogs.get_record_master_by_id(rec.discogs_release_id).tracklist
    context = {
        "record": rec,
        "votes_count": votes_count,
        "avg_rating": avg_rating,
        "tracks": tracks
        }
    return render(request, 'staff_pick.html', context)


@user_passes_test(_is_super_user)
def staff_pick_delete(request, pick_id):
    get_object_or_404(Staff_Picks, pk=pick_id).delete()
    return HttpResponseRedirect(reverse('home:staff_picks'))


def play_record(request):
    pass
@login_required
def add_to_collection_save(request, record_id):
    
    new_addition = None
    try:
        new_addition = Collection_Record(record_id = Record.objects.get(pk=record_id), collection_id=Collection.objects.get(pk=request.POST['collection']))
        collection_id = Collection.objects.get(pk=request.POST['collection'])
            
    except:
        return render(request, 'add_to_collection.html', {'error_message': 'Please, choose one collection.', 'record_id': record_id})
    
    # TODO: lidar com IntegrityError 

    else:
        new_addition.save()
        return HttpResponseRedirect(reverse('home:single_collection', args=(request.user.username, collection_id.id,))) 


@login_required
def remove_from_collection(request, collection_id, record_id):
    
    to_remove = Collection_Record.objects.get(collection_id = collection_id, record_id = record_id)
    to_remove.delete()
    return HttpResponseRedirect(reverse('home:single_collection', args=(request.user.username, collection_id,))) 


def single_collection(request, username, collection_id):
    records_list = []
    #ratings_list = []
    template = 'single_collection.html'
    collection = Collection.objects.get(pk=collection_id)
    records = Collection_Record.objects.filter(collection_id=collection_id)
    for record in records:
        records_list.append(Record.objects.get(pk=record.record_id.id))
    user_ratings = Rating.objects.filter(user_id = collection.user_id.id)
    context = {'username': username, 'collection': collection, 'records_list':records_list, 'user_ratings': user_ratings}
    
    return render(request, template, context)


def mycollections(request, username, must_login=False):
    current_user = None
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.get(username=username)
    collections_list = Collection.objects.filter(user_id=current_user.id)
    return render(request, 'mycollections.html', {'collections_list': collections_list, 'current_user': current_user, 'username': username, 'must_login': must_login})


def new_collection_form(request, username):
    must_login = False
    if request.user.is_authenticated:
        return render(request, "create_collection.html")
    else:
        must_login = True
        return HttpResponseRedirect(reverse("home:mycollections", args=(username, must_login,)))


def save_new_collection(request, username):
    new_collection = None
    try:
        new_collection = Collection(
            user_id=request.user, name=request.POST['collection_name'], creation_date=timezone.now())
        if not new_collection.name:
            return render(request, 'create_collection.html', {'error_message': 'Por favor, atribua um nome à nova coleção.'})
    except(KeyError):
        return HttpResponseRedirect(reverse("home:create_collection"))
    else:
        new_collection.save()
        return HttpResponseRedirect(reverse('home:mycollections', args=(username,)))


def my_artists(request):
    artists = None
    context = {
        "artists": artists,
    }
    return render(request, 'my_artists.html', context)
