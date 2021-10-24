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
    path('mycollections/<str:username>', views.mycollections, name='mycollections'),


]