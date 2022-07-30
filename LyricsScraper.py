import lyricsgenius as lg

class LyricsScraper:
    def __init__(self, auth_input = "2deZwjOJD4SByuFg4c0xQDOzQFPh3YNFElU6y6KJIsBrXcWTFNwDP2LI40ApfcKW"):
        self.auth = auth_input
        self.genius = lg.Genius(auth_input, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
    
    def get_lyrics(self, song, artist = ""):
        return self.genius.search_song(song).lyrics if (artist == "") else self.genius.search_song(song, artist).lyrics

    def get_songs_from_artist(self, artist, n = 10):
        songs = []
        results = self.genius.search(artist, per_page = n)
        list_results = results["hits"]
        for res in list_results:
            if (res["type"] == "song"):
                ft = res["result"]["full_title"]
                songs.append(ft[0:ft.index(" by")])
        return songs
    
    def write_lyrics_to_file(self, song, file, artist = ""):
        file = open(file, "w", encoding = "UTF-8")
        if (artist == ""):
            file.write(self.get_lyrics(song))
        else:
            file.write(self.get_lyrics(song, artist))
