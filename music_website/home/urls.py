from django.urls import path
from . import views


app_name = 'home'

urlpatterns = [
    #path('my_collections/<int:user_id>', views.collections_index, name='collections_index'),
    path('my_collections/<int:user_id>/<int:collection_id>', views.mycollection, name='mycollection'),
    path('', views.home_index, name='home_index'),
    path('artist/<int:artist_id>', views.artist, name='artist')

]