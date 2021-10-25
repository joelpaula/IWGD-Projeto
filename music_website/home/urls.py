from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    #path('my_collections/<int:user_id>', views.collections_index, name='collections_index'),
    path('', views.home_index, name='home_index'),
    path('register', views.register, name="register"),
    path('search', views.search, name="search"),
    path('artist/<int:artist_id>', views.artist, name='artist'),
    path('record/<int:record_id>', views.record, name='record'),
    path('artist/save/d/<int:discogs_id>', views.discogs_save_artist, name='discogs_save_artist'),
    path('record/save/d/<int:discogs_master_id>', views.discogs_save_record, name='discogs_save_record'),
    path('artist/<int:artist_id>/like_artist', views.save_like_artist, name='like_artist'),
    path('review', views.review, name='review'),
    path('review/<int:review_id>', views.review, name='review'),
    path('reviews', views.reviews, name='reviews'),
    path('mycollections/<str:username>', views.mycollections, name='mycollections'),
    path('mycollections/<str:username>/new_collection', views.new_collection_form, name='new_collection_form'),
    path('mycollections/<str:username>/save_collection', views.save_new_collection, name='save_new_collection'),
    path('mycollections/<str:username>/<int:collection_id>', views.single_collection, name='single_collection'),
    path('mycollections/<str:username>/<int:collection_id>/add_new_record', views.add_to_collection, name='add_to_collection'),

]

