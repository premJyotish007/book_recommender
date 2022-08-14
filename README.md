# Cram Your Jam

<hr>
Book recommendation algorithm that relies on a user's song playlist to make accurate suggestions for next books to read.

As two mediums of expressions inherently tied to the same emotional stimulator: text/lyrics, the choice of your songs can reveal a lot about what books you might be interested in, through the song pace, its genres, any specific themes and/or nouns associated with it, and so on.

Current progress:
Have set up an API infrastructure to make REST API calls to the spotify api for song properties, a song lyrics scraper, and the google books api to accumulate data about books, their description, categories, and themes. This obtained data serves to represent as many genres and as many varations of choices possible among listeners. 

Have implemented a naive kmeans clustering + rigourous NLP model that uses 15 different factors about every song including + sentiment analysis + WMD (word mover's distance) algorithms implemented by the spacy library to make informed predictions about songs given a single song/playlist of songs.

Next Steps:
Connecting datapoints among songs to those in books to devise a neural network/decision tree model + graph algorithms for book recommendations
