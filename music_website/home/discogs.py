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
        self.artist: DiscogsArtist
        self.tracklist: List[DiscogsTrack] = []
        self.videos: List[DiscogsVideos] = []

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
        return f"{self.position} - {self.title} ({self.duration})"

    def __repr__(self) -> str:
        return self.__str__()


class DiscogsVideos:
    def __init__(self, title, uri, description) -> None:
        self.title = title
        self.uri = uri
        self.description = description

    def __str__(self) -> str:
        return f"{self.title}"

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
    payload = {"type": "artist", "q": query}
    response = requests.request("GET", url, headers=_headers, params=payload)

    for result in response.json()["results"]:
        if str(result["cover_image"]).endswith("spacer.gif"):
            continue
        artist = DiscogsArtist(
            result["title"], result["id"], result["cover_image"])
        url = f"{_baseurl}/artists/{artist.discogs_id}"
        response = requests.request("GET", url, headers=_headers)
        artist.bio = response.json()["profile"]
        res.append(artist)
        if len(res) >= 5: 
            break

    return res


def search_records(query: str) -> List[DiscogsRecord]:
    res = []

    url = _baseurl + "/database/search"
    payload = {"type": "release", "q": query}
    response = requests.request("GET", url, headers=_headers, params=payload)
    #res= response.json()
    try:
        for result in response.json()["results"]:
            if any(r.discogs_master_id == result["master_id"] for r in res):
                continue
            # handle master id = 0
            id = - \
                result["id"] if result["master_id"] == 0 else result["master_id"]
            record = DiscogsRecord(
                result["title"], id, result["cover_image"], result["year"])
            res.append(record)
    finally:
        return res


def get_artist_by_id(artist_id) -> DiscogsArtist:
    res = DiscogsArtist(None, None, None)
    url = f"{_baseurl}/artists/{artist_id}"
    response = requests.request("GET", url, headers=_headers)
    art = response.json()
    res = DiscogsArtist(title=art["name"],
                        discogs_id=art["id"],
                        cover_image=None)
    if art.get("images") and len(art["images"]):
        res.cover_image = art["images"][0]["uri"]
    res.bio = art["profile"]

    return res


def get_record_master_by_id(master_record_id, include_tracklist=True, include_videos=True) -> DiscogsRecord:
    res = DiscogsRecord(None, None, None, None)
    master_record_id = int(master_record_id)
    if master_record_id > 0:
        url = f"{_baseurl}/masters/{master_record_id}"
    else:
        url = f"{_baseurl}/releases/{-master_record_id}"
    response = requests.request("GET", url, headers=_headers)
    rec = response.json()
    res = DiscogsRecord(title=rec["title"],
                        discogs_master_id=master_record_id,
                        cover_image=None,
                        year=rec["year"])
    if rec.get("images") and len(rec["images"]):
        res.cover_image = rec["images"][0]["uri"]
    art = rec["artists"][0]
    res.artist = DiscogsArtist(
        art["name"], art["id"], art.get("thumbnail_url", ""))
    if include_tracklist and rec.get("tracklist"):
        for track in rec["tracklist"]:
            res.tracklist.append(DiscogsTrack(
                track["title"], track["position"], track["duration"]))
    if include_videos and rec.get("videos"):
        for video in rec["videos"]:
            res.videos.append(DiscogsVideos(
                video["title"], video["uri"], video["description"]))
    return res
