from _typeshed import Self
import requests

headers = {
    'User-Agent': 'Grupo22TestDjangoProject/0.1 +https://github.com/joelpaula/Interfaces-Web',
    'Authorization': 'Discogs key=cKSyLXiSxCJNlrKOxolL, secret=AyGJnWvaPdeUCzFLPTgpWruaqIKRvujS'
}
baseurl = "https://api.discogs.com"

class discog_artist:
    def __init__(self, title, discogs_id, cover_image):
        self.title = title
        self.discogs_id = discogs_id
        self.cover_image = cover_image
        self.bio = None

    def __str__(self) -> str:
        return f"[{self.discogs_id}] {self.title}"
    
    def __repr__(self) -> str:
        return self.__str__()
    

class discog_record:
    def __init__(self, title, discogs_master_id, cover_image, year):
        self.title = title
        self.discogs_master_id = discogs_master_id
        self.cover_image = cover_image
        self.year = year

    def __str__(self) -> str:
        return f"[{self.discogs_master_id}] {self.title}"
    
    def __repr__(self) -> str:
        return self.__str__()


class Discogs:
    def search_artists(query):
        res = []

        url = baseurl + "/database/search"
        payload={"type": "artist", "q": query}
        response = requests.request("GET", url, headers=headers, params=payload)

        for result in response.json()["results"][0:5]:
            artist = discog_artist(result["title"], result["id"], result["cover_image"])
            url = f"{baseurl}/artists/{artist.discogs_id}"
            response = requests.request("GET", url, headers=headers)
            artist.bio = response.json()["profile"]
            res.append(artist)

        return res

    def search_records(query):
        res = []

        url = baseurl + "/database/search"
        payload={"type": "release", "q": query}
        response = requests.request("GET", url, headers=headers, params=payload)
        #res= response.json()
        try:
            for result in response.json()["results"][0:10]:
                record = discog_record(result["title"], result["master_id"], result["cover_image"], result["year"])
                res.append(record)
        finally:
            return res


