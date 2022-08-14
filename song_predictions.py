import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
import NLP
import music_api.track_analysis

class Predict:
    def __init__(self, database: str) -> None:
        self.nlp = NLP.Analyze()
        self.df = pd.read_csv(database)
        categorical = ["artist" , "song", "type", "id", "uri", "track_href", "analysis_url", "lyrics"]
        self.columns = [col for col in self.df.columns if col not in categorical]
        self.trained = False
        self.kmeans = KMeans()
    
    def optimal_k_means(self, max_num_clusters):
        sil_arr = {}
        for n in range(4, max_num_clusters):
            kmeans = KMeans(n_clusters = n, random_state = 1).fit(self.df[self.columns])
            score = metrics.silhouette_score(self.df[self.columns], kmeans.labels_, metric = 'euclidean')
            sil_arr[n] = score
        max_score = max(sil_arr.values())
        for key, value in sil_arr.items():
            if (value == max_score):
                return key
    
    def train_dataset(self, n = 47):
        self.trained = True
        self.kmeans = KMeans(n_clusters = n, random_state = 1).fit(self.df[self.columns])
        self.df["cluster"] = self.kmeans.predict(self.df[self.columns])
    

    def get_recommendations(self, song):
        if (not self.trained):
            return "Train the data first."
        ta = music_api.track_analysis.TrackAnalysis()
        song = ta.get_track_info(song)
        df_song = pd.DataFrame(song, index = [0])
        target = self.kmeans.predict(df_song[self.columns])
        df_target = self.df[self.df["cluster"] == target[0]].copy()
        def get_similarity(row, lyrics):
            return self.nlp.word_similarity(lyrics, row["lyrics"])
        df_target["similarity"] = df_target.apply(get_similarity, args = [df_song["lyrics"][0]], axis = 1)
        df_target.sort_values(by = "similarity", ascending = False, inplace = True)
        return df_target.head()
