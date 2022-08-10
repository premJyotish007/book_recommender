import spotipy
import os
import json
from spotipy.oauth2 import SpotifyClientCredentials

os.environ["SPOTIPY_CLIENT_ID"] = "987d1f0d327c4804bb7a2d487f3235ad"
os.environ["SPOTIPY_CLIENT_SECRET"] = "d40a35f91657451bb3e54a05c906560a"

class TrackInfo:
    def __init__(self) -> None:
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    
    def get_artist_uri(self, search_query) -> str:
        result = self.spotify.search(search_query, 5, type = 'artist')
        return result['artists']['items'][0]["uri"]
    
    def get_album_uri(self, search_query) -> str:
        result = self.spotify.search(search_query, 5, type = 'album')
        return result['albums']['items'][0]["uri"]
    
    def get_track_uri(self, search_query) -> str:
        result = self.spotify.search(search_query, 1, type = 'track')
        return (result['tracks']['items'][0]["uri"], result['tracks']['items'][0]["album"]["artists"][0]["name"])

    def get_albums(self, artist_uri, n = 20) -> list[list[str]]:
        to_return = []
        arg = artist_uri if "spotify:artist" in artist_uri else self.get_artist_uri(artist_uri)
        albums =  self.spotify.artist_albums(artist_uri, album_type = "album", limit = n)
        for result in albums["items"]:
            to_return.append([result["name"], result["uri"]])
        return to_return
    
    def get_songs_from_album(self, album, n = 50) -> list[str]:
        arg = album if "spotify:album" in album else self.get_album_uri("album")
        tracks =  self.spotify.album_tracks(arg)
        return [item["uri"] for item in tracks["items"]]
        
    def track(self, track_uri) -> str:
        return self.spotify.track(track_uri)
    
    def track_features(self, track_uri) -> dict:
        return self.spotify.audio_features(track_uri)

    def get_genres_list(self):
        return self.spotify.recommendation_genre_seeds()
t = TrackInfo()
print(t.get_track_uri("Beat It"))