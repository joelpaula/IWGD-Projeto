from django.http import Http404
from home.models import Artist, Record
from . import discogs


def save_artist_to_db(discogs_id) -> int:
    try:
        db_art = Artist.objects.get(discogs_artist_id=discogs_id)
    except:
        try:
            artist = discogs.get_artist_by_id(artist_id=discogs_id)
            db_art = Artist(discogs_artist_id=discogs_id, name=artist.title, bio=artist.bio, picture_url=artist.cover_image)
            db_art.save()        
        except:
            raise Http404("Artist not found or not saved")
        
    return db_art.pk

def save_record_to_db(discogs_release_id) -> int:
    try:
        db_rec = Record.objects.get(discogs_release_id=discogs_release_id)
    except:
        try:
            record = discogs.get_record_master_by_id(discogs_release_id)
            artist_id = save_artist_to_db(record.artist.discogs_id)
            db_rec = Record(artist_id=Artist.objects.get(pk=artist_id), discogs_release_id=discogs_release_id, title=record.title, year=record.year, cover_url=record.cover_image)
            db_rec.save()
        except:
            raise Http404("Record not found or not saved")
    
    return db_rec.pk
    