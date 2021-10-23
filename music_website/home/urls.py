from django.urls import path

from home.discogs import DiscogsArtist
from home import views


app_name = 'home'

urlpatterns = [
    #path('my_collections/<int:user_id>', views.collections_index, name='collections_index'),
    path('my_collections/<int:user_id>/<int:collection_id>', views.mycollection, name='mycollection'),
    path('', views.home_index, name='home_index'),
    path('register', views.register, name="register"),
    path('search', views.search, name="search"),
    path('artist/<int:artist_id>', views.artist, name='artist'),
    path('record/<int:record_id>', views.record, name='record'),

]