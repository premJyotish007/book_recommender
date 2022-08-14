# Code snippet to add song data
import music_api.track_analysis
ta = music_api.track_analysis.TrackAnalysis()
ta.append_artists(input_file = "" , output_file = "") # input file is a txt file with list of artists, output file is a csv of the dataset



# Code snippet to make predictions
import song_predictions

p = song_predictions.Predict(dataset = "") #dataset consisting of the songs

p.train_dataset()

print(p.get_recommendations(song = ""))