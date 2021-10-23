import Levenshtein as lev
import home.discogs as discogs
from home.models import Artist, Record


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
    def search(self, query):
        res = []

        res.extend(self._get_discogs_artists(query))
        res.extend(self._get_discogs_records(query))
        res = self.order_results(query, res)

        return res
    
    def order_results(self, query, results):
        for item in results:
            item.matching = lev.distance(item.title, query)

        return sorted(results, key=lambda x: x.matching)

    def _get_discogs_records(self, query):
        res = []
        records = discogs.search_records(query)
        for rec in records:
            a = Result(rec.discogs_master_id, rec.title, rec.cover_image, Result.RECORD)
            a.specifics["year"] = rec.year
            res.append(a)
        return res

    def _get_discogs_artists(self, query):
        res = []
        artists = discogs.search_artists(query)
        for art in artists:
            a = Result(art.discogs_id, art.title, art.cover_image, Result.ARTIST)
            a.specifics["bio"] = art.bio
            res.append(a)
        return res