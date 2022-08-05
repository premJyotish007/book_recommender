from msilib.schema import File
import music_api.spotifyAPI
import pandas as pd

class TrackAnalysis:
    def __init__(self) -> None:
        self.spotify = music_api.spotifyAPI.TrackInfo()

    def get_artists_from_file(self, file) -> list[str]:
        artists = []
        with open (file, "r") as input_file:
            lines = input_file.readlines()
            artists = [line.strip() for line in lines]
        return set(artists)

    def append_data(self, dicts, file) -> None:
        headers = []
        with open("C:/Users/harsh/Desktop/spotify api/book_recommender/music_api/analysis_headers.txt", "r") as headers_file:
            headers = [line.strip() for line in headers_file.readlines()]
        df = pd.DataFrame()
        try:
            df = pd.read_csv(file, usecols=headers)
        except:
            df = pd.DataFrame()
        df = df.append(dicts, ignore_index=True)
        df.to_csv(file, index = False)


    def generate_track_data(self, a) -> dict:
        a_uri = self.spotify.get_artist_uri(a)
        a_albums = self.spotify.get_albums(a_uri)
        print(a_uri)
        size = 0
        dicts = []
        songs = set()
        for item in a_albums:
            album = item[1]
            tracks = self.spotify.get_songs_from_album(album)
            for track in tracks:
                song = self.spotify.track(track)["name"]
                songs.add(song)
                if (len(songs) > size):
                    to_append = self.spotify.track_features(track)[0]
                    to_append['Artist'] = a
                    to_append['Song'] = song
                    dicts.append(to_append)
                    size += 1
        return dicts

    def get_track(self, track_uri) -> str:
        return self.spotify.track(track_uri)
    
    def append_artists(self, file, output_file) -> None:
        for line in self.get_artists_from_file(file):
            print(f"Appending {line},")
            dicts = self.generate_track_data(line)
            self.append_data(dicts, output_file)