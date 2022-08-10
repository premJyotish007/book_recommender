from msilib.schema import File
import music_api.spotifyAPI
import pandas as pd
import music_api.GeniusAPI as genius_api
import NLP

class TrackAnalysis:
    def __init__(self) -> None:
        self.spotify = music_api.spotifyAPI.TrackInfo()
        self.ls = genius_api.LyricsScraper()
        self.nlp = NLP.Analyze()

    def get_artists_from_file(self, file) -> list[str]:
        artists = []
        with open (file, "r") as input_file:
            lines = input_file.readlines()
            artists = [line.strip() for line in lines]
        return set(artists)

    def append_data(self, dicts, file) -> None:
        headers = []
        with open("music_api/analysis_headers.txt", "r") as headers_file:
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
                    to_append = self.get_track_info(a, song, track)
                    if (len(to_append) > 0):
                        dicts.append(to_append)
                    size += 1
        return dicts
    
    def get_track_info(self, song, a = "", track = ""):
        if (len(track) == 0):
            track_info = self.spotify.get_track_uri(song)
            track = track_info[0]
            a = track_info[1]
        to_return = self.spotify.track_features(track)[0]
        to_return['artist'] = a
        to_return['song'] = song

        # Obtaining lyrics of a song
        lyrics = self.ls.get_lyrics(song, a)
        lyrics = self.process_lyrics(lyrics, song)
        if (lyrics == "not found" or "1." in lyrics):
            return {}
        to_return["lyrics"] = lyrics

        # Analyzing lyrics
        analysis = self.nlp.analyze(text = lyrics)
        tones_to_analyze = ["sadness", "joy", "fear", "disgust", "anger"]
        for tone in tones_to_analyze:
            to_return[tone] = self.tone_value(analysis, tone)
        return to_return



    def get_track(self, track_uri) -> str:
        return self.spotify.track(track_uri)
    
    def append_artists(self, file, output_file) -> None:
        for line in self.get_artists_from_file(file):
            print(f"Appending {line},")
            dicts = self.generate_track_data(line)
            self.append_data(dicts, output_file)

    def contains_proper_characters(self, lyrics):
        if ("??" in lyrics):
            return False
        for char in lyrics:
            if ord(char) > 128:
                return False
        return True
    def process_lyrics(self, lyrics, song):
        keywords = ["-", "(ft", "live", "(feat", "feat", "ft", "("]
        if "1." in lyrics:
            for keyword in keywords:
                if (keyword in song):
                    song = song[0:song.index(keyword)]
                    break
            lyrics = self.ls.get_lyrics(song)
        if ("Lyrics" in lyrics):
            try:
                lyrics = lyrics[(lyrics.index("Lyrics") + 6): lyrics.index("Embed")]
            except:
                lyrics = lyrics[(lyrics.index("Lyrics") + 6):]
            lyrics = str(lyrics).strip()
        return lyrics
    
    def keywords(self, lyrics):
        try:
            keywords = self.nlp.get_keywords(lyrics)
            keywords.sort()
            return keywords
        except:
            return []
    
    def tone_value(self, tone_arr, tone_input):
        for tone in tone_arr:
            if (len(tone) > 0):
                if (tone[0] == tone_input):
                    return tone[1]
        return 0