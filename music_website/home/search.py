from typing import List
import Levenshtein as lev
from django.core.checks.messages import Debug
import home.discogs as discogs
from home.models import Artist, Record
from home.discogs import DiscogsRecord


class Result:
    RECORD = "Record"
    ARTIST = "Artist"

    def __init__(self, discogs_id, title, cover_image, type_=RECORD):
        self.id=0
        self.discogs_id = discogs_id
        self.title = title
        self.cover_image = cover_image
        self.type_ = type_
        self.specifics = {}
        self.matching = 0

    def __str__(self) -> str:
        return f"[{self.discogs_id}] {self.title}"
    
    def __repr__(self) -> str:
        return self.__str__()


class Search:
    def search(self, query: str):
        res = []

        res.extend(self._get_discogs_artists(query))
        res.extend(self._get_discogs_records(query))
        self._check_db_ids(res)
        res = self._order_results(query, res)

        return res
    
    def _check_db_ids(self, results: List[Result]):
        for result in results:
            if result.type_ == Result.ARTIST:
                try:
                    art: Artist = Artist.objects.get(discogs_artist_id=result.discogs_id)
                    result.id = art.pk
                except (KeyError, Artist.DoesNotExist):
                    continue
            else:
                try:
                    rec: Record = Record.objects.get(discogs_release_id=result.discogs_id)
                    result.id = rec.pk
                except (KeyError, Record.DoesNotExist):
                    continue
                
        return

    def _order_results(self, query: str, results: List[Result]) -> List[Result]:
        # uses the Levenshtein distance to calculate similarity
        for item in results:
            item.matching = lev.distance(item.title, query)

        return sorted(results, key=lambda x: x.matching)

    def _get_discogs_records(self, query: str) -> List[Result]:
        res = []
        records = discogs.search_records(query)
        for rec in records:
            a = Result(rec.discogs_master_id, rec.title, rec.cover_image, Result.RECORD)
            a.specifics["year"] = rec.year
            res.append(a)
        return res

    def _get_discogs_artists(self, query: str) -> List[Result]:
        res = []
        artists = discogs.search_artists(query)
        for art in artists:
            a = Result(art.discogs_id, art.title, art.cover_image, Result.ARTIST)
            a.specifics["bio"] = art.bio
            res.append(a)
        return res