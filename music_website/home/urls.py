from django.urls import path

from home.discogs import discog_artist
from home import views


app_name = 'home'

urlpatterns = [
    #path('my_collections/<int:user_id>', views.collections_index, name='collections_index'),
    path('my_collections/<int:user_id>/<int:collection_id>', views.mycollection, name='mycollection'),
    path('', views.home_index, name='home_index'),
    path('register', views.register, name="register"),
    path('record', views.record, name='record'),
 #    path('artist/<int:d_artist.discogs_id>', views.artist, name='artist', kwargs={'d_artist': d_artist})

]