from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    #path('my_collections/<int:user_id>', views.collections_index, name='collections_index'),
    path('', views.home_index, name='home_index'),
    path('register', views.register, name="register"),
    path('search', views.search, name="search"),
    path('search/<int:collection_id>', views.search, name="search"),
    path('artist/<int:artist_id>', views.artist, name='artist'),
    path('record/<int:record_id>', views.record, name='record'),
    path('artist/save/d/<int:discogs_id>', views.discogs_save_artist, name='discogs_save_artist'),
    path('record/save/d/<str:discogs_master_id>', views.discogs_save_record, name='discogs_save_record'),
    path('artist/<int:artist_id>/like', views.save_like_artist, name='like_artist'),
    path('artist/<int:artist_id>/unlike', views.save_unlike_artist, name='unlike_artist'),
    path('review', views.review, name='review'),
    path('review/<int:review_id>', views.review, name='review'),
    path('reviews', views.reviews, name='reviews'),
    path('mycollections/<str:username>', views.mycollections, name='mycollections'),
    path('mycollections/<str:username>/new_collection', views.new_collection_form, name='new_collection_form'),
    path('mycollections/<str:username>/save_collection', views.save_new_collection, name='save_new_collection'),
    path('mycollections/<str:username>/<int:collection_id>', views.single_collection, name='single_collection'),
    path('mycollections/<str:username>/<int:collection_id>/add_new_record', views.add_to_collection, name='add_to_collection'),
    path('myartists', views.my_artists, name='myartists'),
    path('staffpick', views.staff_picks, name='staff_picks'),
    path('staffpick/<int:pick_id>', views.staff_pick_edit, name='staff_pick'),
    path('staffpick/<int:pick_id>/delete', views.staff_pick_delete, name='staff_pick_delete'),
    path('record/<int:record_id>/staffpick', views.staff_pick_add, name='staff_pick_add'),
    path('add_to_collection/<int:record_id>', views.add_to_collection, name='add_to_collection'),
    path('add_to_collection/<int:record_id>/save', views.add_to_collection_save, name='add_to_collection_save'),
    path('remove_from_collection/<int:collection_id>/<int:record_id>', views.remove_from_collection, name='remove_from_collection'),

]

