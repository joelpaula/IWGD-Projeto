from typing import List
import requests


class DiscogsArtist:
    def __init__(self, title, discogs_id, cover_image):
        self.title = title
        self.discogs_id = discogs_id
        self.cover_image = cover_image
        self.bio = None

    def __str__(self) -> str:
        return f"[{self.discogs_id}] {self.title}"
    
    def __repr__(self) -> str:
        return self.__str__()
    

class DiscogsRecord:
    def __init__(self, title, discogs_master_id, cover_image, year):
        self.title = title
        self.discogs_master_id = discogs_master_id
        self.cover_image = cover_image
        self.year = year
        self.artist : DiscogsArtist
        self.tracklist: List[DiscogsTrack] = []

    def __str__(self) -> str:
        return f"[{self.discogs_master_id}] {self.title}"
    
    def __repr__(self) -> str:
        return self.__str__()


class DiscogsTrack:
    def __init__(self, title, position, duration) -> None:
        self.title = title
        self.position = position
        self.duration = duration

    def __str__(self) -> str:
        return f"{self.position} - {self.title} [{self.duration}]"
    
    def __repr__(self) -> str:
        return self.__str__()

_headers = {
    'User-Agent': 'Grupo22TestDjangoProject/0.1 +https://github.com/joelpaula/Interfaces-Web',
    'Authorization': 'Discogs key=cKSyLXiSxCJNlrKOxolL, secret=AyGJnWvaPdeUCzFLPTgpWruaqIKRvujS'
}
_baseurl = "https://api.discogs.com"

def search_artists(query: str) -> List[DiscogsArtist]:
    res = []

    url = _baseurl + "/database/search"
    payload={"type": "artist", "q": query}
    response = requests.request("GET", url, headers=_headers, params=payload)

    for result in response.json()["results"][0:5]:
        artist = DiscogsArtist(result["title"], result["id"], result["cover_image"])
        url = f"{_baseurl}/artists/{artist.discogs_id}"
        response = requests.request("GET", url, headers=_headers)
        artist.bio = response.json()["profile"]
        res.append(artist)

    return res

def search_records(query: str) -> List[DiscogsRecord]:
    res = []

    url = _baseurl + "/database/search"
    payload={"type": "release", "q": query}
    response = requests.request("GET", url, headers=_headers, params=payload)
    #res= response.json()
    try:
        for result in response.json()["results"]:
            if any(r.discogs_master_id == result["master_id"] for r in res):
                continue
            record = DiscogsRecord(result["title"], result["master_id"], result["cover_image"], result["year"])
            res.append(record)
    finally:
        return res

def get_artist_by_id(artist_id) -> DiscogsArtist:
    res = DiscogsArtist(None, None, None)
    url = f"{_baseurl}/artists/{artist_id}"
    response = requests.request("GET", url, headers=_headers)
    art = response.json()
    res=DiscogsArtist(title=art["name"], 
        discogs_id=art["id"], 
        cover_image=art["images"][0]["uri"])
    res.bio = art["profile"]

    return res

def get_record_master_by_id(master_record_id, include_tracklist = True) -> DiscogsRecord:
    res = DiscogsRecord(None, None, None, None)
    url = f"{_baseurl}/masters/{master_record_id}"
    response = requests.request("GET", url, headers=_headers)
    rec = response.json()
    res=DiscogsRecord(title=rec["title"], 
        discogs_master_id=rec["id"], 
        cover_image=rec["images"][0]["uri"],
        year=rec["year"])
    art = rec["artists"][0]
    res.artist = DiscogsArtist(art["name"], art["id"], art.get("thumbnail_url", ""))
    if include_tracklist:
        for track in rec["tracklist"]:
            res.tracklist.append(DiscogsTrack(track["title"], track["position"], track["duration"]))
    return res
